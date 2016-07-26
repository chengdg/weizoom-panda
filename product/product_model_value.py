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
import requests
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST


class ProductModelValue(resource.Resource):
	app = 'product'
	resource = 'product_model_value'

	def api_put(request):
		model_id = request.POST.get('model_id',0)
		model_value = request.POST.get('model_value','')
		path = request.POST.get('path','')
		response = create_response(500)
		try:
			if model_id!=0:
				db_model = models.ProductModelPropertyValue.objects.create(
					property_id = model_id,
					name = model_value,
					pic_url = path
				)

				relation = models.ProductModelPropertyRelation.objects.filter(model_property_id=model_id).first()
				if relation:
					if not path.startswith('http'):
						path = 'http://chaozhi.weizoom.com' + path
					params = {
						'id': relation.weapp_property_id,
						'name': model_value,
						'pic_url': path
					}
					resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put({
						'resource': 'mall.model_property_value',
						'data': params
					})
					if not resp or not resp.get('code') == 200:
						response = create_response(500)
					else:
						weapp_data = resp.get('data').get('product_model_value')
						models.ProductModelPropertyValueRelation.objects.create(property_value_id=db_model.id,
																				weapp_property_value_id=weapp_data.get('id'))
						response = create_response(200)
		except:
			msg = unicode_full_stack()
			response.innerErrMsg = msg
			watchdog.error(msg)

		return response.get_response()

	def api_delete(request):
		value_id = request.POST.get('value_id',0)
		response = create_response(500)
		try:
			if value_id!=0:
				models.ProductModelPropertyValue.objects.filter(id=value_id).delete()
				response = create_response(200)
				relation = models.ProductModelPropertyValueRelation.objects.filter(property_value_id=value_id).first()
				if relation:
					params = {
						'id': relation.weapp_property_value_id,
					}
					resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).delete({
						'resource': 'mall.model_property_value',
						'data': params
					})
					if not resp or not resp.get('code') == 200:
						response = create_response(500)
		except:
			msg = unicode_full_stack()
			response.innerErrMsg = msg
			watchdog.error(msg)
		return response.get_response()