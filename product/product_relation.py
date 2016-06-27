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
from panda.settings import PANDA_HOST
from product.sales_from_weapp import sales_from_weapp
import nav
import models
import requests
import sys,os

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
		product_images = models.ProductImage.objects.all().order_by('-id')
		account_has_suppliers = AccountHasSupplier.objects.all()
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

		self_shop = []
		self_user_name2self_first_name = {}
		for product in product_relations:
			self_shop.append({
				'self_user_name': product.self_user_name,
				'self_first_name': product.self_first_name
			})
			self_user_name2self_first_name[product.self_user_name] = product.self_first_name

		product_id2relations = {}
		product_id2self_user_name = {}
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

			if product_id not in product_id2self_user_name:
				product_id2self_user_name[product_id] = [self_user_name]
			else:
				product_id2self_user_name[product_id].append(self_user_name)

		#获取商品图片
		product_id2image_id = {}
		image_id2images = {}
		for product in product_images:
			if product.product_id not in product_id2image_id:
				product_id2image_id[product.product_id] = [product.image_id]
			else:
				product_id2image_id[product.product_id].append(product.image_id)
		for image in resource_models.Image.objects.all():
			image_id2images[image.id] = image.path
		
		pageinfo, products = paginator.paginate(products, cur_page, 10, query_string=request.META['QUERY_STRING'])
		#从weapp获取销量
		p_ids = [product.id for product in products]
		product_has_relations = product_has_relations.filter(product_id__in=p_ids)
		id2sales = sales_from_weapp(product_has_relations)
		
		p_owner_ids = [product.owner_id for product in products]
		user_profiles = user_profiles.filter(user_id__in=p_owner_ids)
		user_id2name = {user_profile.user_id:user_profile.name for user_profile in user_profiles}
		user_id2account_id = {user_profile.user_id:user_profile.id for user_profile in user_profiles}
		account_ids = [user_profile.id for user_profile in user_profiles]
		account_has_suppliers = account_has_suppliers.filter(account_id__in=account_ids)
		# account_id2supplier_ids = {}
		# account_id2user_ids = {}
		# for account_has_supplier in account_has_suppliers:
		# 	account_id = account_has_supplier.account_id
		# 	supplier_id = str(account_has_supplier.supplier_id)
		# 	user_id = str(account_has_supplier.user_id)
		# 	if account_id not in account_id2supplier_ids:
		# 		account_id2supplier_ids[account_id] = [supplier_id]
		# 	else:
		# 		account_id2supplier_ids[account_id].append(supplier_id)

		# 	if account_id not in account_id2user_ids:
		# 		account_id2user_ids[account_id] = [user_id]
		# 	else:
		# 		account_id2user_ids[account_id].append(user_id)
		# print  account_id2user_ids,"============="
		#组装数据
		rows = []
		for product in products:
			owner_id = product.owner_id
			if owner_id in user_id2name:
				image_ids = -1 if product.id not in product_id2image_id else product_id2image_id[product.id]
				image_path = []
				for image_id in image_ids:
					if image_id in image_id2images:
						img_path = image_id2images[image_id]
						if 'http' not in image_id2images[image_id]:
							img_path = PANDA_HOST + image_id2images[image_id]
						image_path.append(img_path)
				sales = 0 if product.id not in id2sales else id2sales[product.id]
				self_user_name = [] if product.id not in product_id2self_user_name else product_id2self_user_name[product.id]
				account_id = -1 if owner_id not in user_id2account_id else user_id2account_id[owner_id]
				# supplier_ids = [] if account_id not in account_id2supplier_ids else account_id2supplier_ids[account_id]
				# user_ids = [] if account_id not in account_id2user_ids else account_id2user_ids[account_id]
				product_info = {
					# 'owner_id': '_'.join(user_ids),#所属账号的user id
					'account_id': account_id,
					'product_id': product.id,
					# 'supplier_ids': '_'.join(supplier_ids),#供货商 id
					'product_name': product.product_name,
					'promotion_title': product.promotion_title if product.promotion_title else '',
					'clear_price': '%s' %product.clear_price,
					'product_price': '%s' %product.product_price,
					'product_weight': '%s' %product.product_weight,
					'product_store': '%s' %product.product_store,
					'remark': '%s' %product.remark,
					'image_path': ','.join(image_path)
				}
				rows.append({
					'id': product.id,
					'role': role,
					'owner_id': owner_id,
					'product_name': product.product_name,
					'customer_name': '' if owner_id not in user_id2name else user_id2name[owner_id],
					'total_sales': '%s' %sales,
					'weapp_name': product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
					'self_user_name': self_user_name,
					'self_shop': json.dumps(self_shop),
					'product_info': product_info,
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