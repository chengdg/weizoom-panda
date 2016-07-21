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
from account.models import *
from product.models import *
from product_catalog import models as catalog_models
from excel_response import ExcelResponse

FIRST_NAV = 'manager'
SECOND_NAV = 'account-list'

COUNT_PER_PAGE = 20

filter2field = {
	'account_type': 'role'
}

#账号管理列表
class ManagerAccount(resource.Resource):
	app = 'manager'
	resource = 'account'

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
		
		return render_to_response('manager/account_list.html', c)

	@login_required
	def api_get(request):
		is_for_list = True if request.GET.get('is_for_list') else False
		cur_page = request.GET.get('page', 1)
		accounts = UserProfile.objects.filter(is_active = True).exclude(role=MANAGER).order_by('-id')
		catalogs = catalog_models.ProductCatalog.objects.filters(father_catalog = -1)
		filters = dict([(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET if key.startswith('__f-')])
		name = filters.get('name','')
		username = filters.get('username','')
		role = filters.get('role','')
		if name:
			accounts = accounts.filter(name__icontains=name)
		if username:
			user_ids = [user.id for user in User.objects.filter(username__icontains = username)]
			accounts = accounts.filter(user_id__in=user_ids)
		if role:
			accounts = accounts.filter(role=role)
		if is_for_list:
			pageinfo, accounts = paginator.paginate(accounts, cur_page, COUNT_PER_PAGE)

		user_ids = [account.user_id for account in accounts]
		user_id2username = {user.id: user.username for user in User.objects.filter(id__in=user_ids)}
		rows = []
		date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		for account in accounts:
			#关闭已过期的账号/开启可以登录的账号
			if account.valid_time_from and account.valid_time_to:
				valid_time_from = account.valid_time_from.strftime("%Y-%m-%d %H:%M:%S")
				valid_time_to = account.valid_time_to.strftime("%Y-%m-%d %H:%M:%S")
				if valid_time_from <= date_now and date_now < valid_time_to and account.status != 0:
					account.status = 1
					account.save()
				elif date_now >= valid_time_to or date_now <= valid_time_from:
					account.status = 2
					account.save()
			if is_for_list:
				rows.append({
					'id' : account.id,
					'name' : account.name,
					'username' : user_id2username[account.user_id],
					'company_type' : account.company_type if account.role==1 else '--',
					'purchase_method' : METHOD2NAME[account.purchase_method] if account.role==1 else '--',
					'account_type' : ROLE2NAME[account.role],
					'status' : account.status
				})
			else:
				rows.append({
					'name' : account.name,
					'username' : user_id2username[account.user_id],
					'role' : ROLE2NAME[account.role],
					'note' : account.note
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

	@login_required
	def api_post(request):
		#更新账户状态
		account_id = request.POST.get('id','')
		status = request.POST.get('method','')
		if status == 'close':
			change_to_status = 0
		else:
			change_to_status = 1
		try:
			UserProfile.objects.filter(manager_id = request.user.id,id = account_id).update(
				status = change_to_status
			)
			response = create_response(200)
			return response.get_response()
		except:
			response = create_response(500)
			response.errMsg = u'该账号不存在，请检查'
			return response.get_response()

	@login_required
	def api_delete(request):
		account_id = request.POST.get('id','')
		try:
			user_profile = UserProfile.objects.get(id = account_id)
			user_id = user_profile.user_id
			user_profile.delete()
			User.objects.filter(id = user_id).delete()
			products = Product.objects.filter(owner_id=user_id)
			if products:
				product_ids = [product.id for product in products]
				products.delete()
				ProductHasRelationWeapp.objects.filter(product_id__in=product_ids).delete()
			AccountHasSupplier.objects.filter(account_id=account_id).delete()
			response = create_response(200)
			return response.get_response()
		except:
			response = create_response(500)
			response.errMsg = u'该账号不存在，请检查'
			return response.get_response()

class ExportAccounts(resource.Resource):
	app = 'manager'
	resource = 'account_export'

	@login_required
	def get(request):
		accounts = ManagerAccount.api_get(request)
		titles = [
			u'账号类型', u'账号名称',u'登录账号', u'备注'
		]
		table = []
		table.append(titles)
		for account in accounts:
			table.append([
				account['role'],
				account['name'],
				account['username'],
				account['note'],
			])
		return ExcelResponse(table,output_name=u'账号管理文件'.encode('utf8'),force_csv=False)