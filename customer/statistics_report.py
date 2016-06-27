# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from core import resource
from core.jsonresponse import create_response
from core import paginator

from resource import models as resource_models
from product import models as product_models
from account.models import *
from util import string_util
from util import db_util
from panda.settings import ZEUS_HOST
from product.sales_from_weapp import sales_from_weapp
import nav
import requests

FIRST_NAV = 'customer'
SECOND_NAV = 'customer'

class StatisticsReport(resource.Resource):
	app = 'customer'
	resource = 'statistics_report'

	@login_required
	def get(request):
		"""
		显示商品列表
		"""
		user_id = request.GET.get('id', '')
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
			'user_id': user_id
		})
		
		return render_to_response('customer/statistics_report.html', c)

	def api_get(request):
		user_id = request.GET.get('user_id', '')
		products = product_models.Product.objects.filter(owner_id=user_id)
		product_ids = [int(product.id) for product in products]
		product_has_relations = product_models.ProductHasRelationWeapp.objects.filter(product_id__in=product_ids).exclude(weapp_product_id='')
		api_pids = []
		#构造panda数据库内商品id，与云商通内商品id的关系
		for product_has_relation in product_has_relations:
			weapp_product_ids = product_has_relation.weapp_product_id.split(';')
			for weapp_product_id in weapp_product_ids:
				#获得所有绑定过云商通的云商通商品id
				api_pids.append(weapp_product_id)
		
		product_weapp_id2product_id = {}
		for product_has_relation in product_has_relations:
			weapp_product_ids = product_has_relation.weapp_product_id.split(';')
			for weapp_product_id in weapp_product_ids:
				#获得所有绑定过云商通的云商通商品id
				product_weapp_id2product_id[weapp_product_id] = product_has_relation.product_id
		
		product_id2time = {}
		for product_has_relation in product_has_relations:
			product_id = product_has_relation.product_id
			if product_id not in product_id2time:
				product_id2time[product_id] = [product_has_relation.created_at]
			else:
				product_id2time[product_id].append(product_has_relation.created_at)
		api_pids = '_'.join(api_pids)
		print('api_pids:')
		print(api_pids)

		try:
			webapp_id2store_username = {}
			account_zypt_infos = []
			params = {
				'mall_type': 1
			}
			r = requests.get(ZEUS_HOST+'/account/zypt_info/',params=params)
			res = json.loads(r.text)
			if res['code'] == 200:
				account_zypt_infos = res['data']
				for account_zypt_info in account_zypt_infos:
					if account_zypt_info['store_name'] == u'微众白富美':
						webapp_id2store_username[account_zypt_info['webapp_id']] = 'weizoom_baifumei'
					elif account_zypt_info['store_name'] == u'微众俱乐部':
						webapp_id2store_username[account_zypt_info['webapp_id']] = 'weizoom_club'
					elif account_zypt_info['store_name'] == u'微众家':
						webapp_id2store_username[account_zypt_info['webapp_id']] = 'weizoom_jia'
					elif account_zypt_info['store_name'] == u'微众妈妈':
						webapp_id2store_username[account_zypt_info['webapp_id']] = 'weizoom_mama'
					elif account_zypt_info['store_name'] == u'微众商城':
						webapp_id2store_username[account_zypt_info['webapp_id']] = 'weizoom_shop'
					elif account_zypt_info['store_name'] == u'微众学生':
						webapp_id2store_username[account_zypt_info['webapp_id']] = 'weizoom_xuesheng'
					else:
						# webapp_id2store_username[account_zypt_info['webapp_id']] = [account_zypt_info['store_name']]
						webapp_id2store_username[account_zypt_info['webapp_id']] = 'weizoom_baifumei'
			else:
				print(res)
		except Exception,e:
			print "=====error====="
			print(e)

		rows = []
		#商品id与各个平台对应的销量之间的关系
		pid2weizoom_baifumei_sales = {}
		weizoom_baifumei_sales = 0
		pid2weizoom_club_sales = {}
		weizoom_club_sales = 0
		pid2weizoom_jia_sales = {}
		weizoom_jia_sales = 0
		pid2weizoom_mama_sales = {}
		weizoom_mama_sales = 0
		pid2weizoom_shop_sales = {}
		weizoom_shop_sales = 0
		pid2weizoom_xuesheng_sales = {}
		weizoom_xuesheng_sales = 0

		if api_pids != '':
			params = {'product_ids': api_pids}
			r = requests.get(ZEUS_HOST+'/panda/order_export/',params=params)
			res = json.loads(r.text)
			if res['code'] == 200:
				orders = res['data']['orders']
			else:
				print(res)
				response = create_response(500)
				return response.get_response()
			
			# #获得所有的自营平台的总销量
			# for order in orders:
			# 	store_username = webapp_id2store_username[order['webapp_id']]
			# 	if store_username == 'weizoom_baifumei':
			# 		weizoom_baifumei_sales += 1
			# 	elif store_username == 'weizoom_club':
			# 		weizoom_club_sales += 1
			# 	elif store_username == 'weizoom_jia':
			# 		weizoom_jia_sales += 1
			# 	elif store_username == 'weizoom_mama':
			# 		weizoom_mama_sales += 1
			# 	elif store_username == 'weizoom_shop':
			# 		weizoom_shop_sales += 1
			# 	elif store_username == 'weizoom_xuesheng':
			# 		weizoom_xuesheng_sales += 1

			#获得云商通商品id与对应的自营平台的总销量之间的关系
			for order in orders:
				store_username = webapp_id2store_username[order['webapp_id']]
				return_product_infos = order['products'] #返回的订单数据
				for return_product_info in return_product_infos:
					product_weapp_id = str(return_product_info['id'])
					product_id = product_weapp_id2product_id[product_weapp_id]
					if store_username == 'weizoom_baifumei':
						if not pid2weizoom_baifumei_sales.has_key(product_id):
							pid2weizoom_baifumei_sales[product_id] = weizoom_baifumei_sales
					if not pid2weizoom_club_sales.has_key(product_id):
						pid2weizoom_club_sales[product_id] = weizoom_club_sales
					if not pid2weizoom_jia_sales.has_key(product_id):
						pid2weizoom_jia_sales[product_id] = weizoom_jia_sales
					if not pid2weizoom_mama_sales.has_key(product_id):
						pid2weizoom_mama_sales[product_id] = weizoom_mama_sales
					if not pid2weizoom_shop_sales.has_key(product_id):
						pid2weizoom_shop_sales[product_id] = weizoom_shop_sales
					if not pid2weizoom_xuesheng_sales.has_key(product_id):
						pid2weizoom_xuesheng_sales[product_id] = weizoom_xuesheng_sales

			for product in products:
				product_sales = pid2weizoom_baifumei_sales[product.id]+pid2weizoom_club_sales[product.id]+pid2weizoom_jia_sales[product.id]+pid2weizoom_mama_sales[product.id]+pid2weizoom_shop_sales[product.id]+pid2weizoom_xuesheng_sales[product.id]
				rows.append({
					'product_name': product.product_name,
					'weizoom_baifumei' : pid2weizoom_baifumei_sales[product.id],
					'weizoom_club': pid2weizoom_club_sales[product.id],
					'weizoom_jia': pid2weizoom_jia_sales[product.id],
					'weizoom_mama': pid2weizoom_mama_sales[product.id],
					'weizoom_shop': pid2weizoom_shop_sales[product.id],
					'weizoom_xuesheng': pid2weizoom_xuesheng_sales[product.id],
					'product_sales': product_sales
				})
			# rows_all.append({
			# 	'first_week': '',
			# 	'second_week': '',
			# 	'third_week': '',
			# 	'fourth_week': '',
			# 	'all_purchase_number': '',
			# 	'one_time_purchase': '',
			# 	're_purchase':'',
			# 	'weizoom_baifumei_orders_number': '',
			# 	'weizoom_club_orders_number': '',
			# 	'weizoom_jia_orders_number': '',
			# 	'weizoom_mama_orders_number': '',
			# 	'weizoom_shop_orders_number': '',
			# 	'weizoom_xuesheng_orders_number': ''
			# })
		data = {
			'rows': rows,
			# 'rows_all': rows_all
		}
		response = create_response(200)
		response.data = data
		return response.get_response()

