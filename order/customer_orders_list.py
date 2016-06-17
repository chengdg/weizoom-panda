# -*- coding: utf-8 -*-
import json
import time
import requests
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
from panda.settings import ZEUS_HOST

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
		is_for_list = True if request.GET.get('is_for_list') else False
		cur_page = request.GET.get('page', 1)
		filter_idct = dict([(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET if key.startswith('__f-')])
		order_id = filter_idct.get('order_id','')
		status = filter_idct.get('status','-1')
		order_create_at_range = filter_idct.get('order_create_at__range','')

		products = product_models.Product.objects.filter(owner_id=request.user.id)
		product_ids = [int(product.id) for product in products]
		product_has_relations = product_models.ProductHasRelationWeapp.objects.filter(product_id__in=product_ids).exclude(weapp_product_id='')
		product_images = product_models.ProductImage.objects.filter(product_id__in=product_ids)
		image_ids = [product_image.image_id for product_image in product_images]
		images = resource_models.Image.objects.filter(id__in=image_ids)

		api_pids = []
		#构造panda数据库内商品id，与云商通内商品id的关系
		product_id2product_weapp_id = {}
		for product_has_relation in product_has_relations:
			weapp_product_ids = product_has_relation.weapp_product_id.split(';')
			for weapp_product_id in weapp_product_ids:
				#获得所有绑定过云商通的云商通商品id
				api_pids.append(weapp_product_id)
				if not product_id2product_weapp_id.has_key(product_has_relation.product_id):
					product_id2product_weapp_id[product_has_relation.product_id] = [weapp_product_id]
				else:
					product_id2product_weapp_id[product_has_relation.product_id].append(weapp_product_id)

		#构造云商通内商品id，与panda数据库内商品名称与商品图片的关系
		product_weapp_id2info = {}
		for product_id in product_ids:
			image_id = product_images.filter(product_id=product_id).first().image_id
			url = images.get(id=image_id).path
			product_name = products.get(id=product_id).product_name
			if product_id2product_weapp_id.has_key(product_id):
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
		#查找
		filter_params = {}
		if order_id:
			filter_params['order_id'] = order_id
		if status != '-1':
			filter_params['status'] = status
		if order_create_at_range:
			start_time = order_create_at_range[0]
			end_time = order_create_at_range[1]
			filter_params['start_time'] = start_time
			filter_params['end_time'] = end_time

		api_pids = '_'.join(api_pids)
		print('api_pids:')
		print(api_pids)
		rows = []
		if api_pids != '':
			# try:
			#请求接口获得数据
			params = {
				'product_ids': api_pids,
				'page':cur_page,
				'count_per_page': COUNT_PER_PAGE
			}
			params.update(filter_params)
			r = requests.get(ZEUS_HOST+'/panda/order_list/',params=params)
			res = json.loads(r.text)
			if res['code'] == 200:
				orders = res['data']['orders']
			else:
				print(res)
				response = create_response(500)
				return response.get_response()

			pageinfo = res['data']['pageinfo']
			pageinfo['total_count'] = pageinfo['object_count']

			for order in orders:
				order_id = order['order_id']
				product_infos = []
				return_product_infos = order['products'] #返回的订单数据，包含了不需要的product信息
				total_purchase_price = 0
				for return_product_info in return_product_infos:
					product_id = str(return_product_info['id'])
					if product_weapp_id2info.has_key(product_id):#只展示关联商品id的订单
						product_infos.append({
							'product_name': product_weapp_id2info[product_id][0]['product_name'],
							'product_img': product_weapp_id2info[product_id][0]['product_img'],
							'purchase_price': return_product_info['price'],
							'count': return_product_info['count'],
							'total_price': return_product_info['total_price']
						})
						total_purchase_price += int(return_product_info['count'])*float(return_product_info['purchase_price'])#计算订单总金额
				rows.append({
					'order_id': order_id,
					'order_create_at': order['created_at'],
					'ship_name': order['ship_name'],
					'total_purchase_price': str('%.2f' % total_purchase_price),
					'status': order_status2text[order['status']],
					'product_infos': json.dumps(product_infos),
					'express_company_name': order['express_company_name'],
					'express_number': order['express_number'],
					'leader_name': order['leader_name']
				})
			# except Exception,e:
			# 	print('eeeeeeeeeeeeeeeeeee')
			# 	print(e)
			# 	orders = []
			# 	pageinfo, orders = paginator.paginate(orders, cur_page, COUNT_PER_PAGE)
			# 	pageinfo = pageinfo.to_dict()
		else:
			orders = []
			pageinfo, orders = paginator.paginate(orders, cur_page, COUNT_PER_PAGE)
			pageinfo = pageinfo.to_dict()

		if is_for_list:
			data = {
				'rows': rows,
				'pagination_info': pageinfo
			}
			#构造response
			response = create_response(200)
			response.data = data
			return response.get_response()
		else:
			return rows