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

from util import string_util
from account import models as account_models
from product import models as product_models
from panda.settings import ZEUS_HOST
from util import db_util
import models as fans_models
import nav
import requests

filter2field ={
	'status': 'status',
	'recommend_time': 'recommend_time'
}

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

FIRST_NAV = 'fans'
SECOND_NAV = 'fans'

class Fans(resource.Resource):
	app = 'fans'
	resource = 'fans'

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
		
		return render_to_response('fans/fans.html', c)

	def api_get(request):
		cur_page = request.GET.get('page', 1)
		filter_idct = dict([(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET if key.startswith('__f-')])
		status = filter_idct.get('status',-1)
		# recommend_time = filter_idct.get('recommend_time__range','')
		user_has_fans = fans_models.UserHasFans.objects.filter(user_id=request.user.id)
		#查询
		if status != -1:
			user_has_fans = user_has_fans.filter(status=status)

		pageinfo, user_has_fans = paginator.paginate(user_has_fans, cur_page, 10, query_string=request.META['QUERY_STRING'])
		fans_id = [fans.fans_id for fans in user_has_fans]
		user_ids = [user.user_id for user in user_has_fans]
		fans = fans_models.Fans.objects.filter(id__in=fans_id)
		fans_id2fans = {fan.id:fan for fan in fans}

		products = product_models.Product.objects.filter(owner_id__in=user_ids)
		product_ids = [product.id for product in products]
		product_id2name = {product.id:product.product_name for product in products}

		product_has_relations = product_models.ProductHasRelationWeapp.objects.filter(product_id__in=product_ids).exclude(weapp_product_id='')
		product_weapp_id2product_id = {}
		for product_has_relation in product_has_relations:
			weapp_product_ids = product_has_relation.weapp_product_id.split(';')
			for weapp_product_id in weapp_product_ids:
				#获得所有绑定过云商通的云商通商品id
				product_weapp_id2product_id[weapp_product_id] = product_has_relation.product_id

		user_profiles = account_models.UserProfile.objects.filter(user_id__in=user_ids)
		account_ids = [user_profile.id for user_profile in user_profiles]
		account_has_suppliers = account_models.AccountHasSupplier.objects.filter(account_id__in=account_ids)
		supplier_ids = []
		for account_has_supplier in account_has_suppliers:
			if str(account_has_supplier.supplier_id) not in supplier_ids:
				supplier_ids.append(str(account_has_supplier.supplier_id))

		supplier_ids = '_'.join(supplier_ids)
		if supplier_ids != '':
			orders = []
			try:
				params = {
					'supplier_ids': supplier_ids
				}
				r = requests.post(ZEUS_HOST+'/panda/order_export_by_supplier/',data=params)
				res = json.loads(r.text)
				if res['code'] == 200:
					orders = res['data']['orders']
				else:
					print(res)
			except Exception,e:
				print(e)
			print('===orders===',orders)
			if orders:
				order_id2order = {}
				for order in orders:
					order_id = order['order_id']
					product_infos = order['products']
					total_count = 0
					total_order_money = 0
					product_name = ''
					purchase_price = 0
					for product in product_infos:
						total_count += product['count']
						weapp_product_id = str(product['id'])
						product_id = -1 if weapp_product_id not in product_weapp_id2product_id else product_weapp_id2product_id[weapp_product_id]
						product_name = product['name'] if product_id not in product_id2name else product_id2name[product_id]
						purchase_price = product['purchase_price']
						order_money = product['count'] * purchase_price
						total_order_money += order_money

					order_id2order[order_id] = {
						'order_id': order_id,
						'product_name': product_name,
						'purchase_price': '%.2f' %purchase_price,
						'total_count': total_count,
						'total_order_money': '%.2f' %total_order_money,
						'status': order_status2text[order['status']]
					}

		rows=[]
		for user_fans in user_has_fans:
			if user_fans.fans_id in fans_id2fans:
				fans = fans_id2fans[user_fans.fans_id]
				order_id = user_fans.related_order_id
				order_ids = order_id.split('_')
				order_infos = []
				for o_id in order_ids:
					if o_id in order_id2order:
						order_infos.append(order_id2order[o_id])

				status = user_fans.status
				rows.append({
					'fans_pic': fans.fans_url,
					'fans_id': fans.weibo_id,
					'user_id': user_fans.id,
					'purchase_index': fans.purchasing_index * 10,
					'diffusion_index': fans.spread_index * 10,
					'status': fans_models.STATUS2NAME[status],
					'order_id': user_fans.related_order_id,
					'order_infos': '' if not order_infos else json.dumps(order_infos)
				})
		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}
		response = create_response(200)
		response.data = data
		return response.get_response()