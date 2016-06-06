# -*- coding: utf-8 -*-
import json
import time
import urllib, urllib2
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
from account import models as account_models
from product import models as product_models
from resource import models as resource_models

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
filter2field ={
}

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
		filter_idct = dict([(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET if key.startswith('__f-')])
		order_id = filter_idct.get('order_id','')
		status = filter_idct.get('status','')
		order_create_at = filter_idct.get('order_create_at','')

		product_has_relations = product_models.ProductHasRelationWeapp.objects.exclude(weapp_product_id='')
		product_ids = []
		product_id2product_weapp_id = {}
		api_pids = [product_has_relation.weapp_product_id for product_has_relation in product_has_relations]

		for product_has_relation in product_has_relations:
			if product_has_relation.product_id not in product_ids:
				product_ids.append(product_has_relation.product_id)
			weapp_product_ids = product_has_relation.weapp_product_id.split(';')
			for weapp_product_id in weapp_product_ids:
				if not product_id2product_weapp_id.has_key(product_has_relation.product_id):
					product_id2product_weapp_id[product_has_relation.product_id] = [weapp_product_id]
				else:
					product_id2product_weapp_id[product_has_relation.product_id].append(weapp_product_id)
		product_images = product_models.ProductImage.objects.filter(product_id__in=product_ids)
		product = product_models.Product.objects.filter(id__in=product_ids)
		image_ids = [product_image.image_id for product_image in product_images]
		images = resource_models.Image.objects.filter(id__in=image_ids)

		product_weapp_id2info = {}
		for product_id in product_ids:
			image_id = product_images.get(product_id=product_id).image_id
			url = images.get(id=image_id).path
			product_name = product.get(id=product_id).product_name
			product_weapp_ids = product_id2product_weapp_id[product_id]
			for product_weapp_id in product_weapp_ids:
				if not product_weapp_id2info.has_key(product_id):
					product_weapp_id2info[product_weapp_id] = [{
						'product_name': product_name,
						'product_img': url
					}]
				else:
					product_weapp_id2info[product_weapp_id].append({
						'product_name': product_name,
						'product_img': url
					})
		# if order_id:
		# 	orders = orders.filter(order_id__icontains=order_id)
		# if status:
		# 	orders = orders.filter(status=status)
		# if order_create_at:
		# 	orders = orders.filter(order_create_at=order_create_at)

		api_pids = '_'.join(api_pids)
		product_ids = api_pids
		print('product_ids:')
		print(product_ids)
		account_type = 'customer'
		api_url = 'http://api.zeus.com/panda/order_list/?product_ids={}&account_type={}&page={}'.format(product_ids,account_type,cur_page)
		url_request = urllib2.Request(api_url)
		res_data = urllib2.urlopen(url_request)
		res = json.loads(res_data.read())
		if res['code'] == 200:
			print(res['data'])
			orders = res['data']['orders']
		else:
			print(res)
			response = create_response(500)
			return response.get_response()

		rows = []
		pageinfo = res['data']['pageinfo']
		pageinfo['total_count'] = pageinfo['object_count']

		for order in orders:
			order_id = order['order_id']
			product_infos = order['product_info']
			for product_info in product_infos:
				product_id = str(product_info['product_id'])
				product_info['product_name'] = product_weapp_id2info[product_id][0]['product_name']
				product_info['product_img'] = product_weapp_id2info[product_id][0]['product_img']
				product_info['purchase_price'] = str('%.2f' % product_info['purchase_price'])
				product_info['total_price'] = str('%.2f' % product_info['total_price'])
			rows.append({
				'order_id': order_id,
				'order_create_at': order['created_at'],
				'ship_name': order['ship_name'],
				'total_purchase_price': str('%.2f' % order['order_money']),
				'status': order_status2text[order['status']],
				'product_infos': json.dumps(product_infos)
			})
		data = {
			'rows': rows,
			'pagination_info': pageinfo
		}

		#构造response
		response = create_response(200)
		response.data = data

		return response.get_response()