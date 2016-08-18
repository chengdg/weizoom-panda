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
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
from eaglet.utils.resource_client import Resource
from product_catalog import models as product_catalog_models

second_navs = [{
	'name': 'product-list',
	'displayName': '商品',
	'href': '/product/product_relation/'
}]
FIRST_NAV = 'product'
SECOND_NAV = 'product-list'

filter2field ={
	'product_name_query': 'product_name',
	'customer_name_query': 'customer_name',
	'product_status_query': 'product_status'
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
			'second_navs': second_navs,
			'second_nav_name': SECOND_NAV,
			'first_catalog_id': request.GET.get('first_catalog_id', ''),
			'second_catalog_id': request.GET.get('second_catalog_id', '')
		})

		return render_to_response('product/product_relation.html', c)

	def api_get(request):
		cur_page = request.GET.get('page', 1)
		first_catalog_id = request.GET.get('first_catalog_id', '')
		second_catalog_id = request.GET.get('second_catalog_id', '')
		role = UserProfile.objects.get(user_id=request.user.id).role
		user_profiles = UserProfile.objects.filter(role=1)#role{1:客户}
		if first_catalog_id != '':
			catalog_ids = [catalog.id for catalog in product_catalog_models.ProductCatalog.objects.filter(father_id=int(first_catalog_id))]
			products = models.Product.objects.filter(catalog_id__in=catalog_ids,is_deleted=False).order_by('-id')
		elif second_catalog_id != '':
			products = models.Product.objects.filter(catalog_id=int(second_catalog_id),is_deleted=False).order_by('-id')
		else:
			products = models.Product.objects.filter(is_deleted=False).order_by('-id')
		product_relations = models.ProductRelation.objects.all().order_by('self_user_name')
		product_images = models.ProductImage.objects.all().order_by('id')
		product_has_relations = models.ProductHasRelationWeapp.objects.exclude(weapp_product_id='').order_by('self_user_name')
		filter_idct = dict([(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET if key.startswith('__f-')])
		product_name = filter_idct.get('product_name','')
		customer_name = filter_idct.get('customer_name','')
		product_status_value = filter_idct.get('product_status','0')
		#查询
		if product_name:
			products = products.filter(product_name__icontains=product_name)
		if customer_name:
			user_profiles = user_profiles.filter(name__icontains=customer_name)
			user_ids = [user_profile.user_id for user_profile in user_profiles]
			products = products.filter(owner_id__in=user_ids)
		if int(product_status_value)!=0:
			sync_weapp_accounts = models.ProductSyncWeappAccount.objects.all()
			has_relation_p_ids = set([sync_weapp_account.product_id for sync_weapp_account in sync_weapp_accounts])
			if int(product_status_value)==1:
				products = products.filter(id__in=has_relation_p_ids)
			if int(product_status_value)==2:
				products = products.exclude(id__in=has_relation_p_ids)

		pageinfo, products = paginator.paginate(products, cur_page, 10, query_string=request.META['QUERY_STRING'])
		p_ids = [product.id for product in products]
		p_has_relations = models.ProductHasRelationWeapp.objects.filter(product_id__in=p_ids).exclude(weapp_product_id='')

		sync_weapp_accounts = models.ProductSyncWeappAccount.objects.filter(product_id__in=p_ids)
		has_relation_p_ids = set([sync_weapp_account.product_id for sync_weapp_account in sync_weapp_accounts])

		#从weapp获取销量sales_from_weapp
		id2sales = sales_from_weapp(p_has_relations)

		#获取分类
		product_catalogs = product_catalog_models.ProductCatalog.objects.all()
		id2product_catalog = {product_catalog.id:product_catalog for product_catalog in product_catalogs}

		p_owner_ids = [product.owner_id for product in products]
		user_profiles = user_profiles.filter(user_id__in=p_owner_ids)
		user_id2name = {user_profile.user_id:user_profile.name for user_profile in user_profiles}
		user_id2account_id = {user_profile.user_id:user_profile.id for user_profile in user_profiles}

		#组装数据
		rows = []
		for product in products:
			owner_id = product.owner_id
			if owner_id in user_id2name:
				sales = 0 if product.id not in id2sales else id2sales[product.id]
				product_status_text = u'未同步'
				if product.id in has_relation_p_ids:
					product_status_text = u'已同步'

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
					'owner_id': owner_id,
					'product_name': product.product_name,
					'customer_name': '' if owner_id not in user_id2name else user_id2name[owner_id],
					'total_sales': '%s' %sales,
					'product_status': product_status_text,
					'first_level_name': first_level_name,
					'second_level_name': second_level_name,
					'cur_page': pageinfo.cur_page
				})
		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}

		#构造response
		response = create_response(200)
		response.data = data
		return response.get_response()