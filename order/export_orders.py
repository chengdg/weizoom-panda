# -*- coding: utf-8 -*-
__author__ = 'lihanyi'

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
from yunying_orders_list import YunyingOrdersList

express_company_name2text = {
	'':'',
	'shentong': u'申通快递',
	'ems': u'EMS',
	'yuantong': u'圆通速递',
	'shunfeng': u'顺丰速运',
	'zhongtong': u'中通速递',
	'tiantian': u'天天快递',
	'yunda': u'韵达快运',
	'huitongkuaidi': u'百世快递',
	'quanfengkuaidi': u'全峰快递',
	'debangwuliu': u'德邦物流',
	'zhaijisong': u'宅急送',
	'kuaijiesudi': u'快捷速递',
	'bpost': u'比利时邮政',
	'suer': u'速尔快递',
	'guotongkuaidi': u'国通快递',
	'youzhengguonei': u'邮政包裹/平邮',
	'rufengda': u'如风达',
	'youshuwuliu': u'优速物流',
	'annengwuliu': u'安能物流',
	'yuanchengkuaiyun':'远成快运',
}
haved_express_company_name = ['shentong','ems','yuantong','shunfeng','zhongtong','tiantian','yunda','huitongkuaidi','quanfengkuaidi','debangwuliu','zhaijisong','kuaijiesudi','bpost','suer','guotongkuaidi','youzhengguonei','rufengda','youshuwuliu','annengwuliu','yuanchengkuaiyun']

class ExportOrders(resource.Resource):
	app = 'order'
	resource = 'export_orders'

	@login_required
	def get(request):
		orders = CustomerOrdersList.api_get(request)
		titles = [
			u'订单号',u'下单时间',u'商品名称',u'商品规格', u'商品单价', u'商品数量', u'销售额', u'商品总重量', u'订单状态', u'收货人', u'联系电话', u'收货地址', u'发货人', u'发货人备注', u'物流公司', u'快递单号', u'发货时间', u'用户备注'
		]
		table = []
		table.append(titles)
		for order in orders:
			product_infos = json.loads(order['product_infos'])
			for product_info in product_infos:
				if product_info['model_names']:
					product_models = product_info['model_names']
				else:
					product_models = ''
				if order['leader_name'].find('|') == -1:
					leader_name = order['leader_name']
					leader_name_message = ''
				else:
					leader_name,leader_name_message = order['leader_name'].split('|')
				price = float(product_info['price'])
				sales_price = str('%.2f' %  ( price*int(product_info['count'])) )
				# print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.'
				# print order['express_company_name']
				# print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.'
				if order['express_company_name'] not in haved_express_company_name:
					cur_express_company_name = order['express_company_name']
				else:
					cur_express_company_name = express_company_name2text[order['express_company_name']]
				table.append([
					order['order_id'],
					order['order_create_at'],
					product_info['product_name'],
					product_models,
					str('%.2f' % price),
					str(product_info['count'])+u'件',
					sales_price,
					order['total_weight'],
					order['status'],
					order['ship_name'],
					order['ship_tel'],
					order['ship_area']+' '+order['ship_address'],
					leader_name,
					leader_name_message,
					cur_express_company_name,
					order['express_number'],
					order['delivery_time'],
					order['customer_message']
				])
		return ExcelResponse(table,output_name=u'订单列表'.encode('utf8'),force_csv=False)

class YunyingExportOrders(resource.Resource):
	app = 'order'
	resource = 'yunying_export_orders'

	@login_required
	def get(request):
		orders = YunyingOrdersList.api_get(request)
		titles = [
			u'订单编号', u'物流公司', u'快递单号'
		]
		table = []
		table.append(titles)

		for order in orders:
			if order['express_company_name'] not in haved_express_company_name:
				cur_express_company_name = order['express_company_name']
			else:
				cur_express_company_name = express_company_name2text[order['express_company_name']]
			table.append([
				order['order_id'],
				cur_express_company_name,
				order['express_number']
			])
		return ExcelResponse(table,output_name=u'发货文件'.encode('utf8'),force_csv=False)