# -*- coding: utf-8 -*-
__author__ = 'hj'

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
from panda.settings import ZEUS_HOST, ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
from eaglet.utils.resource_client import Resource
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
		products = product_models.Product.objects.filter(owner_id=request.user.id)
		product_images = product_models.ProductImage.objects.all().order_by('-id')

		#获取商品图片
		product_id2image_id = {}
		image_id2images = {}
		for product in product_images:
			product_id2image_id[product.product_id] = product.image_id
		for image in resource_models.Image.objects.all():
			image_id2images[image.id] = image.path

		#请求接口获得数据
		data = []
		try:
			params = {
				'order_id': order_id
			}
			# r = requests.get(ZEUS_HOST+'/mall/order_detail/',params=params)
			resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).get({
				'resource': 'mall.order_detail',
				'data': params
			})
			# res = json.loads(r.text)
			if resp and resp['code'] == 200:

				data = resp['data']['order']
			else:
				# print(res)
				response = create_response(500)
				return response.get_response()
		except Exception,e:
			print(e)

		#构造panda数据库内商品id，与云商通内商品id的关系
		product_has_relations = product_models.ProductHasRelationWeapp.objects.exclude(weapp_product_id='')
		product_weapp_id2product_id = {}
		for product_has_relation in product_has_relations:
			weapp_product_ids = product_has_relation.weapp_product_id.split(';')
			for weapp_product_id in weapp_product_ids:
				#获得所有绑定过云商通的云商通商品id
				product_weapp_id2product_id[weapp_product_id] = product_has_relation.product_id
		product_id2name = {product.id:product.product_name for product in products}
		order_products = data['product'] if data else []
		total_count = 0
		for product in order_products:
			total_count += product['count']
			product['origin_price'] = '%.2f' % product['origin_price']
			weapp_product_id = str(product['id'])
			product_id = -1 if weapp_product_id not in product_weapp_id2product_id else product_weapp_id2product_id[weapp_product_id]
			product['product_name'] = product['name'] if product_id not in product_id2name else product_id2name[product_id]
			image_id = '' if product_id not in product_id2image_id else product_id2image_id[product_id]
			product['product_img'] = product['thumbnails_url'] if image_id not in image_id2images else image_id2images[image_id]
			custom_model_properties = []
			if product['custom_model_properties']:
				for custom_model_propertie in product['custom_model_properties']:
					property_value = custom_model_propertie['property_value']
					custom_model_properties.append(property_value)
			product['custom_models'] = '' if not custom_model_properties else '/'.join(custom_model_properties)

		express_details = ''
		if data:
			express_details = json.dumps(data['express_details']) if data['express_details'] else ''
		status = '' if not data else data['status']
		origin_total_price = 0 if not data else data['origin_total_price']
		orders = [{
			'order_id': '' if not data else data['order_id'],#订单编号
			'order_status': '' if status not in order_status2text else order_status2text[status],#订单状态
			'order_express_details': express_details,#订单物流
			'ship_name': '' if not data else data['ship_name'],#收货人
			'ship_tel': '' if not data else data['ship_tel'],#收货人电话
			'customer_message': '' if not data else data['customer_message'],#买家留言
			'ship_area': '' if not data else data['ship_area'],#收货区域
			'ship_address': '' if not data else data['ship_address'],#收货地址
			'express_company_name': '' if not data else data['express_company_name'],#物流公司名称
			'express_number': '' if not data else data['express_number'],#运单号
			'origin_total_price': '%.2f' % origin_total_price,#订单金额
			'postage': '%.2f' % data['postage'],#运费
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