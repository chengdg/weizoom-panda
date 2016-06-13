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
from util import string_util
from excel_response import ExcelResponse
from customer_orders_list import CustomerOrdersList

class ExportOrders(resource.Resource):
	app = 'order'
	resource = 'export_orders'

	@login_required
	def get(request):
		orders = CustomerOrdersList.api_get(request)
		titles = [
			u'商品', u'单价/数量', u'收货人', u'订单金额', u'订单状态'
		]
		table = []
		table.append(titles)
		for order in orders:
			product_names = []
			product_price_count = []
			product_infos = json.loads(order['product_infos'])
			for product_info in product_infos:
				product_names.append(product_info['product_name'])
				product_price_count.append( product_info['purchase_price']+'('+str(product_info['count'])+u'件)')
			product_names = ','.join(product_names)
			product_price_count = ','.join(product_price_count)
			table.append([
				product_names,
				product_price_count,
				order['ship_name'],
				order['total_purchase_price'],
				order['status']
			])
		return ExcelResponse(table,output_name=u'订单列表'.encode('utf8'),force_csv=False)