class StatisticsReportData(resource.Resource):
	app = 'customer'
	resource = 'statistics_report_date'

	def api_get(request):
		user_id = request.GET.get('user_id', '')
		products = product_models.Product.objects.filter(owner_id=user_id)
		product_ids = [int(product.id) for product in products]
		product_has_relations = product_models.ProductHasRelationWeapp.objects.filter(product_id__in=product_ids).exclude(weapp_product_id='')
		api_pids = []
		#构造panda数据库内商品id，与云商通内商品id的关系
		for product_has_relation in product_has_relations:
			weapp_product_ids = product_has_relation.weapp_product_id.split(';')
			for weapp_product_id in weapp_product_ids:
				#获得所有绑定过云商通的云商通商品id
				api_pids.append(weapp_product_id)
		
		product_weapp_id2product_id = {}
		for product_has_relation in product_has_relations:
			weapp_product_ids = product_has_relation.weapp_product_id.split(';')
			for weapp_product_id in weapp_product_ids:
				#获得所有绑定过云商通的云商通商品id
				product_weapp_id2product_id[weapp_product_id] = product_has_relation.product_id
		
		product_id2time = {}
		for product_has_relation in product_has_relations:
			product_id = product_has_relation.product_id
			if product_id not in product_id2time:
				product_id2time[product_id] = [product_has_relation.created_at]
			else:
				product_id2time[product_id].append(product_has_relation.created_at)
		api_pids = '_'.join(api_pids)
		print('api_pids:')
		print(api_pids)

		try:
			webapp_id2store_username = {}
			account_zypt_infos = []
			params = {
				'mall_type': 1
			}
			r = requests.get(ZEUS_HOST+'/account/zypt_info/',params=params)
			res = json.loads(r.text)
			if res['code'] == 200:
				account_zypt_infos = res['data']
				for account_zypt_info in account_zypt_infos:
					if account_zypt_info['store_name'] == u'微众白富美':
						webapp_id2store_username[account_zypt_info['webapp_id']] = 'weizoom_baifumei'
					elif account_zypt_info['store_name'] == u'微众俱乐部':
						webapp_id2store_username[account_zypt_info['webapp_id']] = 'weizoom_club'
					elif account_zypt_info['store_name'] == u'微众家':
						webapp_id2store_username[account_zypt_info['webapp_id']] = 'weizoom_jia'
					elif account_zypt_info['store_name'] == u'微众妈妈':
						webapp_id2store_username[account_zypt_info['webapp_id']] = 'weizoom_mama'
					elif account_zypt_info['store_name'] == u'微众商城':
						webapp_id2store_username[account_zypt_info['webapp_id']] = 'weizoom_shop'
					elif account_zypt_info['store_name'] == u'微众学生':
						webapp_id2store_username[account_zypt_info['webapp_id']] = 'weizoom_xuesheng'
					else:
						# webapp_id2store_username[account_zypt_info['webapp_id']] = [account_zypt_info['store_name']]
						webapp_id2store_username[account_zypt_info['webapp_id']] = 'weizoom_baifumei'
			else:
				print(res)
		except Exception,e:
			print "=====error====="
			print(e)

		rows = []
		#商品id与各个平台对应的销量之间的关系
		pid2weizoom_baifumei_sales = {}
		weizoom_baifumei_sales = 0
		pid2weizoom_club_sales = {}
		weizoom_club_sales = 0
		pid2weizoom_jia_sales = {}
		weizoom_jia_sales = 0
		pid2weizoom_mama_sales = {}
		weizoom_mama_sales = 0
		pid2weizoom_shop_sales = {}
		weizoom_shop_sales = 0
		pid2weizoom_xuesheng_sales = {}
		weizoom_xuesheng_sales = 0

		if api_pids != '':
			params = {'product_ids': api_pids}
			r = requests.get(ZEUS_HOST+'/panda/order_export/',params=params)
			res = json.loads(r.text)
			if res['code'] == 200:
				orders = res['data']['orders']
			else:
				print(res)
				response = create_response(500)
				return response.get_response()
			
			#获得所有的自营平台的总销量
			for order in orders:
				store_username = webapp_id2store_username[order['webapp_id']]
				if store_username == 'weizoom_baifumei':
					weizoom_baifumei_sales += 1
				elif store_username == 'weizoom_club':
					weizoom_club_sales += 1
				elif store_username == 'weizoom_jia':
					weizoom_jia_sales += 1
				elif store_username == 'weizoom_mama':
					weizoom_mama_sales += 1
				elif store_username == 'weizoom_shop':
					weizoom_shop_sales += 1
				elif store_username == 'weizoom_xuesheng':
					weizoom_xuesheng_sales += 1

			#获得云商通商品id与对应的自营平台的总销量之间的关系
			for order in orders:
				return_product_infos = order['products'] #返回的订单数据
				for return_product_info in return_product_infos:
					product_weapp_id = str(return_product_info['id'])
					product_id = product_weapp_id2product_id[product_weapp_id]
					if not pid2weizoom_baifumei_sales.has_key(product_id):
						pid2weizoom_baifumei_sales[product_id] = weizoom_baifumei_sales
					if not pid2weizoom_club_sales.has_key(product_id):
						pid2weizoom_club_sales[product_id] = weizoom_club_sales
					if not pid2weizoom_jia_sales.has_key(product_id):
						pid2weizoom_jia_sales[product_id] = weizoom_jia_sales
					if not pid2weizoom_mama_sales.has_key(product_id):
						pid2weizoom_mama_sales[product_id] = weizoom_mama_sales
					if not pid2weizoom_shop_sales.has_key(product_id):
						pid2weizoom_shop_sales[product_id] = weizoom_shop_sales
					if not pid2weizoom_xuesheng_sales.has_key(product_id):
						pid2weizoom_xuesheng_sales[product_id] = weizoom_xuesheng_sales

			# for product in products:
			# 	product_sales = pid2weizoom_baifumei_sales[product.id]+pid2weizoom_club_sales[product.id]+pid2weizoom_jia_sales[product.id]+pid2weizoom_mama_sales[product.id]+pid2weizoom_shop_sales[product.id]+pid2weizoom_xuesheng_sales[product.id]
			# 	rows.append({
			# 		'product_name': product.product_name,
			# 		'weizoom_baifumei' : pid2weizoom_baifumei_sales[product.id],
			# 		'weizoom_club': pid2weizoom_club_sales[product.id],
			# 		'weizoom_jia': pid2weizoom_jia_sales[product.id],
			# 		'weizoom_mama': pid2weizoom_mama_sales[product.id],
			# 		'weizoom_shop': pid2weizoom_shop_sales[product.id],
			# 		'weizoom_xuesheng': pid2weizoom_xuesheng_sales[product.id],
			# 		'product_sales': product_sales
			# 	})
			rows.append({
				'first_week': '',
				'second_week': '',
				'third_week': '',
				'fourth_week': '',
				'all_purchase_number': '',
				'one_time_purchase': '',
				're_purchase':'',
				'weizoom_baifumei_orders_number': '11',
				'weizoom_club_orders_number': '',
				'weizoom_jia_orders_number': '',
				'weizoom_mama_orders_number': '',
				'weizoom_shop_orders_number': '',
				'weizoom_xuesheng_orders_number': ''
			})
		data = {
			'rows': rows,
			# 'rows_all': rows_all
		}
		response = create_response(200)
		response.data = data
		return response.get_response()