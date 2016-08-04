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
from core.exceptionutil import unicode_full_stack
from core import paginator

from util import string_util
from account import models as account_models
from product import models as product_models
from panda.settings import ZEUS_HOST
from util import db_util
import nav
import models

FIRST_NAV = 'freight_service'
SECOND_NAV = 'freight'

class freight(resource.Resource):
	app = 'freight_service'
	resource = 'freight'

	@login_required
	def get(request):
		"""
		显示商品列表
		"""
		user_profile = account_models.UserProfile.objects.filter(user_id=request.user.id)
		free_freight_money = user_profile[0].free_freight_money
		need_freight_money = user_profile[0].need_freight_money
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
			'free_freight_money': free_freight_money if free_freight_money else '-1',
			'need_freight_money': need_freight_money if need_freight_money else '-1'
		})
		return render_to_response('freight_service/freight.html', c)

	@login_required
	def api_put(request):
		user_id = request.user.id
		free_freight_money = request.POST.get('free_freight_money',0)
		need_freight_money = request.POST.get('need_freight_money',0)
		print type(free_freight_money),need_freight_money,"========"
		# try:
		# 	user_profile = account_models.UserProfile.objects.filter(user_id=user_id)
		# 	if user_profile:
		# 		user_profile.update(
		# 			free_freight_money = free_freight_money,
		# 			need_freight_money = need_freight_money
		# 		)
		# 	response = create_response(200)
		# 	data = {}
		# 	data['code'] = 200
		# 	response.data=data
		# except Exception, e:
		# 	response = create_response(500)
		# 	data = {}
		# 	data['code'] = 500
		# 	response.data=data
		# 	response.innerErrMsg = unicode_full_stack()
		user_profile = account_models.UserProfile.objects.filter(user_id=user_id)
		if user_profile:
			user_profile.update(
				free_freight_money = float(free_freight_money),
				need_freight_money = float(need_freight_money)
			)
		response = create_response(200)
		data = {}
		data['code'] = 200
		response.data=data
		return response.get_response()