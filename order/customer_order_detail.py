# -*- coding: utf-8 -*-
import json
import time
import base64

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
import nav
import models
from resource import models as resource_models
from util import string_util

FIRST_NAV = 'order'
SECOND_NAV = 'order-list'
COUNT_PER_PAGE = 10

class CustomerOrderDetail(resource.Resource):
	app = 'order'
	resource = 'customer_order_detail'
	
	@login_required
	def get(request):
		#获取业务数据
		order_id = request.GET.get('id', None)
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
			'order_id': order_id
		})
		return render_to_response('order/customer_order_detail.html', c)

	@login_required
	def api_get(request):
		cur_page = request.GET.get('page', 1)
		order_id = request.GET.get('order_id', 0)
		rows = [{
			'product_name': u'[唯美农业]红枣夹核桃250g*2包',
			'unit_price': '25.30',
			'quantity': '2',
			'total_count': '2',
			'order_money': '50.60'
		},{
			'product_name': u'米琦尔大米',
			'unit_price': '59',
			'quantity': '1',
			'total_count': '1',
			'order_money': '59'
		},{
			'product_name': u'土小宝礼品装',
			'unit_price': '60',
			'quantity': '2',
			'total_count': '2',
			'order_money': '12.00'
		}]
		data = {
			'rows': rows
		}

		#构造response
		response = create_response(200)
		response.data = data

		return response.get_response()