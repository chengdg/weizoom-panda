# -*- coding: utf-8 -*-
__author__ = 'lihanyi'

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
from eaglet.utils.resource_client import Resource

import nav
import models
from account.models import *
from product import models as product_models
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST, ZEUS_HOST
from panda.settings import CESHI_USERNAMES
from self_shop.manage import get_all_synced_self_shops

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
haved_express_company_name = ['shentong','ems','yuantong','shunfeng','zhongtong','tiantian','yunda','huitongkuaidi','quanfengkuaidi','debangwuliu','zhaijisong','kuaijiesudi','bpost','suer','guotongkuaidi','youzhengguonei','rufengda','youshuwuliu','annengwuliu','yuanchengkuaiyun']

class YunyingOrdersList(resource.Resource):
	app = 'order'
	resource = 'yunying_orders_list'
	#运营查看的订单页面
	@login_required
	def get(request):
		"""
		响应GET
		"""
		jsons = {'items' : []}
		rows = get_all_synced_self_shops(request, is_for_search=True)['rows']
		jsons['items'].append(('typeOptions', json.dumps(rows)))
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
			'jsons': jsons
		})

		return render_to_response('order/yunying_orders_list.html', c)

	# def api_get(request):
	# 	is_for_list = True if request.GET.get('is_for_list') else False
	# 	cur_page = request.GET.get('page', 1)
	# 	filter_idct = dict([(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET if key.startswith('__f-')])
	# 	customer_name = filter_idct.get('customer_name','')
	# 	filter_product_name = filter_idct.get('product_name','')
	# 	from_mall = filter_idct.get('from_mall','-1')
	# 	order_status = filter_idct.get('order_status','-1')
	# 	order_create_at_range = filter_idct.get('order_create_at__range','')
	# 	product_has_relations = product_models.ProductHasRelationWeapp.objects.exclude(weapp_product_id='')
	# 	print order_create_at_range, '++++++++++++++++++++++++++++++++++'
	# 	account_has_suppliers = AccountHasSupplier.objects.all()
	# 	supplier_ids = []
	# 	api_pids = []
	# 	is_search_product_name = False
    #
	# 	for account_has_supplier in account_has_suppliers:
	# 		if str(account_has_supplier.supplier_id) not in supplier_ids:
	# 			supplier_ids.append(str(account_has_supplier.supplier_id))
	#
	# 	#构造panda数据库内商品id，与云商通内商品id的关系
	# 	product_id2product_weapp_id = {}
	# 	for product_has_relation in product_has_relations:
	# 		weapp_product_ids = product_has_relation.weapp_product_id.split(';')
	# 		for weapp_product_id in weapp_product_ids:
	# 			if not product_id2product_weapp_id.has_key(product_has_relation.product_id):
	# 				product_id2product_weapp_id[product_has_relation.product_id] = [weapp_product_id]
	# 			else:
	# 				product_id2product_weapp_id[product_has_relation.product_id].append(weapp_product_id)
    #
	# 	all_products = product_models.Product.objects.all()
	# 	product_id2product_name = dict((product.id, product.product_name) for product in all_products)
	# 	#构造云商通内商品id，与panda数据库内商品名称的关系
	# 	product_weapp_id2product_name = {}
	# 	for product_id,product_name in product_id2product_name.items():
	# 		# product_name = product_id2product_name[product_id]
	# 		if product_id2product_weapp_id.has_key(product_id):
	# 			product_weapp_ids = product_id2product_weapp_id[product_id]
	# 			for product_weapp_id in product_weapp_ids:
	# 				if not product_weapp_id2product_name.has_key(product_id):
	# 					product_weapp_id2product_name[product_weapp_id] = product_name
	# 				else:
	# 					product_weapp_id2product_name[product_weapp_id].append(product_name)
    #
	# 	#构造云商通供货商id与客户名称的对应关系
	# 	all_sellers = UserProfile.objects.filter(role=CUSTOMER)
	# 	account_id2seller_name = dict((account.id, account.name) for account in all_sellers)
	# 	supplier_id2seller_name = {}
	# 	for supplier_id in supplier_ids:
	# 		if not supplier_id2seller_name.has_key(supplier_id):
	# 			account_id = account_has_suppliers.filter(supplier_id=int(supplier_id)).first().account_id
	# 			seller_name = account_id2seller_name.get(account_id)
	# 			supplier_id2seller_name[supplier_id] = [seller_name]
	# 	#查找
	# 	filter_params = {}
	# 	if customer_name:
	# 		supplier_ids = []
	# 		sellers = all_sellers.filter(name__icontains=customer_name)
	# 		customer_ids = [seller.id for seller in sellers]
	# 		cur_account_has_suppliers = account_has_suppliers.filter(account_id__in=customer_ids)
	# 		for cur_account_has_supplier in cur_account_has_suppliers:
	# 			if str(cur_account_has_supplier.supplier_id) not in supplier_ids:
	# 				supplier_ids.append(str(cur_account_has_supplier.supplier_id))
	# 	if filter_product_name:
	# 		is_search_product_name = True
	# 		products = product_models.Product.objects.filter(product_name__icontains=filter_product_name)
	# 		product_ids = [int(product.id) for product in products]
	# 		for product_id in product_ids:
	# 			if product_id2product_weapp_id.has_key(product_id):
	# 				product_weapp_ids = product_id2product_weapp_id[product_id]
	# 				for product_weapp_id in product_weapp_ids:
	# 					api_pids.append(product_weapp_id)
	# 		api_pids = '_'.join(api_pids)
	# 		print 'api_pids'
	# 		print api_pids
	# 	if from_mall != '-1':
	# 		filter_params['webapp_id'] = from_mall
	# 	if order_status != '-1':
	# 		filter_params['status'] = order_status
	# 	if order_create_at_range:
	# 		start_time = order_create_at_range[0]
	# 		end_time = order_create_at_range[1]
	# 		filter_params['start_time'] = start_time
	# 		filter_params['end_time'] = end_time
    #
	# 	supplier_ids = '_'.join(supplier_ids)
	# 	rows = []
	# 	if supplier_ids != '':
	# 		#请求接口获得数据
	# 		if is_for_list:
	# 			if is_search_product_name:
	# 				if api_pids!= '':
	# 					#按照商品名搜索、传递商品id
	# 					params = {
	# 						'product_ids': api_pids,
	# 						'supplier_ids': supplier_ids,
	# 						'page':cur_page,
	# 						'count_per_page': COUNT_PER_PAGE
	# 					}
	# 				else:
	# 					orders = []
	# 					pageinfo, orders = paginator.paginate(orders, cur_page, COUNT_PER_PAGE)
	# 					pageinfo = pageinfo.to_dict()
	# 					data = {
	# 						'rows': rows,
	# 						'pagination_info': pageinfo
	# 					}
	# 					#构造response
	# 					response = create_response(200)
	# 					response.data = data
	# 					return response.get_response()
	# 			else:
	# 				params = {
	# 					'supplier_ids': supplier_ids,
	# 					'page':cur_page,
	# 					'count_per_page': COUNT_PER_PAGE
	# 				}
	# 			params.update(filter_params)
	# 			r = requests.post(ZEUS_HOST+'/panda/order_list_by_supplier/',data=params)
	# 			res = json.loads(r.text)
	# 			if res['code'] == 200:
	# 				orders = res['data']['orders']
	# 			else:
	# 				print('res!!!!!!!!!!!!!!!!!!!!')
	# 				print(res)
	# 				response = create_response(500)
	# 				return response.get_response()
    #
	# 			#从接口获得来源商城名称
	# 			webapp_ids = [order['webapp_id'] for order in orders]
	# 			webapp_ids = '_'.join(webapp_ids)
	# 			from_mall_response = requests.get(ZEUS_HOST+'/mall/store_name/',params={'webapp_ids':webapp_ids})
	# 			from_mall_res = json.loads(from_mall_response.text)
	# 			webapp_id2store_name = {}
	# 			if from_mall_res['code'] == 200:
	# 				store_names = from_mall_res['data']['store_names']
	# 				for store_name in store_names:
	# 					webapp_id = store_name['webapp_id']
	# 					store_name = store_name['store_name']
	# 					webapp_id2store_name[webapp_id] = [store_name]
	# 			else:
	# 				print('from_mall_res!!!!!!!!!!!!!!!!!')
	# 				print(from_mall_res)
	# 			pageinfo = res['data']['pageinfo']
	# 			pageinfo['total_count'] = pageinfo['object_count']
	# 		else:
	# 			#请求导出的接口
	# 			if is_search_product_name:
	# 				if api_pids!= '':
	# 					params = {
	# 						'supplier_ids': supplier_ids,
	# 						'product_ids': api_pids
	# 					}
	# 				else:
	# 					return rows
	# 			else:
	# 				params = {
	# 					'supplier_ids': supplier_ids
	# 				}
	# 			params.update(filter_params)
	# 			r = requests.post(ZEUS_HOST+'/panda/order_export_by_supplier/',data=params)
	# 			res = json.loads(r.text)
	# 			if res['code'] == 200:
	# 				orders = res['data']['orders']
	# 			else:
	# 				print('res!!!!!!!!!!!!!!!!!')
	# 				print(res)
	# 				response = create_response(500)
	# 				return response.get_response()
    #
	# 		for order in orders:
	# 			return_product_infos = order['products']
	# 			product_infos = []
	# 			if is_for_list:
	# 				total_purchase_price = 0
	# 				for return_product_info in return_product_infos:
	# 					product_id = str(return_product_info['id'])
	# 					total_purchase_price += int(return_product_info['count'])*float(return_product_info['purchase_price'])#计算订单总金额
	# 					if product_weapp_id2product_name.has_key(product_id):
	# 						product_name = product_weapp_id2product_name[product_id]
	# 						if return_product_info['model_names']:
	# 							model_names = '/'.join(return_product_info['model_names'])
	# 							product_infos.append(
	# 								product_name +','+str(return_product_info['count'])+u'件'+','+model_names
	# 							)
	# 						else:
	# 							product_infos.append(
	# 								product_name +','+str(return_product_info['count'])+u'件'
	# 							)
	# 					else:
	# 						#panda里面没有商品数据
	# 						if return_product_info['model_names']:
	# 							model_names = '/'.join(return_product_info['model_names'])
	# 							product_infos.append(
	# 								return_product_info['name'] +','+str(return_product_info['count'])+u'件'+','+model_names
	# 							)
	# 						else:
	# 							product_infos.append(
	# 								return_product_info['name'] +','+str(return_product_info['count'])+u'件'
	# 							)
	# 				product_infos = ';'.join(product_infos)
	# 				webapp_id = order['webapp_id']
	# 				rows.append({
	# 					'order_id': order['order_id'],
	# 					'product_name': product_infos,
	# 					'total_purchase_price': str('%.2f' % total_purchase_price),
	# 					'customer_name': supplier_id2seller_name[str(order['supplier'])],
	# 					'from_mall': webapp_id2store_name[webapp_id],
	# 					'order_status': order_status2text[order['status']]
	# 				})
	# 			else:
	# 				rows.append({
	# 					'order_id': order['order_id'],
	# 					'express_company_name': order['express_company_name'],
	# 					'express_number': order['express_number']
	# 				})
	# 	else:
	# 		orders = []
	# 		pageinfo, orders = paginator.paginate(orders, cur_page, COUNT_PER_PAGE)
	# 		pageinfo = pageinfo.to_dict()
    #
	# 	if is_for_list:
	# 		print rows, pageinfo
	# 		data = {
	# 			'rows': rows,
	# 			'pagination_info': pageinfo
	# 		}
	# 		#构造response
	# 		response = create_response(200)
	# 		response.data = data
	# 		return response.get_response()
	# 	else:
	# 		return rows


	def api_get(request):
		"""

		"""
		is_for_list = True if request.GET.get('is_for_list') else False
		is_first = True if request.GET.get('is_first') else False #是否需要发接口请求
		cur_page = request.GET.get('page', 1)
		filter_idct = dict(
			[(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET
			 if key.startswith('__f-')])
		customer_name = filter_idct.get('customerName', '')
		filter_product_name = filter_idct.get('productName', '')
		from_mall = filter_idct.get('fromMall', '-1')
		order_status = filter_idct.get('orderStatus', '-1')
		# 订单号
		order_id = filter_idct.get('orderId', '')
		order_create_at_range = filter_idct.get('orderCreateAt__range', '')
		if filter_idct:
			is_first = False #含有查找条件，发送接口请求
		# product_has_relations = product_models.ProductHasRelationWeapp.objects.exclude(weapp_product_id='')
		if from_mall == '-1':
			from_mall = ''
		else:
			weapp_count = product_models.SelfUsernameWeappAccount.objects.filter(self_user_name=from_mall).first()
			weapp_count_id = weapp_count.weapp_account_id
			from_mall = weapp_count_id
		if order_status == '-1':
			order_status = ''
		#
		supplier_ids = []
		if customer_name:
			all_sellers = UserProfile.objects.filter(role=CUSTOMER,
													 name__icontains=customer_name,
													 is_active=True)
			account_ids = [seller.id for seller in all_sellers]
			# 获取该客户下旧的供货商id获取到
			account_ids += [-seller.id for seller in all_sellers]
			supplier_ids = [a.supplier_id for a in AccountHasSupplier.objects.filter(account_id__in=account_ids)]

			# supplier_ids = [a.supplier_id for a in AccountHasSupplier.objects.filter(user_id__in=account_ids)]
			# supplier_ids = old_supplier_ids + supplier_ids
			# print 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWW', supplier_ids
			# 如果根据名字获取不到供应商，就直接返回none
			if not supplier_ids:
				pageinfo = paginator.paginate_by_count(0,
											1, 15, '')
				# print pageinfo
				data = {
					'rows': [],
					'pagination_info': pageinfo
				}

				# 构造response
				response = create_response(200)
				response.data = data
				return response.get_response()
		# if not supplier_ids:
		# 	account_has_suppliers = AccountHasSupplier.objects.all()
		weapp_product_ids = []
		if filter_product_name:
			product_ids = [p.id for p in product_models.Product.objects.filter(product_name__icontains=filter_product_name)]
			weapp_product_ids = [product.weapp_product_id
								 for product in product_models.ProductHasRelationWeapp.objects.filter(product_id__in=product_ids)]
			if not weapp_product_ids:
				# 通过商品名字获取不到商品，直接返回None
				pageinfo = paginator.paginate_by_count(0,
													   1, 15, '')
				data = {
					'rows': [],
					'pagination_info': pageinfo
				}
				# 构造response
				response = create_response(200)
				response.data = data
				return response.get_response()
		try:
			cur_page = int(cur_page)
		except:
			cur_page = 1
		params = {
			'page': cur_page,
			'from_mall': from_mall,
			'order_status': order_status,
			'supplier_ids': json.dumps(supplier_ids),
			'product_ids': json.dumps(weapp_product_ids),
			'per_count_page': 15,
			'order_id': order_id
		}
		if order_create_at_range:
			params.update({'order_create_start': order_create_at_range[0],
						   'order_create_end': order_create_at_range[1],})
		# print supplier_ids, '+++++++++++++++++++++++++++'
		if not is_first:
			resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post({
					'resource': 'panda.order_list',
					'data': params
				})
		else:
			resp = None

		if resp:
			if resp.get('code') == 200:
				# print resp.get('data').get('orders')
				orders = resp.get('data').get('orders')
				rows = []
				for order in orders:
					if is_for_list:#运营订单列表展示用
						weapp_supplier_id = order.get('products')[0].get('supplier')
						supplier = AccountHasSupplier.objects.filter(supplier_id=weapp_supplier_id).last()
						user_profile = None
						if supplier:
							user_profile = UserProfile.objects.filter(user_id=supplier.user_id).first()
						# print supplier.store_name, '------------------------------------------------'
						# weapp_owner_id = order.get('owner_id')
						# 规格信息
						temp_product_name = []
						product_model_properties = order['products']
						total_price = 0
						for product_model in product_model_properties:

							total_price += product_model.get('origin_total_price')
							product_properties = product_model.get('custom_model_properties')
							if product_properties:
								model_info = [p_model.get('property_value') for p_model in product_properties if product_properties]

								if model_info:
									model_info = u'(' + '/'.join(model_info) + u')'
							else:
								model_info = ''
							# print type(model_info), type(product_model.get('count', 0)), type(product_model.get('name', ''))
							temp_product_name.append( product_model.get('name', '') + model_info \
											 + u',' + str(product_model.get('count', 0)) + u'件' )

						# model_info = ''
						# if product_models:
						# 	model_info = [p_model.get('property_value') for p_model in product_models]
						# 	if model_info:
						# 		model_info = u'('+ '/'.join(model_info) + u')'

						rows.append({'totalPurchasePrice': '%.2f' % total_price,
									 'orderId': order.get('order_id'),
									 'fromMall': [order.get('store_name')],
									 'orderStatus': order_status2text.get(order.get('status')),
									 'productName': '\n'.join(temp_product_name),
									 'customerName': [user_profile.name if user_profile else ''],
									 'postage': '%.2f' % order.get('postage')})
					else:
						#导出订单字段
						rows.append({
							'order_id': order['order_id'],
							'express_company_name': order['express_company_name'] if order['express_company_name']  in haved_express_company_name else 'qita',
							'express_company_storename': order['express_company_name'],
							'express_number': order['express_number']
						})
				# print rows, '------------------------------------------------'
				if is_for_list:
					pageinfo = paginator.paginate_by_count(resp.get('data').get('count'),
																   int(cur_page), 15, '')
					data = {
						'rows': rows,
						'pagination_info': pageinfo
					}
					# 构造response
					response = create_response(200)
					response.data = data
					return response.get_response()
				else:
					return rows
		if not resp:
			pageinfo = paginator.paginate_by_count(0,
												   int(cur_page), 15, '')
			data = {
				'rows': [],
				'pagination_info': pageinfo
			}
			# 构造response
			response = create_response(200)
			response.data = data
			return response.get_response()