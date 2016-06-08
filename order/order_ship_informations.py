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
from core.exceptionutil import unicode_full_stack

from util import db_util
from resource import models as resource_models
from account.models import *
from util import string_util
import nav
import models

class OrderShipInformations(resource.Resource):
	app = 'order'
	resource = 'order_ship_informations'

	@login_required
	def api_get(request):
		order_id = request.GET.get('order_id',0)
		print('order_id!!!!!!')
		print(order_id)

		#组装数据
		rows = {}
		rows['ship_company'] = '申通快递'
		rows['ship_number'] = '2016002157544125'
		rows['shiper_name'] = '小张'

		data = {
			'rows': rows
		}
		#构造response
		response = create_response(200)
		response.data = data
		return response.get_response()

	@login_required
	def api_put(request):
		order_id = request.POST.get('order_id',0)
		print('order_id!!!!!!')
		print(order_id)

		response = create_response(200)
		return response.get_response()