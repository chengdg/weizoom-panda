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

product_filter2field = {
	'product_name_query': 'product_name'
}

user_filter2field = {
	'customer_name_query': 'name'
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
		product_relations = models.ProductRelation.objects.all()
		product_has_relations = models.ProductHasRelationWeapp.objects.all()

		products = db_util.filter_query_set(products, request, product_filter2field)
		user_profiles = db_util.filter_query_set(user_profiles, request, user_filter2field)

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
		for product in products:
			rows.append({
				'id': product.id,
				'role': role,
				'product_name': product.product_name,
				'customer_name': '' if product.owner_id not in user_id2name else user_id2name[product.owner_id],
				'total_sales': '0',
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
