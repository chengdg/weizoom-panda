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
from core.exceptionutil import unicode_full_stack

from resource import models as resource_models
from product import models as product_models
from util import string_util
from panda.settings import ZEUS_HOST
import nav
import models
import urllib2
import urllib
import requests

FIRST_NAV = 'order'
SECOND_NAV = 'order-list'
COUNT_PER_PAGE = 10
order_status2text = {
	0: u'待支付',
	1: u'已取消',
	2: u'已支付',
	3: u'待发货',
	4: u'已发货',
	5: u'已完成',
	6: u'退款中',
	7: u'退款完成',
	8: u'团购退款',
	9: u'团购退款完成'
}

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
		products = product_models.Product.objects.all()
		# 请求接口获得数据
		url = ZEUS_HOST+'/mall/order_detail/?order_id=20160615143712504'
		url_request = urllib2.Request(url)
		opener = urllib2.urlopen(url_request)
		data = []
		res = opener.read()
		if json.loads(res)['code'] == 200:
			data = json.loads(res)['data']['order']
		else:
			response = create_response(500)
			return response.get_response()
		product_id2name = {product.id:product.product_name for product in products}
		order_products = data['product']
		total_count = 0
		for product in order_products:
			total_count += product['count']
			product['purchase_price'] = '%.2f' %product['purchase_price']
			product_id = product['id']
			product['product_name'] = '' if product_id not in product_id2name else product_id2name[product_id]
		orders=[{
			'order_id': data['order_id'],#订单编号
			'order_status': order_status2text[data['status']],#订单状态
			'order_express_details': json.dumps(data['express_details']) if data['express_details'] else '',#订单物流
			'ship_name': data['ship_name'],#收货人
			'ship_tel': data['ship_tel'],#收货人电话
			'customer_message': data['customer_message'],#买家留言
			'ship_address': data['ship_address'],#收货地址
			'express_company_name': data['express_company_name'],#物流公司名称
			'express_number': data['express_number'],#运单号
			'order_money': '%.2f' %data['total_purchase_price'],#订单金额
			'total_count': total_count,#商品件数
			'products': json.dumps(order_products)# 购买商品
		}]
		data = {
			'rows': orders
		}
		#构造response
		response = create_response(200)
		response.data = data
		return response.get_response()