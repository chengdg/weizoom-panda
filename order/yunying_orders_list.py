# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from core import paginator
from util import db_util
import nav
import models
from account.models import *

FIRST_NAV = 'order'
SECOND_NAV = 'order-list'
COUNT_PER_PAGE = 10

class YunyingOrdersList(resource.Resource):
	app = 'order'
	resource = 'yunying_orders_list'
	#运营查看的订单页面
	@login_required
	def get(request):
		"""
		响应GET
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV
		})

		return render_to_response('order/yunying_orders_list.html', c)

	def api_get(request):
		cur_page = request.GET.get('page', 1)
		orders = []
		rows = []
		pageinfo, products = paginator.paginate(orders, cur_page, COUNT_PER_PAGE, query_string=request.META['QUERY_STRING'])

		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}

		#构造response
		response = create_response(200)
		response.data = data

		return response.get_response()