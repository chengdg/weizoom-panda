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
		product_model_properties = models.ProductModelProperty.objects.filter(owner=request.user)
		pageinfo, product_model_properties = paginator.paginate(product_model_properties, cur_page, 20, query_string=request.META['QUERY_STRING'])
		property_ids = [product_model_property.id for product_model_property in product_model_properties]
		product_model_property_values = models.ProductModelPropertyValue.objects.filter(property_id__in=property_ids)
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
				'product_model_name': product_model_property.name,
				'model_type': product_model_property.type,
				'model_name': '' if not model_name else json.dumps(model_name),
			})
		
		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}

		#构造response
		response = create_response(200)
		response.data = data
		return response.get_response()

	def api_put(request):
		try:
			models.ProductModelProperty.objects.create(
				owner = request.user
			)
			response = create_response(200)
		except:
			response = create_response(500)
			response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	def api_post(request):
		model_id = int(request.POST.get('id',0))
		name = request.POST.get('name','')
		model_type = request.POST.get('model_type',0)
		model_type_id = int(request.POST.get('model_id',0))
		try:
			if model_id!=0 and model_type_id==0:
				models.ProductModelProperty.objects.filter(id=model_id).update(
					name = name
				)
			if model_type_id!=0 and model_id==0:
				models.ProductModelProperty.objects.filter(id=model_type_id).update(
					type = int(model_type)
				)
			response = create_response(200)
		except:
			response = create_response(500)
			response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	def api_delete(request):
		model_id = request.POST.get('model_id',0)
		response = create_response(500)
		try:
			if model_id!=0:
				models.ProductModelProperty.objects.filter(id=model_id).delete()
				response = create_response(200)
		except:
			response.innerErrMsg = unicode_full_stack()
		return response.get_response()