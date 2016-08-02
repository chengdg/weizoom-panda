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
from core.exceptionutil import unicode_full_stack
from core import paginator
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog

from util import db_util
from resource import models as resource_models
from account.models import *
from util import string_util
from panda.settings import ZEUS_HOST
from product.sales_from_weapp import sales_from_weapp
import nav
import models
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST

FIRST_NAV = 'product'
SECOND_NAV = 'product-model'


class ProductModel(resource.Resource):
	app = 'product'
	resource = 'product_model'

	@login_required
	def get(request):
		"""
		显示商品列表
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
		})

		return render_to_response('product/product_model.html', c)

	def api_get(request):
		cur_page = request.GET.get('page', 1)
		role = UserProfile.objects.get(user_id=request.user.id).role
		if role == YUN_YING:
			product_model_properties = models.ProductModelProperty.objects.filter(is_deleted=False)
		else:
			product_model_properties = models.ProductModelProperty.objects.filter(owner=request.user,
																				  is_deleted=False)
		pageinfo, product_model_properties = paginator.paginate(product_model_properties, cur_page, 20,
																query_string=request.META['QUERY_STRING'])
		property_ids = [product_model_property.id for product_model_property in product_model_properties]
		product_model_property_values = models.ProductModelPropertyValue.objects.filter(property_id__in=property_ids)
		product_models = models.ProductModel.objects.filter(owner=request.user)
		# 获取用户使用的规格
		model_ids = []
		for product_model in product_models:
			modelIds = product_model.name.split('_');
			for modelId in modelIds:
				index = modelId.find(":")
				model_ids.append(str(modelId[:index]))
		model_ids = set(model_ids)

		property_id2model_property_value = {}
		for model_property_value in product_model_property_values:
			if model_property_value.property_id not in property_id2model_property_value:
				property_id2model_property_value[model_property_value.property_id] = [{
					'name': model_property_value.name,
					'pic_url': model_property_value.pic_url,
					'id': model_property_value.id
				}]
			else:
				property_id2model_property_value[model_property_value.property_id].append({
					'name': model_property_value.name,
					'pic_url': model_property_value.pic_url,
					'id': model_property_value.id
				})

		rows = []
		for product_model_property in product_model_properties:
			model_name = ''
			if product_model_property.id in property_id2model_property_value:
				model_name = property_id2model_property_value[product_model_property.id]
			rows.append({
				'id': product_model_property.id,
				'model_ids': ','.join(model_ids),
				'product_model_name': product_model_property.name,
				'model_type': product_model_property.type,
				'model_name': '' if not model_name else json.dumps(model_name),
			})

		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}

		# 构造response
		response = create_response(200)
		response.data = data
		return response.get_response()

	def api_put(request):
		db_model = None
		try:
			db_model = models.ProductModelProperty.objects.create(
				owner=request.user
			)

			# type =
			type = 'text' if db_model.type == models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT else 'image'
			params = {
				"owner_id": "owner_id",
				'type': type,
				'name': db_model.name
			}
			resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put({
				'resource': 'mall.product_model_property',
				'data': params
			})
			# print resp.get('code'), '+++++++++++++++++++++++++++++++'
			if resp and resp.get('code') == 200 and resp.get('data').get('product_model'):
				# 新增中间关系
				weapp_property_id = resp.get('data').get('product_model').get('id')
				models.ProductModelPropertyRelation.objects.create(weapp_property_id=weapp_property_id,
																   model_property_id=db_model.id)
				response = create_response(200)

			else:
				db_model.update(is_deleted=False)
				response = create_response(500)
			return response.get_response()
		except:
			response = create_response(500)
			msg = unicode_full_stack()
			watchdog.error(msg)
			response.innerErrMsg = msg
			if db_model:
				db_model.update(is_deleted=False)
			return response.get_response()

	def api_post(request):
		model_id = int(request.POST.get('id', 0))
		name = request.POST.get('name', '')
		model_type = request.POST.get('model_type', 0)
		model_type_id = int(request.POST.get('model_id', 0))
		try:
			if model_id != 0 and model_type_id == 0:
				models.ProductModelProperty.objects.filter(id=model_id).update(
					name=name
				)
			if model_type_id != 0 and model_id == 0:
				models.ProductModelProperty.objects.filter(id=model_type_id).update(
					type=int(model_type)
				)
			response = create_response(200)
			# 调用zeus接口
			db_model_id = model_type_id if model_type_id != 0 else model_id
			db_model = models.ProductModelProperty.objects.filter(id=db_model_id).first()
			if not db_model:
				response = create_response(500)
				return response.get_response()

			relation = models.ProductModelPropertyRelation.objects.filter(model_property_id=db_model.id).first()
			model_type = 'text' if db_model.type == models.PRODUCT_MODEL_PROPERTY_TYPE_TEXT else 'image'
			if relation:
				# update
				# print 'update'
				params = {
					"id": relation.weapp_property_id,
					'type': model_type,
					'name': db_model.name
				}
				resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post({
					'resource': 'mall.product_model_property',
					'data': params
				})
				if not resp or not resp.get('code') == 200 and resp.get('data').get('change_rows') >= 0:
					# 新增中间关系

					db_model.update(is_deleted=False)
					response = create_response(500)
			else:
				# add
				# print 'add'
				params = {
					"owner_id": 'owner_id',
					'type': model_type,
					'name': db_model.name
				}
				resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put({
					'resource': 'mall.product_model_property',
					'data': params
				})
				if resp and resp.get('code') == 200:
					weapp_property_id = resp.get('data').get('product_model').get('id')
					models.ProductModelPropertyRelation.objects.create(weapp_property_id=weapp_property_id,
																	   model_property_id=db_model.id)
				else:
					response = create_response(500)

		except:
			response = create_response(500)
			msg = unicode_full_stack()
			watchdog.error(msg)
			response.innerErrMsg = msg
		return response.get_response()

	def api_delete(request):
		model_id = request.POST.get('model_id', 0)
		response = create_response(500)
		try:
			if model_id != 0:
				models.ProductModelProperty.objects.filter(id=model_id).update(is_deleted=True)
				models.ProductModelPropertyValue.objects.filter(property_id=model_id).update(is_deleted=True)
				has_properrty_values = models.ProductModelHasPropertyValue.objects.filter(property_id=model_id)
				model_ids = [has_properrty_value.model_id for has_properrty_value in has_properrty_values]
				product_models = models.ProductModel.objects.filter(id__in=model_ids)
				product_ids = [product_model.product_id for product_model in product_models]
				product_models.update(
					stocks= 0,
					price= 0,
					market_price= 0,
					weight= 0,
					limit_clear_price= 0,
					is_deleted=True
				)
				models.Product.objects.filter(id__in=product_ids).update(
					product_price= 0,
					clear_price= 0,
					product_store= 0,
					product_weight= 0
				)
				has_properrty_values.delete()
				response = create_response(200)
				# 调用zeus接口
				db_model = models.ProductModelPropertyRelation.objects.filter(model_property_id=model_id).first()
				if db_model:
					params = {
						"id": db_model.weapp_property_id,
					}
					resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).delete({
						'resource': 'mall.product_model_property',
						'data': params
					})
					if not resp or resp.get('code') != 200:
						response = create_response(500)
		except:
			msg = unicode_full_stack()
			watchdog.error(msg)
			response.innerErrMsg = msg
		return response.get_response()
