# -*- coding: utf-8 -*-
import json

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog

from core import resource
from core.jsonresponse import create_response

from account import models as account_models
from product import models as product_models
from panda.settings import EAGLET_CLIENT_ZEUS_HOST, ZEUS_SERVICE_NAME

import models as product_catalog_models
import nav

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
		product_catalog_has_labels = product_catalog_models.ProductCatalogHasLabel.objects.all()
		catalog_ids = [product_catalog_has_label.catalog_id for product_catalog_has_label in product_catalog_has_labels]
		rows = []
		for catalog in all_first_catalogs:
			second_catalogs = []
			total_products_number = 0
			belong_second_catalogs = all_second_catalogs.filter(father_id=catalog.id)
			for belong_second_catalog in belong_second_catalogs:
				qualification_id2name = []
				index = 0
				products_number = product_models.Product.objects.filter(catalog_id=belong_second_catalog.id, is_deleted=False).count()
				total_products_number += products_number
				qualifications = product_catalog_models.ProductCatalogQualification.objects.filter(catalog_id=belong_second_catalog.id)
				for qualification in qualifications:
					qualification_id2name.append({
						'index': index,
						'id': qualification.id,
						'name': qualification.name
						})
					index += 1 
				second_catalogs.append({
					'id': belong_second_catalog.id,
					'fatherCatalog': belong_second_catalog.father_id,
					'catalogName': belong_second_catalog.name,
					'note': belong_second_catalog.note,
					'createdAt': belong_second_catalog.created_at.strftime("%Y-%m-%d %H:%M:%S"),
					'productsNumber': products_number,
					'qualificationId2name': json.dumps(qualification_id2name),
					'has_label': False if belong_second_catalog.id not in catalog_ids else True
				})
			rows.append({
				'id': catalog.id,
				'fatherCatalog': catalog.father_id,
				'catalogName': catalog.name,
				'note': catalog.note,
				'createdAt': catalog.created_at.strftime("%Y-%m-%d %H:%M:%S"),
				'productsNumber': total_products_number,
				'secondCatalogs': json.dumps(second_catalogs)
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
			product_catalog = product_catalog_models.ProductCatalog.objects.create(
				name = name,
				level = level,
				father_id = father_id,
				note = note
			)
			#
			weapp_father_id = father_id
			if father_id > 0:
				relation = product_catalog_models.ProductCatalogRelation.objects.filter(catalog_id=father_id).first()
				if relation:
					weapp_father_id = relation.weapp_catalog_id

			params = {
				'name': name,
				'level': level,
				'father_id': 0 if father_id == -1 else weapp_father_id
			}
			resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put(
				{
					'resource': 'mall.classification',
					'data': params
				}
			)
			if resp and resp.get('code') == 200 and resp.get('data').get('classification'):
				product_catalog_models.ProductCatalogRelation\
					.objects.create(catalog_id=product_catalog.id,
									weapp_catalog_id=resp.get('data').get('classification').get('id'))
				response = create_response(200)
			else:
				product_catalog_models.ProductCatalog.objects.filter(id=product_catalog.id).delete()
				response = create_response(500)
		except:
			response = create_response(500)
			response.errMsg = u'新建失败'
			response.innerErrMsg = unicode_full_stack()
			watchdog.error(unicode_full_stack())
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
			relation = product_catalog_models.ProductCatalogRelation.objects.filter(catalog_id=catalog_id)
			if relation:
				relation = relation.first()
				weapp_catalog_id = relation.weapp_catalog_id
				params = {
					'id': weapp_catalog_id,
					'name': name
				}
				resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post(
					{
						'resource': 'mall.classification',
						'data': params
					}
				)
				if resp and resp.get('code') == 200:
					response = create_response(200)
				else:
					response = create_response(500)
					response.errMsg = u'编辑失败'
			else:
				response = create_response(200)
			return response.get_response()
		except:
			response = create_response(500)
			response.errMsg = u'编辑失败'
			response.innerErrMsg = unicode_full_stack()
			watchdog.error(unicode_full_stack())
			return response.get_response()

	@login_required
	def api_delete(request):
		catalog_id = request.POST.get('id','')
		try:
			relation = product_catalog_models.ProductCatalogRelation.objects.filter(catalog_id=catalog_id).first()
			catalog = product_catalog_models.ProductCatalog.objects.get(id=catalog_id)
			if catalog.father_id != -1:
				#二级分类
				if product_models.Product.objects.filter(catalog_id=catalog_id, is_deleted=False).count() > 0:
					response = create_response(500)
					response.errMsg = u'该分类正在被使用，请先将商品调整分类后再删除分类'
					return response.get_response()
				else:
					if relation:
						params = {
							'id': relation.weapp_catalog_id
						}
						resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).delete(
							{
								'resource': 'mall.classification',
								'data': params
							}
						)
						if resp and resp.get('code') == 200 and resp.get('data').get('change_rows') > -1:
							catalog.delete()
					else:
						catalog.delete()
			else:
				if product_catalog_models.ProductCatalog.objects.filter(father_id=catalog.id).count() > 0:
					response = create_response(500)
					response.errMsg = u'该分类下还存在二级分类，请先删除二级分类'
					return response.get_response()
				else:
					customers = account_models.UserProfile.objects.filter(role=account_models.CUSTOMER, is_active=True).exclude(company_type='')
					using_catalog_ids = []
					for customer in customers:
						for company_type in json.loads(customer.company_type):
							if company_type not in using_catalog_ids:
								using_catalog_ids.append(company_type)
					if int(catalog_id) in using_catalog_ids:
						response = create_response(500)
						response.errMsg = u'分类已被使用，删除失败，请先修改客户账户'
						return response.get_response()
					else:
						if relation:
							params = {
								'id': relation.weapp_catalog_id
							}
							resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).delete(
								{
									'resource': 'mall.classification',
									'data': params
								}
							)
							if resp and resp.get('code') == 200 and resp.get('data').get('change_rows') > -1:
								catalog.delete()
						else:
							catalog.delete()
			response = create_response(200)
			return response.get_response()
		except:
			msg = unicode_full_stack()
			watchdog.error(msg)
			response = create_response(500)
			response.errMsg = u'删除失败'
			return response.get_response()