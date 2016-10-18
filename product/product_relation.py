# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from core import resource
from core.jsonresponse import create_response
from core import paginator

from util import db_util
from resource import models as resource_models
from account.models import *
from util import string_util
from panda.settings import ZEUS_HOST,PANDA_HOST
from panda.settings import CESHI_USERNAMES
from product.sales_from_weapp import sales_from_weapp
import nav
import models
import requests
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
from eaglet.utils.resource_client import Resource
from product_catalog import models as product_catalog_models
from label import models as label_models
from manager.manager_account import get_info_from_axe 

FIRST_NAV = 'product'
SECOND_NAV = 'product-relation-list'

filter2field ={
	'product_name_query': 'product_name',
	'customer_name_query': 'customer_name',
	'product_status_query': 'product_status',
	'catalog_query': 'catalog_name'
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
			'second_navs': nav.get_second_navs(request),
			'second_nav_name': SECOND_NAV,
			'first_catalog_id': request.GET.get('first_catalog_id', ''),
			'second_catalog_id': request.GET.get('second_catalog_id', '')
		})

		return render_to_response('product/product_relation.html', c)

	def api_get(request):
		is_export = False
		rows, pageinfo = getProductRelationData(request, is_export)

		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}

		#构造response
		response = create_response(200)
		response.data = data
		return response.get_response()

