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
from postage_config import models as postage_models
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
options2text = {
	'yuantong': '圆通速递',
	'zhongtong': '中通速递',
	'shentong': '申通快递',
	'tiantian': '天天快递',
	'yunda': '韵达快运',
	'huitongkuaidi': '百世快递',
	'shunfeng': '顺丰速运',
	'debangwuliu': '德邦物流',
	'zhaijisong': '宅急送',
	'youshuwuliu': '优速物流',
	'guangdongyouzheng': '广东邮政',
	'ems': 'EMS',
	'youshuwuliu':'优速物流',
	'annengwuliu':'安能物流'
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
		jsons = {'items':[]}
		account_user_profile = account_models.UserProfile.objects.get(user_id=request.user.id, is_active=True)
		express_bill_accounts = postage_models.ExpressBillAccounts.objects.filter(owner=request.user, is_deleted=False)
		shipper_messages = postage_models.ShipperMessages.objects.filter(owner=request.user, is_deleted=False, is_active=True)
		options_for_express = []
		options_for_express.append({
			'text': u'请选择',
			'value': -1
			})
		for express_bill_account in express_bill_accounts:
			options_for_express.append({
				'text': options2text[express_bill_account.express_name],
				'value': express_bill_account.id,
				})

		hasShipper = {
			'hasShipper': True if shipper_messages else False
		}
		contact ={
			'service_tel': account_user_profile.customer_service_tel,
			'service_qq_first': account_user_profile.customer_service_qq_first,
			'service_qq_second': account_user_profile.customer_service_qq_second
		}
		jsons['items'].append(('optionsForExpress', json.dumps(options_for_express)))
		jsons['items'].append(('hasShipper', json.dumps(hasShipper)))
		jsons['items'].append(('customerServiceContact', json.dumps(contact)))
		c = RequestContext(request, {
			'jsons': jsons,
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
			purchase_method = user_profile.purchase_method #采购方式
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
		orders = []
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
				if res and res['code'] == 200:
					orders = res['data']['orders']
				else:
					print(res)
					response = create_response(500)
					return response.get_response()

			# price【售价】，purchase_price【结算价】，total_price【售价金额】
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
							model_names = u'规格：' + '/'.join(return_product_info['model_names'])
						else:
							model_names = ''
						product_infos.append({
							'product_name': product_weapp_id2info[product_id][0]['product_name'],
							'model_names': model_names,
							'product_img': product_weapp_id2info[product_id][0]['product_img'],
							'price': return_product_info['purchase_price'] if purchase_method == 1 else '%.2f' % (return_product_info['total_price']/return_product_info['count']),
							'count': return_product_info['count']
						})
					else:
						if return_product_info['model_names']:
							model_names = u'规格：' + '/'.join(return_product_info['model_names'])
						else:
							model_names = ''
						product_infos.append({
							'product_name': return_product_info['name'],
							'model_names': model_names,
							'product_img': return_product_info['thumbnails_url'],
							'price': return_product_info['purchase_price'] if purchase_method == 1 else '%.2f' % (return_product_info['total_price']/return_product_info['count']),
							'count': return_product_info['count']
						})
					if not is_for_list:
						total_weight += return_product_info['weight']
					if purchase_method == 1: #固定底价类型客户
						total_purchase_price += int(return_product_info['count']) * float(return_product_info['purchase_price'])#计算订单总金额
					else: #扣点类型客户
						total_purchase_price += float(return_product_info['total_price'])

				if is_for_list:
					rows.append({
						'id': len(rows),
						'order_id': order_id,
						'order_create_at': order['created_at'],
						'ship_name': order['ship_name'],
						'total_purchase_price': str('%.2f' % total_purchase_price),
						'status': order_status2text[order['status']],
						'order_status': order['status'],
						'product_infos': json.dumps(product_infos),
						'express_company_name': order['express_company_name'],
						'express_number': order['express_number'],
						'leader_name': order['leader_name'],
						'postage': str('%.2f' % order['postage'])
					})
				else:
					rows.append({
						'id': order_id,
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
			#构造response
			response = create_response(200)
			response.data = data
			return response.get_response()
		else:
			return rows