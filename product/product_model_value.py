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

class ProductModel(resource.Resource):
	app = 'product'
	resource = 'product_model_value'

	def api_put(request):
		model_id = request.POST.get('model_id',0)
		model_value = request.POST.get('model_value','')
		path = request.POST.get('path','')
		response = create_response(500)
		try:
			if model_id!=0:
				models.ProductModelPropertyValue.objects.create(
					property_id = model_id,
					name = model_value,
					pic_url = path
				)
				response = create_response(200)
		except:
			response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	def api_delete(request):
		value_id = request.POST.get('value_id',0)
		response = create_response(500)
		try:
			if value_id!=0:
				models.ProductModelPropertyValue.objects.filter(id=value_id).delete()
				response = create_response(200)
		except:
			response.innerErrMsg = unicode_full_stack()
		return response.get_response()