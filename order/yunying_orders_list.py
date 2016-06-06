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
from account.models import *
from product import models as product_models

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
		cur_page = request.GET.get('page', 1)
		filter_idct = dict([(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET if key.startswith('__f-')])
		customer_name = filter_idct.get('customer_name','')
		from_mall = filter_idct.get('from_mall','')
		order_create_at_range = filter_idct.get('order_create_at','')

		filter_string = ''
		if customer_name:
			print(customer_name)
		if from_mall != '-1':
			print(from_mall)
		if order_create_at_range:
			start_time = order_create_at_range[0]
			end_time = order_create_at_range[1]
			filter_string = filter_string + '&start_time=' + start_time + '&end_time=' + end_time

		print('filter_string:')
		print(filter_string)

		product_has_relations = product_models.ProductHasRelationWeapp.objects.exclude(weapp_product_id='')
		product_ids = []
		api_pids = [product_has_relation.weapp_product_id for product_has_relation in product_has_relations]

		for product_has_relation in product_has_relations:
			if product_has_relation.product_id not in product_ids:
				product_ids.append(product_has_relation.product_id)

		product_weapp_id2seller_name = {}
		products = product_models.Product.objects.filter(id__in=product_ids)
		all_sellers = UserProfile.objects.filter(role=CUSTOMER)
		for api_pid in api_pids:
			if not product_weapp_id2seller_name.has_key(api_pid):
				product_id = product_has_relations.get(weapp_product_id=api_pid).product_id
				owner_id = products.get(id=product_id).owner_id
				seller_name = all_sellers.get(user_id=owner_id).name
				product_weapp_id2seller_name[api_pid] = [seller_name]

		api_pids = '_'.join(api_pids)
		rows = []
		if api_pids != '':
			account_type = 'yunying'
			api_url = 'http://api.zeus.com/panda/order_list/?product_ids={}&account_type={}&page={}'.format(api_pids,account_type,cur_page)
			if filter_string!= '':
				api_url +=  filter_string
			print(api_url)
			url_request = urllib2.Request(api_url)
			res_data = urllib2.urlopen(url_request)
			res = json.loads(res_data.read())
			if res['code'] == 200:
				orders = res['data']['orders']
			else:
				print(res)
				response = create_response(500)
				return response.get_response()

			pageinfo = res['data']['pageinfo']
			pageinfo['total_count'] = pageinfo['object_count']

			for order in orders:
				weapp_product_id = str(order['product_info'][0]['product_id'])
				rows.append({
					'order_id': order['order_id'],
					'order_create_at': order['created_at'],
					'total_purchase_price': str('%.2f' % order['order_money']),
					'customer_name': product_weapp_id2seller_name[weapp_product_id],
					'from_mall': order['store_name']
				})
		else:
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