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
COUNT_PER_PAGE = 20

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
		cur_page = request.GET.get('page', 1)
		pageinfo, self_shops = paginator.paginate(self_shops, cur_page, COUNT_PER_PAGE, query_string=request.META['QUERY_STRING'])
		
		rows = []
		for self_shop in self_shops:
			rows.append({
				'selfShopName': self_shop.self_shop_name,
				'userName': self_shop.user_name,
				'isSynced': self_shop.is_synced
				})
		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}

		response = create_response(200)
		response.data = data
		return response.get_response()

	@login_required
	def api_put(request):
		user_name = request.POST.get('self_user_name','')
		is_sync = request.POST.get('is_sync','')
		remark = request.POST.get('remark','')
		try:
			print user_name,is_sync,remark,"============"
			response = create_response(200)
		except Exception, e:
			response = create_response(500)
			response.innerErrMsg = unicode_full_stack()
		return response.get_response()

#得到所有还未同步的自营平台
class GetAllUnsyncedSelfShops(resource.Resource):
	app = 'self_shop'
	resource = 'get_all_unsynced_self_shops'

	@login_required
	def api_get(request):
		rows = [{
			'text': u'自营平台1111',
			'value': 'aaaa'
		}]
		data = {
			'rows': rows
		}
		response = create_response(200)
		response.data = data
		return response.get_response()

#得到所有已经同步过的自营平台
class GetAllSyncedSelfShops(resource.Resource):
	app = 'self_shop'
	resource = 'get_all_synced_self_shops'

	@login_required
	def api_get(request):
		self_shops = models.SelfShops.objects.filter(is_deleted=False, is_synced=True)
		rows = [{
			'text': u'全部',
			'value': -1
		}]
		for self_shop in self_shops:
			rows.append({
				'text': self_shop.self_shop_name,
				'value': self_shop.user_name
			})
		data = {
			'rows': rows
		}
		response = create_response(200)
		response.data = data
		return response.get_response()