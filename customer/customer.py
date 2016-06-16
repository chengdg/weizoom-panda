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
from panda.settings import ZEUS_HOST
import nav
import urllib2
import urllib

FIRST_NAV = 'customer'
SECOND_NAV = 'customer'

class Customer(resource.Resource):
	app = 'customer'
	resource = 'customer'

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
		
		return render_to_response('customer/customer.html', c)

	def api_get(request):
		cur_page = request.GET.get('page', 1)
		user_profiles = UserProfile.objects.filter(role=1) #role{1:客户}
		products = product_models.Product.objects.all()
		# user_id2product_name = {}
		# for product in products:
		# 	if product.owner_id not in user_id2product_name:
		# 		user_id2product_name[product.owner_id] = [product.product_name]
		# 	else:
		# 		user_id2product_name[product.owner_id].append(product.product_name)

		user_id2product_id = {}
		for product in products:
			if product.owner_id not in user_id2product_id:
				user_id2product_id[product.owner_id] = [product.id]
			else:
				user_id2product_id[product.owner_id].append(product.id)

		product_id2name = {product.id:product.product_name for product in products}
		pageinfo, user_profiles = paginator.paginate(user_profiles, cur_page, 10, query_string=request.META['QUERY_STRING'])

		products = product_models.Product.objects.all().order_by('-id')
		product_ids = ['%s'%product.id for product in products]
		if len(product_ids)>1:
			product_ids = '_'.join(product_ids)
		else:
			product_ids = '%s' %product_ids[0]
		# 请求接口获得数据
		url = ZEUS_HOST+'/mall/product_sales/?product_ids='+product_ids
		url_request = urllib2.Request(url)
		opener = urllib2.urlopen(url_request)
		sales = []
		res = opener.read()
		if json.loads(res)['code'] == 200:
			sales = json.loads(res)['data']
		else:
			response = create_response(500)
			return response.get_response()

		rows = []
		for user in user_profiles:
			product_ids = [] if user.user_id not in user_id2product_id else user_id2product_id[user.user_id]
			product_infos = []
			total_sales = 0
			if product_ids:
				for product_id in product_ids:
					name = '' if product_id not in product_id2name else product_id2name[product_id]
					sale = 0 if product.id not in sales else sales[product_id]
					total_sales += sale
					product_infos.append({
						'name': name,
						'sales': '%s' %sale,
						'time': '2016-06-01'
					})

			rows.append({
				'user_id': user.user_id,
				'customer_name': user.name,
				'total_orders': 500,
				'total_sales': '%s' %total_sales,
				'total_fans': 808,
				'product_infos': json.dumps(product_infos)
			})
		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}
		response = create_response(200)
		response.data = data
		return response.get_response()