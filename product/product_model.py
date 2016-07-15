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
		is_export = False
		rows = [{
			'product_model_name': u'尺码',
			'model_type': 0,
			'model_name': 'XL',
		}]
		
		data = {
			'rows': rows,
			# 'pagination_info': pageinfo.to_dict()
		}

		#构造response
		response = create_response(200)
		response.data = data
		return response.get_response()