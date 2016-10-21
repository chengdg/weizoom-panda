# -*- coding: utf-8 -*-
import json

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response

from product import models as product_models
from account import models as account_models
from postage_config import models as postage_models
from util import sync_util
import nav
import models
from order.customer_order_detail import getOrderDetail
from order.kdniao_express_eorder import KdniaoExpressEorder

class PrintEorder(resource.Resource):
	app = 'order'
	resource = 'print_eorder'

	@login_required
	def api_get(request):

		express_id = request.GET.get('express_id','')
		order_ids = request.GET.get('order_ids','')
		shipper_messages = postage_models.ShipperMessages.objects.filter(owner=request.user, is_deleted=False)
		express_bill_accounts = postage_models.ExpressBillAccounts.objects.filter(id=express_id, is_deleted=False)
		
		sender = {
			"Name" : shipper_messages[0].shipper_name,
			"Mobile" : shipper_messages[0].tel_number,
			"ProvinceName" : '上海',
			"CityName" : '上海',
			"ExpAreaName" : '青浦区',
			"Address" : shipper_messages[0].address,
		}

		express_company_name = 'EMS'
		express_company_name_value = 'ems'

		items = []
		delivery_param = []
		templates = []
		order_ids = order_ids.split(',')
		#order_ids = request.GET.get('order_ids', '')
		# orders = Order.objects.filter(id__in=[int(id) for id in order_ids], status=3)#待发货的订单
		for order_id in order_ids:
			commodity = [] #需传递的商品信息
			orders = getOrderDetail(order_id, request)
			products = json.loads(orders[0]['products'])
			for product in products:
				goods = {"GoodsName":product['product_name'], "Goodsquantity":product['count'], "GoodsCode":product['user_code']}
				commodity.append(goods)

			receiver = {
				"Name":orders[0]['ship_name'], 
				"Mobile": orders[0]['ship_tel'], 
				"ProvinceName" : '北京', 
				"CityName" : '北京', 
				"ExpAreaName" : '朝阳区',
				"Address" : orders[0]['ship_address']
			}

			orderCode = orders[0]['order_id']
			order_id = orders[0]['id']
			print orderCode, express_company_name_value, sender, receiver, commodity, order_id,"+++++++++++"
			eorder=KdniaoExpressEorder(orderCode, express_company_name_value, sender, receiver, commodity, order_id)

			is_success, template, express_order = eorder.get_express_eorder()
			# print is_success,template,"================="
			# express_number = express_order["LogisticCode"]
			
			# if is_success:
			# 	for order in orders:
			# 		delivery_param.append({'order_id':order.order_id, 'express_company_name':express_company_name, 'express_number':express_number})

		print template,"================="
		data = {
			'template': template,
			'test': '44444'
		}
		response = create_response(200)
		response.data = data
		return response.get_response()