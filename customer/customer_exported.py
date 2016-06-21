# -*- coding: utf-8 -*-
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from core import resource
from excel_response import ExcelResponse
from statistics import getCustomerData

class CustomerExported(resource.Resource):
	app = 'customer'
	resource = 'customer_exported'

	def get(request):
		is_export = True
		customer_list = getCustomerData(request,is_export)
		titles = [
			u'客户名称', u'分类', u'开始推广时间', u'总销量', u'订单数', u'总金额', u'现金', u'微众卡', u'优惠券'
		]
		order_table = []
		order_table.append(titles)
		for customer in customer_list:
			info = [
				customer['customer_name'],
				customer['classify'],
				customer['brand_time'],
				customer['total_sales'],
				customer['total_order_number'],
				customer['total_order_money'],
				customer['total_final_price'],
				customer['total_weizoom_card_money'],
				customer['total_coupon_money']
			]
			order_table.append(info)
		filename = u'客户统计列表'
		return ExcelResponse(order_table,output_name=filename.encode('utf8'),force_csv=False)
