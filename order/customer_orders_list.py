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
# from eaglet.core import watchdog
# from eaglet.core.exceptionutil import unicode_full_stack
from core import resource
from core.jsonresponse import create_response
from core import paginator
from util import db_util
from eaglet.utils.resource_client import Resource

import nav
import models
from account import models as account_models
from account.models import *
from product import models as product_models
from resource import models as resource_models
from panda.settings import ZEUS_HOST
from product import models as product_models
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST

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
		try:
			cur_page = int(cur_page)
		except:
			cur_page = 1
		filter_idct = dict([(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET if key.startswith('__f-')])
		order_id = filter_idct.get('order_id','')
		filter_product_name = filter_idct.get('product_name','')
		status = filter_idct.get('status','-1')
		order_create_at_range = filter_idct.get('order_create_at__range','')

		products = product_models.Product.objects.filter(owner_id=request.user.id)
		product_ids = [int(product.id) for product in products]
		product_has_relations = product_models.ProductHasRelationWeapp.objects.filter(product_id__in=product_ids).exclude(weapp_product_id='')
		product_images = product_models.ProductImage.objects.filter(product_id__in=product_ids)
		image_ids = [product_image.image_id for product_image in product_images]
		images = resource_models.Image.objects.filter(id__in=image_ids)

		user_profile = account_models.UserProfile.objects.filter(user_id=request.user.id).first()
		print '>>>>>>>>>>>>>>>>>>>>>>>>>>>', request.user.id
		if user_profile:
			user_profile_id = user_profile.id
			account_has_suppliers = account_models.AccountHasSupplier.objects.filter(account_id=user_profile_id)
			# 为了适配新逻辑
			old_account_has_suppliers = account_models.AccountHasSupplier.objects.filter(account_id=-user_profile_id)
		else:
			account_has_suppliers = account_models.AccountHasSupplier.objects.filter(user_id=request.user.id)
			# 为了适配新逻辑
			old_account_has_suppliers = account_models.AccountHasSupplier.objects.filter(user_id=-request.user.id)
		account_has_suppliers = list(account_has_suppliers) + list(old_account_has_suppliers)
		supplier_ids = []
		api_pids = []
		is_search_product_name = False
		for account_has_supplier in account_has_suppliers:
			if str(account_has_supplier.supplier_id) not in supplier_ids:
				if account_has_supplier.supplier_id > 0:
					supplier_ids.append(str(account_has_supplier.supplier_id))
				else:
					supplier_ids.append(str(-account_has_supplier.supplier_id))
		# print supplier_ids, 'ffffffffffffffffffffffffffff'

		#构造panda数据库内商品id，与云商通内商品id的关系
		product_id2product_weapp_id = {}
		for product_has_relation in product_has_relations:
			weapp_product_ids = product_has_relation.weapp_product_id.split(';')
			for weapp_product_id in weapp_product_ids:
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
					if not product_weapp_id2info.has_key(product_weapp_id):
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
		if filter_product_name:
			is_search_product_name = True
			#如果按照商品名称查询，则传递product_ids参数给接口
			product_ids = [int(product.id) for product in products.filter(product_name__icontains=filter_product_name)]
			for product_id in product_ids:
				if product_id2product_weapp_id.has_key(product_id):
					product_weapp_ids = product_id2product_weapp_id[product_id]
					for product_weapp_id in product_weapp_ids:
						api_pids.append(product_weapp_id)
			api_pids = '_'.join(api_pids)
		if status != '-1':
			filter_params['status'] = status
		if order_create_at_range:
			start_time = order_create_at_range[0]
			end_time = order_create_at_range[1]
			filter_params['start_time'] = start_time
			filter_params['end_time'] = end_time

		supplier_ids = '_'.join(supplier_ids)
		# print('supplier_ids:')
		# print(supplier_ids)
		rows = []
		if supplier_ids != '':
			#请求接口获得数据
			if is_for_list:
				if is_search_product_name:
					if api_pids!= '':
						#按照商品名搜索、传递商品id
						params = {
							'product_ids': api_pids,
							'supplier_ids': supplier_ids,
							'page':cur_page,
							'count_per_page': COUNT_PER_PAGE
						}
					else:
						#如果商品不存在，直接返回空列表
						orders = []
						pageinfo, orders = paginator.paginate(orders, cur_page, COUNT_PER_PAGE)
						pageinfo = pageinfo.to_dict()
						data = {
							'rows': rows,
							'pagination_info': pageinfo
						}
						#构造response
						response = create_response(200)
						response.data = data
						return response.get_response()
				else:
					params = {
						'supplier_ids': supplier_ids,
						'page':cur_page,
						'count_per_page': COUNT_PER_PAGE
					}
				params.update(filter_params)
				# try:
				# r = requests.post(ZEUS_HOST+'/panda/order_list_by_supplier/',data=params)
				# res = json.loads(r.text)

				# params.update(filter_params)
				res = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post(
					{
						'resource': 'panda.order_list_by_supplier',
						'data': params
					}
				)
				if res and res['code'] == 200:
					orders = res['data']['orders']
				else:
					print(res)
					response = create_response(500)
					return response.get_response()
				pageinfo = res['data']['pageinfo']
				pageinfo['total_count'] = pageinfo['object_count']
				# except:
				# 	watchdog.error(u'连接zeus接口失败，接口:{}, 原因:{}'.format(
				# 			'order_list_by_supplier',
				# 			unicode_full_stack()
				# 		), self.express_config.watchdog_type
				# 	)
			else:
				if is_search_product_name:
					if api_pids!= '':
						#按照商品名搜索、传递商品id
						params = {'supplier_ids': supplier_ids,'product_ids': api_pids}
					else:
						return rows
				else:
					params = {'supplier_ids': supplier_ids}
				params.update(filter_params)
				res = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post(
					{
						'resource': 'panda.order_export_by_supplier',
						'data': params
					}
				)
				# r = requests.post(ZEUS_HOST+'/panda/order_export_by_supplier/',data=params)
				# res = json.loads(r.text)
				if res and res['code'] == 200:
					orders = res['data']['orders']
				else:
					print(res)
					response = create_response(500)
					return response.get_response()

			for order in orders:
				order_id = order['order_id']
				product_infos = []
				return_product_infos = order['products'] #返回的订单数据，包含了所需要的product信息
				total_weight = 0
				total_purchase_price = 0
				for return_product_info in return_product_infos:
					product_id = str(return_product_info['id'])
					if product_weapp_id2info.has_key(product_id):#只展示关联了商品id的订单
						if return_product_info['model_names']:
							model_names = u'规格：'+'/'.join(return_product_info['model_names'])
						else:
							model_names = ''
						product_infos.append({
							'product_name': product_weapp_id2info[product_id][0]['product_name'],
							'model_names': model_names,
							'product_img': product_weapp_id2info[product_id][0]['product_img'],
							'purchase_price': return_product_info['price'],
							'count': return_product_info['count'],
							'total_price': return_product_info['total_price']
						})
					else:
						if return_product_info['model_names']:
							model_names = u'规格：'+'/'.join(return_product_info['model_names'])
						else:
							model_names = ''
						product_infos.append({
							'product_name': return_product_info['name'],
							'model_names': model_names,
							'product_img': return_product_info['thumbnails_url'],
							'purchase_price': return_product_info['price'],
							'count': return_product_info['count'],
							'total_price': return_product_info['total_price']
						})
					if not is_for_list:
						total_weight +=  return_product_info['weight']
					total_purchase_price += int(return_product_info['count'])*float(return_product_info['purchase_price'])#计算订单总金额

				if is_for_list:
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
				else:
					rows.append({
						'order_id': order_id,
						'order_create_at': order['created_at'],
						'ship_name': order['ship_name'],
						'total_purchase_price': str('%.2f' % total_purchase_price),
						'total_weight': total_weight,
						'status': order_status2text[order['status']],
						'product_infos': json.dumps(product_infos),
						'express_company_name': order['express_company_name'],
						'express_number': order['express_number'],
						'leader_name': order['leader_name'],
						'ship_tel': order['ship_tel'],
						'ship_address': order['ship_address'],
						'ship_area': order['ship_area'],
						'delivery_time': order['delivery_time'],
						'customer_message': order['customer_message']
					})
		else:
			orders = []
			pageinfo, orders = paginator.paginate(orders, cur_page, COUNT_PER_PAGE)
			pageinfo = pageinfo.to_dict()

		if is_for_list:
			data = {
				'rows': rows,
				'pagination_info': pageinfo
			}
			print data
			#构造response
			response = create_response(200)
			response.data = data
			return response.get_response()
		else:
			return rows

	# def api_get(request):
	# 	"""
    #
     #    """
	# 	is_for_list = True if request.GET.get('is_for_list') else False
	# 	cur_page = request.GET.get('page', 1)
	# 	filter_idct = dict(
	# 		[(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET
	# 		 if key.startswith('__f-')])
	# 	# customer_name = filter_idct.get('customer_name', '')
	# 	order_id = filter_idct.get('order_id', '')
	# 	filter_product_name = filter_idct.get('product_name', '')
	# 	from_mall = filter_idct.get('from_mall', '-1')
	# 	order_status = filter_idct.get('status', '-1')
	# 	order_create_at_range = filter_idct.get('order_create_at__range', '')
	# 	# product_has_relations = product_models.ProductHasRelationWeapp.objects.exclude(weapp_product_id='')
	# 	if from_mall == '-1':
	# 		from_mall = ''
	# 	if order_status == '-1':
	# 		order_status = ''
	# 	#
	# 	supplier_ids = []
	# 	account_supplier = AccountHasSupplier.objects.filter(user_id=request.user.id).first()
	# 	if account_supplier:
	# 		supplier_ids.append(account_supplier.supplier_id)
	# 	else:
	# 		# 说明未同步
	# 		pageinfo = paginator.paginate_by_count(0,
	# 											   1, 15, '')
	# 		data = {
	# 			'rows': [],
	# 			'pagination_info': pageinfo
	# 		}
	# 		# 构造response
	# 		response = create_response(200)
	# 		response.data = data
	# 		return response.get_response()
    #
	# 	weapp_product_ids = []
	# 	if filter_product_name:
	# 		product_ids = [p.id for p in
	# 					   product_models.Product.objects.filter(product_name__icontains=filter_product_name)]
	# 		weapp_product_ids = [product.weapp_product_id
	# 							 for product in
	# 							 product_models.ProductHasRelationWeapp.objects.filter(product_id__in=product_ids)]
	# 		if not weapp_product_ids:
	# 			# 通过商品名字获取不到商品，直接返回None
	# 			pageinfo = paginator.paginate_by_count(0,
	# 												   1, 15, '')
	# 			data = {
	# 				'rows': [],
	# 				'pagination_info': pageinfo
	# 			}
	# 			# 构造response
	# 			response = create_response(200)
	# 			response.data = data
	# 			return response.get_response()
    #
	# 	params = {
	# 		'page': cur_page,
	# 		'from_mall': from_mall,
	# 		'order_status': order_status,
	# 		'supplier_ids': json.dumps(supplier_ids),
	# 		'product_ids': json.dumps(weapp_product_ids),
	# 		'per_count_page': 15,
	# 		'order_id': order_id
	# 	}
	# 	if order_create_at_range:
	# 		params.update({'order_create_start': order_create_at_range[0],
	# 					   'order_create_end': order_create_at_range[1],})
    #
	# 	resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post({
	# 		'resource': 'panda.order_list',
	# 		'data': params
	# 	})
	# 	if resp:
	# 		if resp.get('code') == 200:
	# 			# print resp.get('data').get('orders')
	# 			orders = resp.get('data').get('orders')
	# 			rows = []
	# 			for order in orders:
	# 				weapp_supplier_id = order.get('products')[0].get('supplier')
	# 				supplier = AccountHasSupplier.objects.filter(supplier_id=weapp_supplier_id).first()
	# 				user_profile = None
	# 				if supplier:
	# 					user_profile = UserProfile.objects.filter(id=supplier.account_id).first()
	# 				# 'order_id': order_id,
	# 				#                   'order_create_at': order['created_at'],
	# 				#                   'ship_name': order['ship_name'],
	# 				#                   'total_purchase_price': str('%.2f' % total_purchase_price),
	# 				#                   'total_weight': total_weight,
	# 				#                   'status': order_status2text[order['status']],
	# 				#                   'product_infos': json.dumps(product_infos),
	# 				#                   'express_company_name': order['express_company_name'],
	# 				#                   'express_number': order['express_number'],
	# 				#                   'leader_name': order['leader_name'],
	# 				#                   'ship_tel': order['ship_tel'],
	# 				#                   'ship_address': order['ship_address'],
	# 				#                   'ship_area': order['ship_area'],
	# 				#                   'delivery_time': order['delivery_time'],
	# 				#                   'customer_message': order['customer_message']
	# 				products = []
	# 				for product in order.get('products'):
	# 					temp = dict(count=product.get('count'),
	# 								total_price=product.get("total_price"),
	# 								product_name=product.get('product_name'),
	# 								model_names=product.get('model_names'),
	# 								purchase_price=product.get('purchase_price'),
	# 								product_img=product.get('thumbnails_url'))
	# 					products.append(temp)
	# 				rows.append({'total_purchase_price': str('%.2f' % order.get('total_purchase_price')),
	# 							 'order_id': order.get('order_id'),
	# 							 'order_create_at': order.get('created_at'),
	# 							 'ship_name': order['ship_name'],
	# 							 'from_mall': [order.get('store_name')],
	# 							 'status': order_status2text.get(order.get('status')),
	# 							 'product_infos': json.dumps(products),
	# 							 'express_company_name': order.get('express_company_name'),
	# 							 'express_number': order.get('express_number'),
	# 							 'leader_name': order.get('leader_name'),
	# 							 'total_weight': order.get('total_weight'),
	# 							 'ship_tel': order['ship_tel'],
	# 							 'ship_area': order.get('ship_area'),
	# 							 'delivery_time': order['delivery_time'],
	# 							 'ship_address': order['ship_address'],
	# 							 'customer_message': order['customer_message'],
	# 							 'customer_name': [user_profile.name if user_profile else '']})
	# 			# print rows, '------------------------------------------------'
	# 			if is_for_list:
	# 				pageinfo, rows = paginator.paginate(rows, cur_page, COUNT_PER_PAGE)
	# 				data = {
	# 					'rows': rows,
	# 					'pagination_info': pageinfo.to_dict()
	# 				}
	# 				# print 'dddddddddddddddddddddddddddddddddddddddddd', data
	# 				# 构造response
	# 				response = create_response(200)
	# 				response.data = data
	# 				return response.get_response()
	# 	if not resp:
	# 		pageinfo = paginator.paginate_by_count(0,
	# 											   int(cur_page), 15, '')
	# 		data = {
	# 			'rows': [],
	# 			'pagination_info': pageinfo
	# 		}
	# 		# 构造response
	# 		response = create_response(200)
	# 		response.data = data
	# 		return response.get_response()