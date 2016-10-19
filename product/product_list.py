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
from util import sync_util
from weapp_relation import get_weapp_model_properties

FIRST_NAV = 'product'
SECOND_NAV = 'product-list'
filter2field = {
	'product_name_query': 'product_name',
	'catalog_query': 'catalog_name'
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

		user_has_products = models.Product.objects.filter(owner_id=request.user.id, is_deleted=False).count()

		user_profile = request.user.get_profile()

		if user_profile.max_product <= user_has_products:
			can_created = False
		else:
			can_created = True
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(request),
			'second_nav_name': SECOND_NAV,
			'user_has_products': user_has_products,
			'can_created': can_created,
			'purchaseMethod': user_profile.purchase_method
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

	# def api_post(request):
	# 	product_id = request.POST.get('product_id','')
	# 	if product_id:
	# 		models.Product.objects.filter(id=product_id, is_deleted=False).update(
	# 			''
	# 		)
	# 	response = create_response(200)
	# 	response.data = data
	# 	return response.get_response()


def getProductData(request, is_export):
	cur_page = request.GET.get('page', 1)
	is_update = request.GET.get('is_update', False)

	filter_dict = dict(
		[(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET if
		 key.startswith('__f-')])
	product_name = filter_dict.get('product_name', '')
	catalog_name = filter_dict.get('catalog_name','')

	role = UserProfile.objects.get(user_id=request.user.id).role
	if role == YUN_YING:
		# product_sync_weapps = models.ProductSyncWeappAccount.objects.all()
		# sync_product_ids = []
		# for product_sync_weapp in product_sync_weapps:
		# 	if product_sync_weapp.product_id not in sync_product_ids:
		# 		sync_product_ids.append(product_sync_weapp.product_id)
		products = models.Product.objects.filter(is_deleted=False, is_update=True, is_refused=False).order_by('-id')
	else:
		products = models.Product.objects.filter(owner=request.user, is_deleted=False).order_by('-id')

	# 查询
	if product_name:
		products = products.filter(product_name__icontains=product_name)
	if is_update:
		products = products.filter(is_update=is_update)
	if catalog_name:
		product_catalogs = catalog_models.ProductCatalog.objects.filter(name__icontains=catalog_name)
		father_id2ids = {}
		for product_catalog in catalog_models.ProductCatalog.objects.all():
			if product_catalog.father_id not in father_id2ids:
				father_id2ids[product_catalog.father_id] = [product_catalog.id]
			else:
				father_id2ids[product_catalog.father_id].append(product_catalog.id)
		catalog_ids = []
		for product_catalog in product_catalogs:
			catalog_id = product_catalog.id
			# 查询的是二级分类
			catalog_ids.append(catalog_id)
			catalog_ids.append(product_catalog.father_id)
			# 查询的是一级分类
			if catalog_id in father_id2ids:
				catalog_ids.extend(father_id2ids[catalog_id])
		products = products.filter(catalog_id__in=catalog_ids)

	if not is_export:
		pageinfo, products = paginator.paginate(products, cur_page, 20, query_string=request.META['QUERY_STRING'])

	product_ids = ['%s' % product.id for product in products]
	product_has_relations = models.ProductHasRelationWeapp.objects.filter(product_id__in=product_ids).exclude(
		weapp_product_id='')
	product_images = models.ProductImage.objects.filter(product_id__in=product_ids)

	# 从weapp获取商品销量
	if role == YUN_YING:
		id2sales = {}
		resource_images = resource_models.Image.objects.all()
	else:
		id2sales = sales_from_weapp(product_has_relations)
		resource_images = resource_models.Image.objects.filter(user_id=request.user.id)

	#获取分类
	product_catalogs = catalog_models.ProductCatalog.objects.all()
	id2product_catalog = {product_catalog.id:product_catalog for product_catalog in product_catalogs}

	# 获取商品图片
	product_id2image_id = {}
	image_id2images = {}
	for product in product_images:
		# product_id2image_id[product.product_id] = product.image_id
		if product.product_id not in product_id2image_id:
			product_id2image_id[product.product_id] = [product.image_id]
		else:
			product_id2image_id[product.product_id].append(product.image_id)
	

	for image in resource_images:
		image_id2images[image.id] = image.path

	# 获取商品是否上线
	product_shelve_on = get_shelve_on_product(role=role, product_ids=product_ids, products=products)

	# 组装数据
	# 获取多规格商品id和结算价,售价的对应数据
	user_id2name = {}
	if role == YUN_YING:
		model_properties = models.ProductModel.objects.filter(is_deleted=False)
		p_owner_ids = [product.owner_id for product in products]
		user_profiles = UserProfile.objects.filter(user_id__in=p_owner_ids)
		user_id2name = {user_profile.user_id:user_profile.name for user_profile in user_profiles}
	else:
		model_properties = models.ProductModel.objects.filter(owner=request.user, product_id__in=product_ids, is_deleted=False)

	product_id2market_price = {}
	product_id2product_price = {}
	product_id2product_store = {}
	for model_property in model_properties:
		if model_property.product_id not in product_id2market_price:
			product_id2market_price[model_property.product_id] = [model_property.market_price]
		else:
			product_id2market_price[model_property.product_id].append(model_property.market_price)

		if model_property.product_id not in product_id2product_price:
			product_id2product_price[model_property.product_id] = [model_property.price]
		else:
			product_id2product_price[model_property.product_id].append(model_property.price)

		if model_property.product_id not in product_id2product_store:
			product_id2product_store[model_property.product_id] = [model_property.stocks]
		else:
			product_id2product_store[model_property.product_id].append(model_property.stocks)

	rows = []

	for product in products:
		owner_id = product.owner_id
		image_id = -1 if product.id not in product_id2image_id else product_id2image_id[product.id][0]
		image_path = '' if image_id not in image_id2images else image_id2images[image_id]
		sales = 0 if product.id not in id2sales else id2sales[product.id]
		product_has_model = 0
		#如果是多规格价格显示区间
		if product.id in product_id2market_price and product.has_product_model:
			market_prices = product_id2market_price[product.id]
			market_prices = sorted(market_prices)
			product_has_model = len(market_prices)
			if (market_prices[0] != market_prices[-1]) and len(market_prices) > 1:
				clear_price = ('%.2f ~ %.2f') % (market_prices[0], market_prices[-1])
			else:
				clear_price = '%.2f' % market_prices[0]
		else:
			clear_price = '%.2f' % product.clear_price

		if product.id in product_id2market_price and product.has_product_model:
			product_prices = product_id2product_price[product.id]
			product_prices = sorted(product_prices)
			if (product_prices[0] != product_prices[-1]) and len(product_prices) > 1:
				product_price = ('%.2f ~ %.2f') % (product_prices[0], product_prices[-1])
			else:
				product_price = '%.2f' % product_prices[0]
		else:
			product_price = '%.2f' % product.product_price
		store_short = False
		if product.id in product_id2product_store and product.has_product_model:
			product_stores = product_id2product_store[product.id]
			product_stores = sorted(product_stores)
			if (product_stores[0] != product_stores[-1]) and len(product_stores) > 1:
				product_store = ('%s ~ %s') % (product_stores[0], product_stores[-1])
				if product_stores[-1] < 20:
					store_short = True
			else:
				product_store = '%s' % product_stores[0]
				if product_stores[0] < 20:
					store_short = True
		else:
			product_store = '%s' % product.product_store
			if product.product_store < 20:
				store_short = True

		image_paths = []
		if product.id in product_id2image_id:
			image_ids = product_id2image_id[product.id]
			for i_id in image_ids:
				if i_id in image_id2images:
					image_paths.append(image_id2images[i_id])
		valid_time_from = product.valid_time_from
		valid_time_to = product.valid_time_to
		valid_time = '' if not valid_time_from else ('%s/%s') % (valid_time_from.strftime('%Y-%m-%d %H:%M'), valid_time_to.strftime('%Y-%m-%d %H:%M'))
		
		#商品分类
		first_level_name = ''
		second_level_name = ''
		if product.catalog_id in id2product_catalog:
			product_catalog = id2product_catalog[product.catalog_id]
			father_id = product_catalog.father_id
			second_level_name = product_catalog.name
			first_level_name = '' if father_id not in id2product_catalog else id2product_catalog[father_id].name

		rows.append({
			'id': product.id,
			'role': role,
			'customer_name': '' if owner_id not in user_id2name else user_id2name[owner_id],
			'promotion_title': product.promotion_title,
			'clear_price': clear_price,
			'product_price': product_price,
			'limit_clear_price': '%.2f' % product.limit_clear_price if product.limit_clear_price > 0 else '',
			'product_weight': '%.2f' % product.product_weight,
			'product_name': product.product_name,
			'product_store': product_store,
			'store_short': store_short,
			'image_path': image_path,
			'image_paths': image_paths if image_paths else '',
			'remark': product.remark,
			'status': product_status2text[product.product_status] if product.id not in product_shelve_on else '已上架',
			'sales': '%s' % sales,
			'has_limit_time': valid_time,
			'product_has_model': product_has_model,
			'first_level_name': first_level_name,
			'second_level_name': second_level_name,
			'is_model': product.has_product_model,
			'is_update': product.is_update,
			'created_at': product.created_at.strftime('%Y-%m-%d %H:%M')
		})
	if is_export:
		return rows
	else:
		return rows, pageinfo


def update_product_store(product_2_weapp_product=None, products=None):
	"""
	从weapp拿到库存后更新panda库存
	"""
	weapp_product_ids = product_2_weapp_product.keys()
	params = {
		'product_ids': json.dumps(weapp_product_ids)
	}
	resp, resp_data = sync_util.sync_zeus(params=params, resource='mall.product', method='get')

	resp_products = resp_data.get('products')
	# 组装(panda商品idweapp规格名: 库存)
	panda_product_id_to_socks = {}
	for resp_product in resp_products:
		temp_models = resp_product.get('models')
		for temp_model in temp_models:
			panda_product_id = product_2_weapp_product.get(temp_model.get('product_id'))
			temp_model_name = temp_model.get('name')
			panda_product_id_to_socks.update({str(panda_product_id)+'#'+ temp_model_name: temp_model.get('stocks')})

	# panda_product_model_name_to_stocks = {}
	for product in products:
		model_properties = get_weapp_model_properties(product=product)
		if len(model_properties) == 0:
			# 单规格
			key = str(product.id) + '#standard'
			product_store = panda_product_id_to_socks.get(key)

			if product_store and int(product_store) != product.product_store:
				models.Product.objects.filter(id=product.id).update(product_store=panda_product_id_to_socks.get(key))
			continue
		for _property in model_properties:
			key = str(product.id) + '#' + _property.get('name')
			stocks = panda_product_id_to_socks.get(key)
			if stocks and stocks != product.product_store:
				models.ProductModel.objects.filter(id=_property.get('panda_model_info_id'))\
					.update(stocks=panda_product_id_to_socks.get(key))


def get_shelve_on_product(role=None, product_ids=None, products=None):
    """
    获取上架的商品
    """
    # 获取商品是否上线
    relations = models.ProductHasRelationWeapp.objects.filter(product_id__in=product_ids)
    product_2_weapp_product = {}
    for relation in relations:
        product_2_weapp_product.update({int(relation.weapp_product_id): relation.product_id})
    if role != YUN_YING:
        update_product_store(product_2_weapp_product=product_2_weapp_product, products=products)
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
        product_shelve_on = [product_2_weapp_product.get(int(product_statu.get('product_id')))
                             for product_statu in product_status
                             if product_statu.get('status') == 'on']
    return product_shelve_on
