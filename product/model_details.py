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
from util import string_util
from product.product_has_model import get_product_model_property_values
import models

class ModelDetails(resource.Resource):
	app = 'product'
	resource = 'model_details'

	def api_get(request):
		user_id = request.user.id
		product_id = request.GET.get('product_id',0)
		product_models = models.ProductModel.objects.filter(product_id=product_id, is_deleted=False)
		model_ids = [product_model.id for product_model in product_models]
		property_values = models.ProductModelHasPropertyValue.objects.filter(model_id__in=model_ids, is_deleted=False)
		value_ids = [property_value.property_value_id for property_value in property_values]
		product_model_property_values = models.ProductModelPropertyValue.objects.filter(id__in=value_ids)
		rows = get_product_model_property_values(product_model_property_values)
		jsons = {'items':[]}
		product_data = {}
		for product_model in product_models:
			model_Id = product_model.name
			product_data['clear_price_'+model_Id] = '%s' %('%.2f'%product_model.market_price)
			product_data['product_store_'+model_Id] = '%s' %product_model.stocks
			product_data['product_weight_'+model_Id] = '%s' %product_model.weight
			product_data['product_code_'+model_Id] = '%s' %product_model.user_code
		data = {
			'rows': rows,
			'product_data':product_data
		}
		#构造response
		response = create_response(200)
		response.data = data
		return response.get_response()