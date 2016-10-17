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

class ProductReject(resource.Resource):
	app = 'product'
	resource = 'product_reject'

	@login_required
	def api_post(request):
		#运营查看商品列表，入库驳回
		product_ids = request.POST.get('product_id',-1)
		reasons = request.POST.get('reasons','')
		data = {}
		product_ids = product_ids.split(',')
		try:
			for product_id in product_ids:
				product_id = int(product_id)
				models.Product.objects.filter(id=product_id).update(is_refused=True)
				models.ProductRejectLogs.objects.create(
					product_id = product_id,
					reject_reasons = reasons
				)		
			data['code'] = 200
			response = create_response(200)
		except:
			data['code'] = 500
			response = create_response(500)
			response.errMsg = u'驳回失败'
		response.data = data
		return response.get_response()