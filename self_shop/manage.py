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

FIRST_NAV = 'self_shop'
SECOND_NAV = 'manage'

SELF_SHOP2TEXT = {
	'weizoom_jia': u'微众家',
	'weizoom_mama': u'微众妈妈',
	'weizoom_xuesheng': u'微众学生',
	'weizoom_baifumei': u'微众白富美',
	'weizoom_shop': u'微众商城',
	'weizoom_club': u'微众俱乐部',
	'weizoom_life': u'微众Life',
	'weizoom_yjr': u'微众一家人',
	'weizoom_fulilaile': u'惠惠来啦'
}

class manage(resource.Resource):
	app = 'self_shop'
	resource = 'manage'

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
		return render_to_response('self_shop/manage.html', c)

	@login_required
	def api_get(request):
		self_shops = models.SelfShops.objects.filter(is_deleted=False)
		rows = []
		for self_shop in self_shops:
			rows.append({
				'self_shop_name': self_shop_has_rebate.self_shop_name,
				'user_name': self_shop_has_rebate.user_name
				})
		data = {
			'rows': rows
		}

		# 构造response
		response = create_response(200)
		response.data = data
		return response.get_response()

	@login_required
	def api_put(request):
		user_name = request.POST.get('self_user_name','')
		rebate_value = request.POST.get('rebate_value','')
		remark = request.POST.get('remark','')
		print user_name,rebate_value,remark,"============"
		self_shop_name = SELF_SHOP2TEXT[user_name] if user_name in SELF_SHOP2TEXT else ''
		try:
			self_shop_has_rebate = models.SelfShopHasRebate.objects.filter(user_name=user_name)
			if self_shop_has_rebate:
				print "----------"
				self_shop_has_rebate.update(
					rebate_value = rebate_value,
					remark = remark
				)
			else:
				print "-----sssssss-----"
				models.SelfShopHasRebate.objects.create(
					self_shop_name = self_shop_name,
					user_name = user_name,
					rebate_value = rebate_value,
					remark = remark
				)
			response = create_response(200)
		except Exception, e:
			response = create_response(500)
			response.innerErrMsg = unicode_full_stack()
		return response.get_response()