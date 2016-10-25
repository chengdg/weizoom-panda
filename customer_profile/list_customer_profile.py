# -*- coding: utf-8 -*-
__author__ = 'lihanyi'

import json
import time
import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.exceptionutil import unicode_full_stack
from core import resource
from core.jsonresponse import create_response
from core import paginator
from util import db_util
import nav
import requests
from account.models import *
from product.models import *
from product_catalog import models as catalog_models
from excel_response import ExcelResponse
from panda.settings import AXE_HOST

FIRST_NAV = 'customer_profile'
SECOND_NAV = 'customer-profile-list'

COUNT_PER_PAGE = 20

filter2field = {
	'account_type': 'role'
}

#账号管理列表
class CustomerProfileList(resource.Resource):
	app = 'customer_profile'
	resource = 'list'

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
		
		return render_to_response('customer_profile/list_customer_profile.html', c)

	@login_required
	def api_get(request):
		cur_page = request.GET.get('page', 1)
		accounts = UserProfile.objects.filter(is_active=True).exclude(role=MANAGER).order_by('-id')
		catalogs = catalog_models.ProductCatalog.objects.filter(father_id=-1)
		catalog_id2name = dict((catalog.id,catalog.name) for catalog in catalogs)
		filters = dict([(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET if key.startswith('__f-')])
		company_name = filters.get('companyName','')
		username = filters.get('username','')
		role = filters.get('accountType','')
		status = filters.get('status','')
		# customer_from = filters.get('customerFrom','')
		if company_name:
			accounts = accounts.filter(company_name__icontains=company_name)
		if username:
			user_ids = [user.id for user in User.objects.filter(username__icontains=username)]
			accounts = accounts.filter(user_id__in=user_ids)
		if role:
			accounts = accounts.filter(role=role)
		if status:
			if status == '1':
				accounts = accounts.filter(status=status)
			else:
				accounts = accounts.exclude(status=1)
		# if customer_from: 客户来源暂时渠道没有接口实现，先注释
		# 	print customer_from

		pageinfo, accounts = paginator.paginate(accounts, cur_page, COUNT_PER_PAGE)

		user_ids = [account.user_id for account in accounts]
		user_id2username = {user.id: user.username for user in User.objects.filter(id__in=user_ids)}
		rows = []
		date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		for account in accounts:
			customerFrom = '--' 
			if account.role == 1 :
				catalog_names = []
				if account.company_type != '':
					#获得经营类目的名称
					catalog_ids = json.loads(account.company_type)
					for catalog_id in catalog_ids:
						catalog_names.append(catalog_id2name.get(catalog_id, ''))
				catalog_names = ','.join(catalog_names)
			else:
				catalog_names = '--'

			rows.append({
				'id': account.id,
				'name': account.name,
				'companyName': account.company_name,
				'username': user_id2username[account.user_id],
				'companyType': catalog_names,
				'purchaseMethod': METHOD2NAME[account.purchase_method] if account.role == 1 else '--',
				'createdAt': account.created_at.strftime("%Y-%m-%d %H:%M:%S"),
				'status': account.status,
				'maxProduct': account.max_product if account.role == CUSTOMER else '--',
				'customerFrom': customerFrom
			})

		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}
		#构造response
		response = create_response(200)
		response.data = data
		return response.get_response()


	# @login_required
	# def api_post(request):
	# 	#更新账户状态
	# 	account_id = request.POST.get('id','')
	# 	status = request.POST.get('method','')
	# 	if status == 'close':
	# 		change_to_status = 0
	# 	else:
	# 		change_to_status = 1
	# 	try:
	# 		UserProfile.objects.filter(id=account_id).update(
	# 			status = change_to_status
	# 		)
	# 		response = create_response(200)
	# 		return response.get_response()
	# 	except:
	# 		response = create_response(500)
	# 		response.errMsg = u'该账号不存在，请检查'
	# 		return response.get_response()