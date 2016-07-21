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

class ProductHasModel(resource.Resource):
	app = 'product'
	resource = 'product_has_model'

	def api_get(request):
		user_id = request.user.id
		value_ids = request.GET.get('value_ids',[])
		if value_ids:
			value_ids = value_ids.split(',')
		print value_ids,"--------------"
		product_model_property_values = models.ProductModelPropertyValue.objects.filter(id__in=value_ids)
		property_ids = []
		for product_model_property_value in product_model_property_values:
			if product_model_property_value.property_id not in property_ids:
				property_ids.append(product_model_property_value.property_id)
		product_model_properties = models.ProductModelProperty.objects.filter(id__in=property_ids)

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
			product_model_value = ''
			if product_model_property.id in property_id2model_property_value:			
				product_model_value = property_id2model_property_value[product_model_property.id]
			rows.append({
				'id': product_model_property.id,
				'product_model_name': product_model_property.name,
				'model_type': product_model_property.type,
				'product_model_value': '' if not product_model_value else json.dumps(product_model_value),
			})

		data = {
			'rows': rows
		}
		#构造response
		response = create_response(200)
		response.data = data
		return response.get_response()