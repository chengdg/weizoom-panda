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
import nav
import models

FIRST_NAV = 'product'
SECOND_NAV = 'product-list'	

filter2field ={
	'product_name_query': 'product_name',
	'customer_name_query': 'customer_name',
	'weapp_name_query': 'weapp_id'
}

class ProductRelation(resource.Resource):
	app = 'product'
	resource = 'product_relation'

	@login_required
	def get(request):
		"""
		显示商品列表
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV
		})
		
		return render_to_response('product/product_relation.html', c)

	def api_get(request):
		cur_page = request.GET.get('page', 1)
		role = UserProfile.objects.get(user_id=request.user.id).role
		user_profiles = UserProfile.objects.filter(role=1)#role{1:客户}
		products = models.Product.objects.all().order_by('-id')
		product_relations = models.ProductRelation.objects.all().order_by('self_user_name')
		product_has_relations = models.ProductHasRelationWeapp.objects.exclude(weapp_product_id='').order_by('self_user_name')
		filter_idct = dict([(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET if key.startswith('__f-')])
		product_name = filter_idct.get('product_name','')
		customer_name = filter_idct.get('customer_name','')
		weapp_id = filter_idct.get('weapp_id','')

		if product_name:
			products = products.filter(product_name__icontains=product_name)
		if customer_name:
			user_profiles = user_profiles.filter(name__icontains=customer_name)
			user_ids = [user_profile.user_id for user_profile in user_profiles]
			products = products.filter(owner_id__in=user_ids)
		if weapp_id:
			product_has_relationss = product_has_relations.filter(weapp_product_id__icontains=weapp_id)
			product_ids = [product_has_relation.product_id for product_has_relation in product_has_relationss]
			products = products.filter(id__in=product_ids)

		product_images = models.ProductImage.objects.all()
		user_id2name = {user_profile.user_id:user_profile.name for user_profile in user_profiles}
		
		self_shop = []
		self_user_name2self_first_name = {}
		for product in product_relations:
			self_shop.append({
				'self_user_name': product.self_user_name,
				'self_first_name': product.self_first_name
			})
			self_user_name2self_first_name[product.self_user_name] = product.self_first_name

		product_id2relations = {}
		for product_has_relation in product_has_relations:
			product_id = product_has_relation.product_id
			self_user_name = product_has_relation.self_user_name
			weapp_product_id = product_has_relation.weapp_product_id
			self_first_name = self_user_name2self_first_name[self_user_name] 
			if product_id not in product_id2relations:
				product_id2relations[product_id] = [{
					'self_first_name': self_first_name,
					'weapp_product_id': weapp_product_id 
				}]
			else:
				product_id2relations[product_id].append({
					'self_first_name': self_first_name,
					'weapp_product_id': weapp_product_id 
				})
		#组装数据
		rows = []
		pageinfo, products = paginator.paginate(products, cur_page, 10, query_string=request.META['QUERY_STRING'])

		product_ids = ''
		#构造panda数据库内商品id，与云商通内商品id的关系
		for product_has_relation in product_has_relations:
			weapp_product_ids = product_has_relation.weapp_product_id.split(';')
			for weapp_product_id in weapp_product_ids:
				product_ids = product_ids + '_' +weapp_product_id

		product_weapp_id2product_id = {}
		for product_has_relation in product_has_relations:
			weapp_product_ids = product_has_relation.weapp_product_id.split(';')
			for weapp_product_id in weapp_product_ids:
				#获得所有绑定过云商通的云商通商品id
				product_weapp_id2product_id[weapp_product_id] = product_has_relation.product_id
		#请求接口获得数据
		id2sales = {}
		try:
			params = {
				'product_ids': product_ids[1:]
			}
			r = requests.get(ZEUS_HOST+'/mall/product_sales/',params=params)
			res = json.loads(r.text)
			if res['code'] == 200:
				product_sales = res['data']['product_sales']
				if product_sales:
					for product_sale in product_sales:
						product_id = str(product_sale['product_id'])
						if product_id in product_weapp_id2product_id:
							p_id = product_weapp_id2product_id[product_id]
							p_sales = product_sale['sales']
							id2sales[p_id] = p_sales
			else:
				print(res)
		except Exception,e:
			print(e)

		for product in products:
			if product.owner_id in user_id2name:
				sales = 0 if product.id not in id2sales else id2sales[product.id]
				rows.append({
					'id': product.id,
					'role': role,
					'product_name': product.product_name,
					'customer_name': '' if product.owner_id not in user_id2name else user_id2name[product.owner_id],
					'total_sales': '%s' %sales,
					'weapp_name': product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
					'self_shop': json.dumps(self_shop),
					'relations': '' if product.id not in product_id2relations else json.dumps(product_id2relations[product.id])
				})
		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}

		#构造response
		response = create_response(200)
		response.data = data
		return response.get_response()