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
import nav

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
		rows = []
		user_profiles = UserProfile.objects.filter(role=1) #role{1:客户}
		products = product_models.Product.objects.all()
		user_id2product_name = {}
		for product in products:
			if product.owner_id not in user_id2product_name:
				user_id2product_name[product.owner_id] = [product.product_name]
			else:
				user_id2product_name[product.owner_id].append(product.product_name)
		pageinfo, user_profiles = paginator.paginate(user_profiles, cur_page, 10, query_string=request.META['QUERY_STRING'])

		for user in user_profiles:
			product_name = [] if user.user_id not in user_id2product_name else user_id2product_name[user.user_id]
			product_infos = []
			if product_name:
				for name in product_name:
					product_infos.append({
						'name': name,
						'sales': 500,
						'time': '2016-06-01'
					})

			rows.append({
				'user_id': user.user_id,
				'customer_name': user.name,
				'total_orders': 500,
				'total_sales': 1500,
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