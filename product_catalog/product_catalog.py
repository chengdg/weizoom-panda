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

from util import string_util
from account import models as account_models
from product import models as product_models
from panda.settings import ZEUS_HOST
from util import db_util
import models as product_catalog_models
import nav
import requests

FIRST_NAV = 'product_catalog'
SECOND_NAV = 'product_catalog'
# COUNT_PER_PAGE = 10

class ProductCatalog(resource.Resource):
	app = 'product_catalog'
	resource = 'product_catalogs'

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
		return render_to_response('product_catalog/product_catalogs.html', c)

	def api_get(request):
		all_first_catalogs = product_catalog_models.ProductCatalog.objects.filter(level=1).order_by('-created_at')
		all_second_catalogs = product_catalog_models.ProductCatalog.objects.filter(level=2).order_by('-created_at')
		rows = []
		for catalog in all_first_catalogs:
			second_catalogs = []
			total_products_number = 0
			belong_second_catalogs = all_second_catalogs.filter(father_id=catalog.id)
			for belong_second_catalog in belong_second_catalogs:
				qualification_id2name = []
				products_number = product_models.Product.objects.filter(catalog_id=belong_second_catalog.id).count()
				total_products_number += products_number
				qualifications = product_catalog_models.ProductCatalogQualification.objects.filter(catalog_id=belong_second_catalog.id)
				for qualification in qualifications:
					qualification_id2name.append({
						'id': qualification.id,
						'name': qualification.name
						})
				second_catalogs.append({
					'id': belong_second_catalog.id,
					'father_catalog': belong_second_catalog.father_id,
					'catalog_name': belong_second_catalog.name,
					'note': belong_second_catalog.note,
					'created_at': belong_second_catalog.created_at.strftime("%Y-%m-%d %H:%M:%S"),
					'products_number': products_number,
					'qualification_id2name': json.dumps(qualification_id2name)
				})
			rows.append({
				'id': catalog.id,
				'father_catalog': catalog.father_id,
				'catalog_name': catalog.name,
				'note': catalog.note,
				'created_at': catalog.created_at.strftime("%Y-%m-%d %H:%M:%S"),
				'products_number': total_products_number,
				'second_catalogs': json.dumps(second_catalogs)
			})
		data = {
			'rows': rows
		}
		response = create_response(200)
		response.data = data
		return response.get_response()

	@login_required
	def api_put(request):
		# 新建商品分类
		post = request.POST
		name = post.get('catalog_name','')
		father_id = int(post.get('father_catalog',-1))
		level = 1 if father_id == -1 else 2
		note = post.get('note','')
		try:
			product_catalog_models.ProductCatalog.objects.create(
				name = name,
				level = level,
				father_id = father_id,
				note = note
			)
			response = create_response(200)
		except:
			response = create_response(500)
			response.errMsg = u'新建失败'
			response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	@login_required
	def api_post(request):
		# 编辑商品分类
		post = request.POST
		catalog_id = post.get('catalog_id','')
		name = post.get('catalog_name','')
		note = post.get('note','')
		try:
			product_catalog_models.ProductCatalog.objects.filter(id=catalog_id).update(
				name = name,
				note = note
			)
			response = create_response(200)
		except:
			response = create_response(500)
			response.errMsg = u'编辑失败'
			response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	@login_required
	def api_delete(request):
		catalog_id = request.POST.get('id','')
		try:
			catalog = product_catalog_models.ProductCatalog.objects.get(id=catalog_id)
			if catalog.father_id != -1:
				#二级分类
				if product_models.Product.objects.filter(catalog_id=catalog_id).count() > 0:
					response = create_response(500)
					response.errMsg = u'该分类正在被使用，请先将商品调整分类后再删除分类'
					return response.get_response()
				else:
					catalog.delete()
			else:
				if product_catalog_models.ProductCatalog.objects.filter(father_id=catalog.id).count() > 0:
					response = create_response(500)
					response.errMsg = u'该分类下还存在二级分类，请先删除二级分类'
					return response.get_response()
				else:
					customers = account_models.UserProfile.objects.filter(role=account_models.CUSTOMER).exclude(company_type='')
					using_catalog_ids = []
					for customer in customers:
						for company_type in json.loads(customer.company_type):
							if company_type not in using_catalog_ids:
								using_catalog_ids.append(company_type)
					print using_catalog_ids
					if int(catalog_id) in using_catalog_ids:
						response = create_response(500)
						response.errMsg = u'分类已被使用，删除失败，请先修改客户账户'
						return response.get_response()
					else:
						catalog.delete()
			response = create_response(200)
			return response.get_response()
		except Exception,e:
			print e
			response = create_response(500)
			response.errMsg = u'删除失败'
			return response.get_response()

class GetAllFirstCatalog(resource.Resource):
	app = 'product_catalog'
	resource = 'get_all_first_catalog'

	@login_required
	def api_get(request):
		is_account_page = request.GET.get('is_account_page','')
		catalogs = product_catalog_models.ProductCatalog.objects.filter(father_id=-1).order_by('-created_at')
		if is_account_page:
			rows = []
		else:
			rows = [{
				'text': u'无',
				'value': -1
			}]
		for catalog in catalogs:
			rows.append({
				'text': catalog.name,
				'value': catalog.id
			})
		data = {
			'rows': rows
		}
		response = create_response(200)
		response.data = data
		return response.get_response()

#配置特殊资质
class GetAllFirstCatalog(resource.Resource):
	app = 'product_catalog'
	resource = 'qualification'

	@login_required
	def api_put(request):
		# 新建/编辑特殊资质
		post = request.POST
		qualification_infos = json.loads(post.get('qualification_infos',''))
		catalog_id = int(post.get('catalog_id'))
		old_ids = [int(catalog.id) for catalog in product_catalog_models.ProductCatalogQualification.objects.filter(catalog_id=catalog_id)]
		new_ids = []
		need_del_ids = []

		#循环第一次，得到编辑后被删除的特殊资质id
		for qualification_info in qualification_infos:
			if qualification_info.has_key('id'):
				new_ids.append(qualification_info['id'])
		for old_id in old_ids:
			if old_id not in new_ids:
				need_del_ids.append(old_id)
		product_catalog_models.ProductCatalogQualification.objects.filter(id__in=need_del_ids).delete()
		
		# 循环第二次，更新特殊资质信息
		for qualification_info in qualification_infos:
			if qualification_info.has_key('id'):
				#编辑分类
				product_catalog_models.ProductCatalogQualification.objects.filter(id=qualification_info['id']).update(
					name = qualification_info['name']
					)
			else:
				#新增分类
				product_catalog_models.ProductCatalogQualification.objects.create(
					catalog_id = catalog_id,
					name = qualification_info['name']
				)
		response = create_response(200)
		return response.get_response()
