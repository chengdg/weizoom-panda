# -*- coding: utf-8 -*-
__author__ = 'bert'

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
from account.models import *
from product.models import *
from product_catalog import models as catalog_models
from excel_response import ExcelResponse

FIRST_NAV = 'manager'
SECOND_NAV = 'account-no－product-list'

COUNT_PER_PAGE = 20

filter2field = {
	'account_type': 'role'
}

#账号管理列表
class ManagerAccount(resource.Resource):
	app = 'manager'
	resource = 'account_no_product'

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
		
		return render_to_response('manager/account_no_product_list.html', c)

	@login_required
	def api_get(request):
		is_for_list = True if request.GET.get('is_for_list') else False
		cur_page = request.GET.get('page', 1)
		accounts = UserProfile.objects.filter(is_active=True, role=1, product_count=0).order_by('created_at')
		catalogs = catalog_models.ProductCatalog.objects.filter(father_id=-1)
		catalog_id2name = dict((catalog.id,catalog.name) for catalog in catalogs)
		filters = dict([(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET if key.startswith('__f-')])
		name = filters.get('name','')
		username = filters.get('username','')

		if name:
			accounts = accounts.filter(name__icontains=name)
		if username:
			user_ids = [user.id for user in User.objects.filter(username__icontains=username)]
			accounts = accounts.filter(user_id__in=user_ids)

		if is_for_list:
			pageinfo, accounts = paginator.paginate(accounts, cur_page, COUNT_PER_PAGE)

		user_ids = [account.user_id for account in accounts]
		user_id2username = {user.id: user.username for user in User.objects.filter(id__in=user_ids)}
		rows = []
		for account in accounts:
			catalog_names = []
			if account.company_type != '':
				#获得经营类目的名称
				catalog_ids = json.loads(account.company_type)
				for catalog_id in catalog_ids:
					catalog_names.append(catalog_id2name.get(catalog_id, ''))
			catalog_names = ','.join(catalog_names)
			if is_for_list:
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
					'id' : account.id,
					'name' : account.name,
					'username' : user_id2username[account.user_id],
					'companyType' : catalog_names,
					'purchaseMethod' : METHOD2NAME[account.purchase_method] if account.role == 1 else '--',
					'accountType' : ROLE2NAME[account.role],
					'status' : account.status,
					'maxProduct': account.max_product if account.role == CUSTOMER else "--",
					'customerFrom': '渠道' if account.customer_from == 1 else '--',
					'productCount': account.product_count
				})
			else:
				rows.append({
					'id' : account.id,
					'user_id' : account.user_id,
					'phone' : account.phone,
					'name' : account.name,
					'contacter' : account.contacter,
					'purchase_method' : METHOD2NAME[account.purchase_method] if account.role == 1 else '--',
					'username' : user_id2username[account.user_id],
					'role' : ROLE2NAME[account.role],
					'note' : account.note,
					'company_name': account.company_name,
					'productCount': account.product_count
				})
			
		if is_for_list:
			data = {
				'rows': rows,
				'pagination_info': pageinfo.to_dict()
			}
			#构造response
			response = create_response(200)
			response.data = data
			return response.get_response()
		else:
			return rows

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

	# @login_required
	# def api_delete(request):
	# 	account_id = request.POST.get('id','')
	# 	try:
	# 		user_profile = UserProfile.objects.get(id=account_id)
	# 		user_id = user_profile.user_id
	# 		user_profile.delete()
	# 		User.objects.filter(id=user_id).delete()
	# 		products = Product.objects.filter(owner_id=user_id)
	# 		if products:
	# 			product_ids = [product.id for product in products]
	# 			products.delete()
	# 			ProductHasRelationWeapp.objects.filter(product_id__in=product_ids).delete()
	# 		AccountHasSupplier.objects.filter(account_id=account_id).delete()
	# 		response = create_response(200)
	# 		return response.get_response()
	# 	except:
	# 		response = create_response(500)
	# 		response.errMsg = u'该账号不存在，请检查'
	# 		return response.get_response()

class ExportAccounts(resource.Resource):
	app = 'manager'
	resource = 'account_no_product_export'

	@login_required
	def get(request):
		accounts = ManagerAccount.api_get(request)
		titles = [
			u'账号id', u'对应user_id', u'账号类型', u'账号名称', u'登录账号', u'公司名称',
			u'联系人', u'手机号', u'采购方式',u'备注'
		]
		table = []
		table.append(titles)
		for account in accounts:
			table.append([
				account['id'],
				account['user_id'],
				account['role'],
				account['name'],
				account['username'],
				account['company_name'],
				account['contacter'],
				account['phone'],
				account['purchase_method'],
				account['note']
			])
		return ExcelResponse(table, output_name=u'未添加商品账号'.encode('utf8'), force_csv=False)