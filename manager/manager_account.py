# -*- coding: utf-8 -*-
import json
import time

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


FIRST_NAV = 'manager'
SECOND_NAV = 'account-list'

COUNT_PER_PAGE = 10

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
		cur_page = request.GET.get('page', 1)
		accounts = UserProfile.objects.filter(manager_id = request.user.id,is_active = True).order_by('-id')

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
		pageinfo, accounts = paginator.paginate(accounts, cur_page, COUNT_PER_PAGE)

		user_ids = [account.user_id for account in accounts]
		user_id2username = {user.id: user.username for user in User.objects.filter(id__in=user_ids)}
		rows = []
		for account in accounts:
			rows.append({
				'id' : account.id,
				'name' : account.name,
				'username' : user_id2username[account.user_id],
				'status' : account.status
			})
		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}

		#构造response
		response = create_response(200)
		response.data = data
		return response.get_response()


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
			UserProfile.objects.filter(manager_id = request.user.id,id = account_id).update(
				is_active = False
			)
			response = create_response(200)
			return response.get_response()
		except:
			response = create_response(500)
			response.errMsg = u'该账号不存在，请检查'
			return response.get_response()