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

class CustomerOrdersList(resource.Resource):
	app = 'order'
	resource = 'customer_orders_list'
	#客户查看的订单页面
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
		return render_to_response('order/customer_orders_list.html', c)

	def api_get(request):
		cur_page = request.GET.get('page', 1)
		rows = []
		orders = []

		#假数据
		rows.append({
			'order_id':'20160427170520421',
			'order_create_at': '2016-05-12',
			'product_img': '/static/upload/20160601/1464765003058_988.jpg',
			'product_name': '【唯美农业】红枣夹核桃250g*2包',
			'product_price': '25.30',
			'product_amount': '1',
			'ship_name': '周康康',
			'total_purchase_price': '25.30',
			'status': '待发货',
		})
		pageinfo, orders = paginator.paginate(orders, cur_page, COUNT_PER_PAGE, query_string=request.META['QUERY_STRING'])

		# for order in orders:
		# 	rows.append({
		# 		'order_id': order.order_id,
		# 		'order_create_at': order.order_create_at,
		# 		'product_img': order.product_img,
		# 		'product_name': order.product_name,
		# 		'product_price': order.product_price,
		# 		'product_amount': order.product_amount,
		# 		'ship_name': order.ship_name,
		# 		'total_purchase_price': order.total_purchase_price,
		# 		'status': order.status,
		# 	})
		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}

		#构造response
		response = create_response(200)
		response.data = data

		return response.get_response()