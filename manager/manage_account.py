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
		rows = []
		data = {
			'rows': rows,
		}

		#构造response
		response = create_response(200)
		response.data = data

		return response.get_response()

class AccountCreate(resource.Resource):
	app = 'manager'
	resource = 'account_create'

	@login_required
	def get(request):
		"""
		响应GET
		"""
		product_id = request.GET.get('id', None)
		jsons = {'items':[]}
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

def check_username(request):
	"""
	创建用户时，检查登录账号是否存在
	"""
	username = request.GET.get('username','')
	user = User.objects.filter(username=username)
	if user:
		response = create_response(500)
		response.innerErrMsg = unicode_full_stack()
		response.errMsg = u'该登录名已存在'
		return response.get_response()
	else:
		response = create_response(200)
		return response.get_response()