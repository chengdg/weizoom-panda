# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from core import resource
from core.jsonresponse import create_response
from core import paginator

from util import db_util
from resource import models as resource_models
from account.models import *
from util import string_util
from panda.settings import ZEUS_HOST
from product.sales_from_weapp import sales_from_weapp
import nav
import models
import requests

FIRST_NAV = 'product'
SECOND_NAV = 'product-list'

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
		cur_page = request.GET.get('page', 1)
		role = UserProfile.objects.get(user_id=request.user.id).role
		products = models.Product.objects.filter(owner=request.user).order_by('-id')
		product_images = models.ProductImage.objects.all().order_by('-id')
		product_ids = ['%s'%product.id for product in products]
		product_has_relations = models.ProductHasRelationWeapp.objects.filter(product_id__in=product_ids).exclude(weapp_product_id='')

		id2sales = sales_from_weapp(product_has_relations)
		# product_ids = ''
		# #构造panda数据库内商品id，与云商通内商品id的关系
		# for product_has_relation in product_has_relations:
		# 	weapp_product_ids = product_has_relation.weapp_product_id.split(';')
		# 	for weapp_product_id in weapp_product_ids:
		# 		product_ids = product_ids + '_' +weapp_product_id

		# product_weapp_id2product_id = {}
		# for product_has_relation in product_has_relations:
		# 	weapp_product_ids = product_has_relation.weapp_product_id.split(';')
		# 	for weapp_product_id in weapp_product_ids:
		# 		#获得所有绑定过云商通的云商通商品id
		# 		product_weapp_id2product_id[weapp_product_id] = product_has_relation.product_id
		# #请求接口获得数据
		# id2sales = {}
		# try:
		# 	params = {
		# 		'product_ids': product_ids[1:]
		# 	}
		# 	r = requests.get(ZEUS_HOST+'/mall/product_sales/',params=params)
		# 	res = json.loads(r.text)
		# 	if res['code'] == 200:
		# 		product_sales = res['data']['product_sales']
		# 		if product_sales:
		# 			for product_sale in product_sales:
		# 				product_id = str(product_sale['product_id'])
		# 				if product_id in product_weapp_id2product_id:
		# 					p_id = product_weapp_id2product_id[product_id]
		# 					p_sales = product_sale['sales']
		# 					if p_id not in id2sales:
		# 						id2sales[p_id] = p_sales
		# 					else:
		# 						id2sales[p_id] += p_sales
		# 	else:
		# 		print(res)
		# except Exception,e:
		# 	print(e)

		#获取商品图片
		product_id2image_id = {}
		image_id2images = {}
		for product in product_images:
			product_id2image_id[product.product_id] = product.image_id
		for image in resource_models.Image.objects.all():
			image_id2images[image.id] = image.path

		pageinfo, products = paginator.paginate(products, cur_page, 5, query_string=request.META['QUERY_STRING'])
		#组装数据
		rows = []
		for product in products:
			image_id = -1 if product.id not in product_id2image_id else product_id2image_id[product.id]
			image_path = '' if image_id not in image_id2images else image_id2images[image_id]
			sales = 0 if product.id not in id2sales else id2sales[product.id]
			rows.append({
				'id': product.id,
				'role': role,
				'promotion_title': product.promotion_title,
				'clear_price': '%.2f' %product.clear_price,
				'product_name': product.product_name,
				'image_path': image_path,
				'status': product_status2text[product.product_status],
				'sales': '%s' %sales,
				'created_at': product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
			})
		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}

		#构造response
		response = create_response(200)
		response.data = data
		return response.get_response()