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

from util import db_util
from util import string_util

import nav
import requests
from eaglet.utils.resource_client import Resource
from account.models import *
import models

FIRST_NAV = 'product'
SECOND_NAV = 'product-update-list'

class ProductUpdated(resource.Resource):
	app = 'product'
	resource = 'product_updated'

	@login_required
	def get(request):
		"""
		显示商品列表
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(request),
			'second_nav_name': SECOND_NAV
		})

		return render_to_response('product/product_updated.html', c)

	@login_required
	def api_post(request):
		#驳回
		product_id = int(request.POST.get('product_id',-1))
		reasons = request.POST.get('reasons','')
		data = {}
		response = create_response(200)
		try:
			models.Product.objects.filter(id=product_id).update(
				is_update = False,
				is_refused = True,
				refuse_reason = reasons
			)		
			data['code'] = 200
		except:
			data['code'] = 500
			response.errMsg = u'驳回失败'
		response.data = data
		return response.get_response()