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
		
		account_has_suppliers = AccountHasSupplier.objects.all()
		supplier_ids = []
		for account_has_supplier in account_has_suppliers:
			if str(account_has_supplier.supplier_id) not in supplier_ids:
				supplier_ids.append(str(account_has_supplier.supplier_id))
		# product_ids = []
		# api_pids = []
		# #构造云商通内商品id，与panda数据库内商品id的关系
		# product_weapp_id2product_id = {}
		# for product_has_relation in product_has_relations:
		# 	#获得所有绑定过云商通的商品id
		# 	if product_has_relation.product_id not in product_ids:
		# 		product_ids.append(product_has_relation.product_id)
		# 	weapp_product_ids = product_has_relation.weapp_product_id.split(';')
		# 	for weapp_product_id in weapp_product_ids:
		# 		#获得所有绑定过云商通的云商通商品id
		# 		api_pids.append(weapp_product_id)
		# 		if not product_weapp_id2product_id.has_key(weapp_product_id):
		# 			product_weapp_id2product_id[weapp_product_id] = [product_has_relation.product_id]
		# 		else:
		# 			product_weapp_id2product_id[weapp_product_id].append(product_has_relation.product_id)

		#构造云商通供货商id与客户名称的对应关系
		# products = product_models.Product.objects.filter(id__in=product_ids)
		all_sellers = UserProfile.objects.filter(role=CUSTOMER)
		account_id2seller_name = dict((account.id, account.name) for account in all_sellers)
		supplier_id2seller_name = {}
		for supplier_id in supplier_ids:
			if not supplier_id2seller_name.has_key(supplier_id):
				account_id = account_has_suppliers.filter(supplier_id=int(supplier_id)).first().account_id
				seller_name = account_id2seller_name[account_id]
				supplier_id2seller_name[supplier_id] = [seller_name]
		#查找
		filter_params = {}
		if customer_name:
			supplier_ids = []
			sellers = all_sellers.filter(name__icontains=customer_name)
			customer_ids = [seller.id for seller in sellers]
			cur_account_has_suppliers = account_has_suppliers.filter(account_id__in=customer_ids)
			for cur_account_has_supplier in cur_account_has_suppliers:
				if str(cur_account_has_supplier.supplier_id) not in supplier_ids:
					supplier_ids.append(str(cur_account_has_supplier.supplier_id))

		if from_mall != '-1':
			filter_params['webapp_id'] = from_mall
		if order_create_at_range:
			start_time = order_create_at_range[0]
			end_time = order_create_at_range[1]
			filter_params['start_time'] = start_time
			filter_params['end_time'] = end_time

		supplier_ids = '_'.join(supplier_ids)
		rows = []
		if supplier_ids != '':
			# try:
			#请求接口获得数据
			if is_for_list:
				params = {
					'status': 5,#运营只查看已完成的订单
					'supplier_ids': supplier_ids,
					'page':cur_page,
					'count_per_page': COUNT_PER_PAGE
				}
				params.update(filter_params)
				r = requests.get(ZEUS_HOST+'/panda/order_list_by_supplier/',params=params)
				res = json.loads(r.text)
				if res['code'] == 200:
					orders = res['data']['orders']
				else:
					print('res!!!!!!!!!!!!!!!!!!!!')
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
					print('from_mall_res!!!!!!!!!!!!!!!!!')
					print(from_mall_res)
				pageinfo = res['data']['pageinfo']
				pageinfo['total_count'] = pageinfo['object_count']
			else:
				#请求导出的接口
				params = {
					'status': 5,
					'supplier_ids': supplier_ids
				}
				params.update(filter_params)
				r = requests.get(ZEUS_HOST+'/panda/order_export_by_supplier/',params=params)
				res = json.loads(r.text)
				if res['code'] == 200:
					orders = res['data']['orders']
				else:
					print('res!!!!!!!!!!!!!!!!!')
					print(res)
					response = create_response(500)
					return response.get_response()

			for order in orders:
				return_product_infos = order['products']
				if is_for_list:
					total_purchase_price = 0
					for return_product_info in return_product_infos:
						product_id = str(return_product_info['id'])
						total_purchase_price += int(return_product_info['count'])*float(return_product_info['purchase_price'])#计算订单总金额
					webapp_id = order['webapp_id']
					rows.append({
						'order_id': order['order_id'],
						'order_create_at': order['created_at'],
						'total_purchase_price': str('%.2f' % total_purchase_price),
						'customer_name': supplier_id2seller_name[str(order['supplier'])],
						'from_mall': webapp_id2store_name[webapp_id]
					})
				else:
					rows.append({
						'order_id': order['order_id'],
						'express_company_name': order['express_company_name'],
						'express_number': order['express_number']
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