def getProductRelationData(request, is_export):
	cur_page = request.GET.get('page', 1)
	first_catalog_id = request.GET.get('first_catalog_id', '')
	second_catalog_id = request.GET.get('second_catalog_id', '')
	role = UserProfile.objects.get(user_id=request.user.id).role
	user_profiles = UserProfile.objects.filter(role=1, is_active=True)#role{1:客户}
	if first_catalog_id != '':
		catalog_ids = [catalog.id for catalog in product_catalog_models.ProductCatalog.objects.filter(father_id=int(first_catalog_id))]
		products = models.Product.objects.filter(catalog_id__in=catalog_ids, is_deleted=False).order_by('-id')
	elif second_catalog_id != '':
		products = models.Product.objects.filter(catalog_id=int(second_catalog_id), is_deleted=False).order_by('-id')
	else:
		products = models.Product.objects.filter(is_deleted=False).order_by('-id')
	filter_dict = dict([(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET if key.startswith('__f-')])
	product_name = filter_dict.get('product_name','')
	customer_name = filter_dict.get('customer_name','')
	product_status_value = filter_dict.get('product_status','0')
	catalog_name = filter_dict.get('catalog_name','')
	#查询
	if product_name:
		products = products.filter(product_name__icontains=product_name)
	if customer_name:
		user_profiles = user_profiles.filter(name__icontains=customer_name)
		user_ids = [user_profile.user_id for user_profile in user_profiles]
		products = products.filter(owner_id__in=user_ids)
	if catalog_name:
		product_catalogs = product_catalog_models.ProductCatalog.objects.filter(name__icontains=catalog_name)
		father_id2ids = {}
		for product_catalog in product_catalog_models.ProductCatalog.objects.all():
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
	if int(product_status_value)!=0:
		sync_weapp_accounts = models.ProductSyncWeappAccount.objects.all()
		has_sync_p_ids = set([sync_weapp_account.product_id for sync_weapp_account in sync_weapp_accounts])

		has_relation_weapps = models.ProductHasRelationWeapp.objects.all()
		has_relation_p_ids = set([has_relation_weapp.product_id for has_relation_weapp in has_relation_weapps])
		if int(product_status_value)==1:#已入库,已同步
			products = products.filter(id__in=has_sync_p_ids)

		if int(product_status_value)==3:#已入库,已停售
			products = products.filter(id__in=has_relation_p_ids)
			products = products.exclude(id__in=has_sync_p_ids)
			
		if int(product_status_value)==2:#待入库
			products = products.exclude(id__in=has_relation_p_ids)
			products = products.exclude(id__in=has_sync_p_ids)
			products = products.exclude(is_refused=True)

		if int(product_status_value)==4:#入库驳回
			all_reject_p_ids = [product.id for product in products.filter(is_refused=True)] #所有驳回状态的id
			print 'all_reject_p_ids'
			print all_reject_p_ids
			all_has_reject_p_ids = [reject_log.product_id for reject_log in models.ProductRejectLogs.objects.filter(id__in=all_reject_p_ids)] #是入库驳回的商品id
			print 'all_has_reject_p_ids'
			print all_has_reject_p_ids
			products = products.filter(id__in=all_has_reject_p_ids)
			print 'products--------------------------'
			print products
		if int(product_status_value)==5:#修改驳回
			products = products.filter(id__in=has_sync_p_ids)
			sync_reject_p_ids = [product.id for product in products.filter(is_refused=True)] #所有驳回状态的id
			products = products.filter(id__in=sync_reject_p_ids)

	if not is_export:
		pageinfo, products = paginator.paginate(products, cur_page, 10, query_string=request.META['QUERY_STRING'])
	p_ids = [product.id for product in products]
	p_has_relations = models.ProductHasRelationWeapp.objects.filter(product_id__in=p_ids).exclude(weapp_product_id='')

	sync_weapp_accounts = models.ProductSyncWeappAccount.objects.filter(product_id__in=p_ids)
	weapp_relations = models.ProductHasRelationWeapp.objects.filter(product_id__in=p_ids)
	has_relation_p_ids = set([sync_weapp_account.product_id for sync_weapp_account in sync_weapp_accounts])
	weapp_relation_ids = [p.product_id for p in weapp_relations]
	has_reject_p_ids = [reject_log.product_id for reject_log in models.ProductRejectLogs.objects.filter(product_id__in=p_ids)]

	#从weapp获取销量sales_from_weapp
	id2sales = sales_from_weapp(p_has_relations)

	#获取标签
	property_ids = []
	catalog_ids = [product.catalog_id for product in products]
	product_catalog_has_labels = product_catalog_models.ProductCatalogHasLabel.objects.filter(catalog_id__in=catalog_ids)
	product_has_labels = models.ProductHasLabel.objects.filter(product_id__in=p_ids)
	
	catalog_property_ids = [product_catalog_has_label.property_id for product_catalog_has_label in product_catalog_has_labels]
	product_property_ids = [product_has_label.property_id for product_has_label in product_has_labels]
	property_ids.extend(catalog_property_ids)
	property_ids.extend(product_property_ids)
	label_group_values = label_models.LabelGroupValue.objects.filter(property_id__in=property_ids, is_deleted=False)
	value_id2name = {label_property_value.id:label_property_value.name for label_property_value in label_group_values}
		
	#分类配置的标签
	catalog_id2names = {}
	for product_catalog_has_label in product_catalog_has_labels:
		label_ids = product_catalog_has_label.label_ids.split(',')
		property_id = product_catalog_has_label.property_id
		catalog_id = product_catalog_has_label.catalog_id
		names = []
		for label_id in label_ids:
			if label_id and int(label_id) in value_id2name:
				names.append(value_id2name[int(label_id)])

		if catalog_id not in catalog_id2names:
			catalog_id2names[catalog_id] = names
		else:
			catalog_id2names[catalog_id].extend(names)

	#商品配置的标签 展示商品配置优先
	product_id2label_names = {}
	for product_has_label in product_has_labels:
		label_ids = product_has_label.label_ids.split(',')
		property_id = product_has_label.property_id
		label_product_id = product_has_label.product_id
		lanel_names = []
		for label_id in label_ids:
			if label_id and int(label_id) in value_id2name:
				lanel_names.append(value_id2name[int(label_id)])

		if label_product_id not in product_id2label_names:
			product_id2label_names[label_product_id] = lanel_names
		else:
			product_id2label_names[label_product_id].extend(lanel_names)

	#获取分类
	product_catalogs = product_catalog_models.ProductCatalog.objects.all()
	id2product_catalog = {product_catalog.id:product_catalog for product_catalog in product_catalogs}

	p_owner_ids = [product.owner_id for product in products]
	user_profiles = user_profiles.filter(user_id__in=p_owner_ids)
	user_id2name = {user_profile.user_id:user_profile.name for user_profile in user_profiles}
	# user_id2account_id = {user_profile.user_id:user_profile.id for user_profile in user_profiles}

	#获取下架商品的原因
	product_revoke_logs = models.ProductRevokeLogs.objects.filter(product_id__in=p_ids)
	#只取最后一次下架原因
	product_id2revoke_reasons = {revoke_log.product_id:revoke_log.revoke_reasons for revoke_log in product_revoke_logs}

	#从渠道接口获得客户来源字段
	company_name2info = {}
	company_names = []
	for user_profile in user_profiles:
		if user_profile.company_name != '':
			company_names.append(user_profile.company_name)
	company_names = '_'.join(company_names)
	company_name2info = get_info_from_axe(company_names)

	#组装数据
	rows = []
	for product in products:
		owner_id = product.owner_id
		catalog_id = product.catalog_id
		if owner_id in user_id2name:
			sales = 0 if product.id not in id2sales else id2sales[product.id]
			product_status_text = u'待入库'
			product_status_value = 0
			if product.id in has_relation_p_ids:
				product_status_text = u'已入库，已同步'
				product_status_value = 1
				if product.is_refused:
					product_status_text = u'修改驳回'
					product_status_value = 4
			elif product.id not in has_relation_p_ids and product.id in weapp_relation_ids:
				product_status_text = u'已入库，已停售'
				product_status_value = 2
			elif product.id in has_reject_p_ids and product_status_value == 0 and product.is_refused:
				product_status_text = u'入库驳回'
				product_status_value = 3
			#商品分类
			first_level_name = ''
			second_level_name = ''
			if catalog_id in id2product_catalog:
				product_catalog = id2product_catalog[catalog_id]
				father_id = product_catalog.father_id
				second_level_name = product_catalog.name
				first_level_name = '' if father_id not in id2product_catalog else id2product_catalog[father_id].name

			#标签
			if product.id not in product_id2label_names:
				property_value_names = [] if catalog_id not in catalog_id2names else catalog_id2names[catalog_id]
			else:
				property_value_names = [] if product.id not in product_id2label_names else product_id2label_names[product.id]
			
			#组织成json格式
			label_names = []
			for property_value_name in property_value_names:
				label_names.append({
					'name': property_value_name
				})


			customer_from_text = '--' 
			#客户来源
			account = user_profiles.get(user_id=owner_id)
			if company_name2info.has_key(account.company_name):
				customer_from_text = company_name2info[account.company_name]
			else:
				customer_from_text = '渠道' if account.customer_from == 1 else '--' #如果从渠道没有找到匹配的，给默认值

			#下架原因
			revoke_reasons = '' if product.id not in product_id2revoke_reasons else product_id2revoke_reasons[product.id]
			
			rows.append({
				'id': product.id,
				'role': role,
				'owner_id': owner_id,
				'catalogId': catalog_id,
				'product_name': product.product_name,
				'customer_name': '' if owner_id not in user_id2name else user_id2name[owner_id],
				'total_sales': '%s' %sales,
				'product_status': product_status_text,
				'product_status_value': product_status_value,
				'first_level_name': first_level_name,
				'second_level_name': second_level_name,
				'is_update': product.is_update,
				'customer_from_text': customer_from_text,
				'revoke_reasons': revoke_reasons,
				'labelNames': [] if not label_names else json.dumps(label_names)
			})
	if is_export:
		return rows
	else:
		return rows, pageinfo