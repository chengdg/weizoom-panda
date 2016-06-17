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
from account.models import *
from product import models as product_models
from panda.settings import ZEUS_HOST

FIRST_NAV = 'order'
SECOND_NAV = 'order-list'
COUNT_PER_PAGE = 10

filter2field ={
}

class YunyingOrdersList(resource.Resource):
	app = 'order'
	resource = 'yunying_orders_list'
	#运营查看的订单页面
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

		return render_to_response('order/yunying_orders_list.html', c)

	def api_get(request):
		is_for_list = True if request.GET.get('is_for_list') else False
		cur_page = request.GET.get('page', 1)
		filter_idct = dict([(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET if key.startswith('__f-')])
		customer_name = filter_idct.get('customer_name','')
		from_mall = filter_idct.get('from_mall','-1')
		order_create_at_range = filter_idct.get('order_create_at__range','')
		product_has_relations = product_models.ProductHasRelationWeapp.objects.exclude(weapp_product_id='')

		product_ids = []
		api_pids = []
		#构造云商通内商品id，与panda数据库内商品id的关系
		product_weapp_id2product_id = {}
		for product_has_relation in product_has_relations:
			#获得所有绑定过云商通的商品id
			if product_has_relation.product_id not in product_ids:
				product_ids.append(product_has_relation.product_id)
			weapp_product_ids = product_has_relation.weapp_product_id.split(';')
			for weapp_product_id in weapp_product_ids:
				#获得所有绑定过云商通的云商通商品id
				api_pids.append(weapp_product_id)
				if not product_weapp_id2product_id.has_key(weapp_product_id):
					product_weapp_id2product_id[weapp_product_id] = [product_has_relation.product_id]
				else:
					product_weapp_id2product_id[weapp_product_id].append(product_has_relation.product_id)

		#构造云商通pid与客户名称的对应关系
		products = product_models.Product.objects.filter(id__in=product_ids)
		all_sellers = UserProfile.objects.filter(role=CUSTOMER)
		product_weapp_id2seller_name = {}
		for api_pid in api_pids:
			if not product_weapp_id2seller_name.has_key(api_pid):
				product_id = product_weapp_id2product_id[api_pid][0]
				owner_id = products.get(id=product_id).owner_id
				seller_name = all_sellers.get(user_id=owner_id).name
				product_weapp_id2seller_name[api_pid] = [seller_name]

		#查找
		filter_params = {}
		if customer_name:
			try:
				customer_id = all_sellers.get(name=customer_name).user_id
				cur_customer_products = products.filter(owner_id=customer_id)
				cur_customer_product_ids = [cur_customer_product.id for cur_customer_product in cur_customer_products]
				cur_customer_relations = product_has_relations.filter(product_id__in=cur_customer_product_ids)
				cur_customer_weapp_ids = [cur_customer_relation.weapp_product_id for cur_customer_relation in cur_customer_relations]
				api_pids = cur_customer_weapp_ids
			except:
				api_pids = []
		if from_mall != '-1':
			filter_params['webapp_id'] = from_mall
		if order_create_at_range:
			start_time = order_create_at_range[0]
			end_time = order_create_at_range[1]
			filter_params['start_time'] = start_time
			filter_params['end_time'] = end_time

		api_pids = '_'.join(api_pids)
		print('api_pids')
		print(api_pids)
		rows = []
		if api_pids != '':
			# try:
			#请求接口获得数据
			params = {
				'status': 5,#运营只查看已完成的订单
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

			#从接口获得来源商城名称
			webapp_ids = [order['webapp_id'] for order in orders]
			webapp_ids = '_'.join(webapp_ids)
			from_mall_response = requests.get(ZEUS_HOST+'/mall/store_name/',params={'webapp_ids':webapp_ids})
			from_mall_res = json.loads(from_mall_response.text)
			webapp_id2store_name = {}
			if from_mall_res['code'] == 200:
				store_names = from_mall_res['data']['store_names']
				for store_name in store_names:
					webapp_id = store_name['webapp_id']
					store_name = store_name['store_name']
					webapp_id2store_name[webapp_id] = [store_name]
			else:
				print(res)

			pageinfo = res['data']['pageinfo']
			pageinfo['total_count'] = pageinfo['object_count']

			for order in orders:
				# print(order)
				return_product_infos = order['products']
				total_purchase_price = 0
				for return_product_info in return_product_infos:
					product_id = str(return_product_info['id'])
					if product_weapp_id2seller_name.has_key(product_id):
						weapp_product_id = product_id
						total_purchase_price += int(return_product_info['count'])*float(return_product_info['purchase_price'])#计算订单总金额
				webapp_id = order['webapp_id']
				rows.append({
					'order_id': order['order_id'],
					'order_create_at': order['created_at'],
					'total_purchase_price': str('%.2f' % total_purchase_price),
					'customer_name': product_weapp_id2seller_name[weapp_product_id],
					'from_mall': webapp_id2store_name[webapp_id]
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