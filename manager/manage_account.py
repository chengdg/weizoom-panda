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

#账号管理列表
class Account(resource.Resource):
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

	def api_get(request):
		accounts = UserProfile.objects.filter(manager_id = request.user.id,is_active = True)
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
		}

		#构造response
		response = create_response(200)
		response.data = data

		return response.get_response()

#创建账号
class AccountCreate(resource.Resource):
	app = 'manager'
	resource = 'account_create'

	@login_required
	def get(request):
		"""
		响应GET
		"""
		user_profile_id = request.GET.get('id', None)
		jsons = {'items':[]}
		if user_profile_id:
			user_profile = UserProfile.objects.get(id=user_profile_id)
			user_profile_data = {
				'id': user_profile.id,
				'name': user_profile.name,
				'username': User.objects.get(id=user_profile.user_id).username,
				'account_type': user_profile.role,
				'note': user_profile.note,
			}
			jsons['items'].append(('user_profile_data', json.dumps(user_profile_data)))
		else:
			jsons['items'].append(('user_profile_data', json.dumps(None)))

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
			'jsons': jsons
		})

		return render_to_response('manager/account_create.html', c)

	def api_put(request):
		post = request.POST
		account_type = post.get('account_type','')
		name = post.get('name','')
		username = post.get('username','')
		password = post.get('password','')
		note = post.get('note','')

		if not check_username_valid(username):
			response = create_response(500)
			response.errMsg = u'登录账号已存在，请重新输入'
			return response.get_response()
		try:
			user = User.objects.create_user(username,username+'@weizoom.com',password)
			user.first_name = name
			user.save()
			user_profile = UserProfile.objects.get(user=user)
			user_profile.manager_id = request.user.id
			user_profile.role = account_type
			user_profile.name = name
			user_profile.note = note
			user_profile.save()
			response = create_response(200)
		except Exception,e:
			print(e)
			print('===========================')
			response = create_response(500)
			response.errMsg = u'创建账号失败'
			response.innerErrMsg = unicode_full_stack()
		return response.get_response()

def check_username_valid(username):
	"""
	创建用户时，检查登录账号是否存在
	"""
	user = User.objects.filter(username = username)
	return False if user else True