# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth

from core import resource
from core.jsonresponse import create_response
from core import paginator
from eaglet.utils.resource_client import Resource

from util import db_util
from resource import models as resource_models
from product_catalog import models as catalog_models
from account.models import *
from util import string_util
from panda.settings import ZEUS_HOST, ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
from product.sales_from_weapp import sales_from_weapp
import nav
import models
import requests

FIRST_NAV = 'product'
SECOND_NAV = 'product-list'
filter2field = {
	'product_name_query': 'product_name'
}

product_status2text = {
	0: u'未上架',
	1: u'已上架'
}


class ProductList(resource.Resource):
	app = 'product'
	resource = 'product_list'

	@login_required
	def get(request):
		"""
		显示商品列表
		"""
		user_has_products = len(models.Product.objects.filter(owner_id=request.user.id))
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
			'user_has_products': user_has_products,
		})

		return render_to_response('product/product_list.html', c)

	def api_get(request):
		is_export = False
		rows, pageinfo = getProductData(request, is_export)
		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}

		# 构造response
		response = create_response(200)
		response.data = data
		return response.get_response()


def getProductData(request, is_export):
	cur_page = request.GET.get('page', 1)
	filter_idct = dict(
		[(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET if
		 key.startswith('__f-')])
	product_name = filter_idct.get('product_name', '')

	role = UserProfile.objects.get(user_id=request.user.id).role
	products = models.Product.objects.filter(owner=request.user, is_deleted=False).order_by('-id')

	# 查询
	if product_name:
		products = products.filter(product_name__icontains=product_name)

	product_ids = ['%s' % product.id for product in products]
	product_has_relations = models.ProductHasRelationWeapp.objects.filter(product_id__in=product_ids).exclude(
		weapp_product_id='')
	product_images = models.ProductImage.objects.filter(product_id__in=product_ids)

	# 从weapp获取商品销量
	id2sales = sales_from_weapp(product_has_relations)

	# 获取商品图片
	product_id2image_id = {}
	image_id2images = {}
	for product in product_images:
		# product_id2image_id[product.product_id] = product.image_id
		if product.product_id not in product_id2image_id:
			product_id2image_id[product.product_id] = [product.image_id]
		else:
			product_id2image_id[product.product_id].append(product.image_id)
	for image in resource_models.Image.objects.all():
		image_id2images[image.id] = image.path

	if not is_export:
		pageinfo, products = paginator.paginate(products, cur_page, 20, query_string=request.META['QUERY_STRING'])
	# 组装数据
	# 获取多规格商品id和结算价,售价的对应数据
	model_properties = models.ProductModel.objects.filter(owner=request.user, is_deleted=False)
	product_id2market_price = {}
	product_id2product_price = {}
	for model_property in model_properties:
		if model_property.product_id not in product_id2market_price:
			product_id2market_price[model_property.product_id] = [model_property.market_price]
		else:
			product_id2market_price[model_property.product_id].append(model_property.market_price)

		if model_property.product_id not in product_id2product_price:
			product_id2product_price[model_property.product_id] = [model_property.price]
		else:
			product_id2product_price[model_property.product_id].append(model_property.price)

	rows = []
	# 获取商品是否上线
	relations = models.ProductHasRelationWeapp.objects.filter(product_id__in=[p.id for p in products])
	product_2_weapp_product = {}
	for relation in relations:
		product_2_weapp_product.update({int(relation.weapp_product_id): relation.product_id})
	
	weapp_product_ids = '_'.join([p.weapp_product_id for p in relations])
	resp = {}
	if weapp_product_ids:
		params = {
			'product_ids': weapp_product_ids
		}
		resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).get(
			{
				'resource': 'mall.product_status',
				'data': params
			}
		)
	# 已上架商品列表
	product_shelve_on = []
	if resp and resp.get('code') == 200:
		product_status = resp.get('data').get('product_status')
		product_shelve_on = [product_2_weapp_product.get(product_statu.get('product_id'))
							 for product_statu in product_status
							 if product_statu.get('status') == 'on']

	for product in products:
		image_id = -1 if product.id not in product_id2image_id else product_id2image_id[product.id][0]
		image_path = '' if image_id not in image_id2images else image_id2images[image_id]
		sales = 0 if product.id not in id2sales else id2sales[product.id]
		product_has_model = 0
		#如果是多规格价格显示区间
		if product.id in product_id2market_price:
			market_prices = product_id2market_price[product.id]
			market_prices = sorted(market_prices)
			product_has_model = len(market_prices)
			if (market_prices[0] != market_prices[-1]) and len(market_prices) > 1:
				clear_price = ('%.2f ~ %.2f') % (market_prices[0], market_prices[-1])
			else:
				clear_price = '%.2f' % market_prices[0]
		else:
			clear_price = '%.2f' % product.clear_price

		if product.id in product_id2market_price:
			product_prices = product_id2product_price[product.id]
			product_prices = sorted(product_prices)
			if (product_prices[0] != product_prices[-1]) and len(product_prices) > 1:
				product_price = ('%.2f ~ %.2f') % (product_prices[0], product_prices[-1])
			else:
				product_price = '%.2f' % product_prices[0]
		else:
			product_price = '%.2f' % product.product_price

		image_paths = []
		if product.id in product_id2image_id:
			image_ids = product_id2image_id[product.id]
			for i_id in image_ids:
				if i_id in image_id2images:
					image_paths.append(image_id2images[i_id])
		valid_time_from = product.valid_time_from
		valid_time_to = product.valid_time_to
		valid_time = '' if not valid_time_from else ('%s/%s') % (valid_time_from.strftime('%Y-%m-%d %H:%M'), valid_time_to.strftime('%Y-%m-%d %H:%M'))
		rows.append({
			'id': product.id,
			'role': role,
			'promotion_title': product.promotion_title,
			'clear_price': clear_price,
			'product_price': product_price,
			'limit_clear_price': '%.2f' % product.limit_clear_price if product.limit_clear_price > 0 else '',
			'product_weight': '%.2f' % product.product_weight,
			'product_name': product.product_name,
			'image_path': image_path,
			'image_paths': image_paths if image_paths else '',
			'remark': product.remark,
			'status': product_status2text[product.product_status] if product.id not in product_shelve_on else '已上架',
			'sales': '%s' % sales,
			'has_limit_time': valid_time,
			'product_has_model': product_has_model,
			'is_model': product.has_product_model,
			'created_at': product.created_at.strftime('%Y-%m-%d %H:%M')
		})
	if is_export:
		return rows
	else:
		return rows, pageinfo
