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
filter2field ={
	'customer_name_query': 'customer_name'
}

class Statistics(resource.Resource):
	app = 'customer'
	resource = 'statistics'

	@login_required
	def get(request):
		"""
		显示商品列表
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV
		})
		
		return render_to_response('customer/statistics.html', c)

	def api_get(request):
		is_export = False
		rows,pageinfo = getCustomerData(request,is_export)
		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}
		response = create_response(200)
		response.data = data
		return response.get_response()

def getCustomerData(request,is_export):
	cur_page = request.GET.get('page', 1)
	user_profiles = UserProfile.objects.filter(role=1, is_active=True) #role{1:客户}

	filter_idct = dict([(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET if key.startswith('__f-')])
	customer_name = filter_idct.get('customer_name','')
	if customer_name:
		user_profiles = user_profiles.filter(name__icontains=customer_name)

	if not is_export:
		pageinfo, user_profiles = paginator.paginate(user_profiles, cur_page, 10, query_string=request.META['QUERY_STRING'])

	user_ids = [user_profile.user_id for user_profile in user_profiles]
	products = product_models.Product.objects.filter(owner_id__in=user_ids).order_by('-id')
	product_ids = ['%s'%product.id for product in products]
	product_has_relations = product_models.ProductHasRelationWeapp.objects.filter(product_id__in=product_ids).exclude(weapp_product_id='')

	user_id2product_id = {}
	for product in products:
		if product.owner_id not in user_id2product_id:
			user_id2product_id[product.owner_id] = [product.id]
		else:
			user_id2product_id[product.owner_id].append(product.id)

	product_id2name = {product.id:product.product_name for product in products}
	#从云商通获取销量
	id2sales = sales_from_weapp(product_has_relations)
	account_ids = [user_profile.id for user_profile in user_profiles]
	account_has_suppliers = AccountHasSupplier.objects.filter(account_id__in=account_ids)
	supplier_ids = []
	for account_has_supplier in account_has_suppliers:
		if str(account_has_supplier.supplier_id) not in supplier_ids:
			supplier_ids.append(str(account_has_supplier.supplier_id))

	api_pids = []

	#构造panda数据库内商品id，与云商通内商品id的关系
	product_weapp_id2product_id = {}
	for product_has_relation in product_has_relations:
		weapp_product_ids = product_has_relation.weapp_product_id.split(';')
		for weapp_product_id in weapp_product_ids:
			api_pids.append(weapp_product_id)
			product_weapp_id2product_id[weapp_product_id] = product_has_relation.product_id

	product_id2time = {}
	for product_has_relation in product_has_relations:
		product_id = product_has_relation.product_id
		if product_id not in product_id2time:
			product_id2time[product_id] = [product_has_relation.created_at.strftime("%Y-%m-%d")]
		else:
			product_id2time[product_id].append(product_has_relation.created_at.strftime("%Y-%m-%d"))
	id2orders = {}		
	supplier_ids = '_'.join(supplier_ids)
	api_pids = '_'.join(api_pids)
	try:
		params = {
			'supplier_ids': supplier_ids
		}
		r = requests.post(ZEUS_HOST+'/panda/order_export_by_supplier/',data=params)
		res = json.loads(r.text)
		if res['code'] == 200:
			orders = res['data']['orders']
			if orders:
				for order in orders:
					if int(order['status']) in [3,4,5]:
						weapp_id = str(order['products'][0]['id'])
						if weapp_id in product_weapp_id2product_id:
							p_id = product_weapp_id2product_id[weapp_id]
							if p_id not in id2orders:
								id2orders[p_id] = [order]
							else:
								id2orders[p_id].append(order)
		else:
			print(res)
	except Exception,e:
		print(e)

	rows = []
	for user in user_profiles:
		product_ids = [] if user.user_id not in user_id2product_id else user_id2product_id[user.user_id]
		product_infos = []
		total_sales = 0 #总销量
		total_weizoom_card_money = 0 #微众卡
		total_coupon_money = 0 #优惠券
		total_order_number = 0 #订单数
		total_final_price = 0 #现金
		total_order_money = 0 #总金额
		brand_time = []
		if product_ids:
			for product_id in product_ids:
				name = '' if product_id not in product_id2name else product_id2name[product_id]
				sale = 0 if product_id not in id2sales else id2sales[product_id]
				times = '' if product_id not in product_id2time else product_id2time[product_id]
				if times:
					brand_time.extend(times)
				total_sales += sale
				product_infos.append({
					'name': name,
					'sales': '%s' %sale,
					'time': '' if not times else min(times)
				})
				if product_id in id2orders:
					orders = id2orders[product_id]
					total_order_number += len(orders)
					for order in orders:
						products = order['products']
						total_weizoom_card_money += order['weizoom_card_money'] #微众卡金额
						total_coupon_money += order['coupon_money'] #优惠券金额
						total_final_price += order['final_price'] #现金
						for product in products:
							order_money = product['count'] * product['purchase_price']
							total_order_money += order_money
		rows.append({
			'user_id': user.user_id,
			'customer_name': user.name,
			'total_order_number': '%s' %total_order_number,
			'total_sales': '%s' %total_sales,
			'total_weizoom_card_money': '%.2f' %total_weizoom_card_money,
			'total_coupon_money': '%.2f' %total_coupon_money,
			'total_final_price': '%.2f' %total_final_price,
			'total_order_money': '%.2f' %total_order_money,
			'brand_time': '' if not brand_time else min(brand_time),
			'feedback': u'查看报告',
			'product_infos': json.dumps(product_infos)
		})

	if is_export:
		return rows
	else:
		return rows,pageinfo