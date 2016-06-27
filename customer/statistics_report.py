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

from resource import models as resource_models
from product import models as product_models
from account.models import *
from util import string_util
from util import db_util
from panda.settings import ZEUS_HOST
from product.sales_from_weapp import sales_from_weapp
import nav
import requests

FIRST_NAV = 'customer'
SECOND_NAV = 'customer'

class Statistics(resource.Resource):
	app = 'customer'
	resource = 'statistics_report'

	@login_required
	def get(request):
		"""
		显示商品列表
		"""
		user_id = request.GET.get('id', '')
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
			'user_id': user_id
		})
		
		return render_to_response('customer/statistics_report.html', c)

	def api_get(request):
		user_id = request.GET.get('user_id', '')
		rows = []
		rows.append({
			'product_name': '商品名称',
			'weizoom_baifumei' : '2',
			'weizoom_club': '1',
			'first_week': '21',
			'second_week': '31',
			'all_purchase_number': '21',
			'one_time_purchase': '11',
			'feedback_all_number': '35',
			'weizoom_baifumei_orders_number': '21',
			'weizoom_club_orders_number': '31'
		})
		data = {
			'rows': rows
		}
		response = create_response(200)
		response.data = data
		return response.get_response()