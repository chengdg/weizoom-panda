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
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog

from util import string_util
from account import models as account_models
from product import models as product_models
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
from util import db_util
from panda.settings import CESHI_USERNAMES
from get_all_unsynced_self_shops import get_self_shops_dict

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
		self_shops = models.SelfShops.objects.filter(is_deleted=False).order_by('-created_at')
		cur_page = request.GET.get('page', 1)
		pageinfo, self_shops = paginator.paginate(self_shops, cur_page, COUNT_PER_PAGE, query_string=request.META['QUERY_STRING'])
		
		that_rows,store_name2id=get_self_shops_dict()

		rows = []
		for self_shop in self_shops:
			self_shop_id = store_name2id.get(self_shop.self_shop_name)
			rows.append({
				'selfShopId': self_shop_id,
				'selfShopName': self_shop.self_shop_name,
				'userName': self_shop.weapp_user_id,
				'settlementType': self_shop.settlement_type,
				'splitRatio': self_shop.split_atio,
				'riskMoney': self_shop.risk_money,
				'remark': self_shop.remark,
				'isSynced': self_shop.is_synced,
				'corpAccount':	self_shop.corp_account
				})
		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}

		response = create_response(200)
		response.data = data
		return response.get_response()

	@login_required
	#新建自营平台
	def api_put(request):
		self_shop_name = request.POST.get('self_shop_name','')
		weapp_user_id = request.POST.get('weapp_user_id','')
		settlement_type = int(request.POST.get('settlement_type',1))
		corp_account = int(request.POST.get('corp_account',1))
		split_atio = float(request.POST.get('split_atio',0))
		risk_money = float(request.POST.get('risk_money',0))
		is_sync = request.POST.get('is_sync','')
		remark = request.POST.get('remark','')
		if models.SelfShops.objects.filter(weapp_user_id=weapp_user_id).count() > 0:
			response = create_response(500)
			response.errMsg = u'该自营平台已存在'
			return response.get_response()
		try:
			models.SelfShops.objects.create(
				self_shop_name = self_shop_name,
				weapp_user_id = weapp_user_id,
				settlement_type = settlement_type,
				split_atio = split_atio,
				risk_money = risk_money,
				corp_account = corp_account,
				remark = remark
			)
			product_models.SelfUsernameWeappAccount.objects.create(
				self_user_name = weapp_user_id,
				weapp_account_id = weapp_user_id
			)
			is_sync = True if is_sync == 'is_sync' else False
			if is_sync: #需要在创建时候同步
				is_synced = sync_all_product_2_new_self_shop(weapp_user_id)
				sync_all_product_2_weapp(weapp_user_id)
				if is_synced:
					models.SelfShops.objects.filter(weapp_user_id=weapp_user_id).update(
						is_synced = True
						)
					response = create_response(200)
				else:
					response = create_response(500)
					response.errMsg = u'同步失败'
					response.innerErrMsg = unicode_full_stack()
			else:
				response = create_response(200)
		except Exception, e:
			msg = unicode_full_stack()
			response = create_response(500)
			response.errMsg = u'添加自营平台失败'
			print msg
		return response.get_response()

	@login_required
	#同步自营平台下的商品
	def api_post(request):
		user_name = request.POST.get('self_user_name','')

		if user_name:
			try:
				is_synced = sync_all_product_2_new_self_shop(user_name)
				sync_all_product_2_weapp(user_name)
				if is_synced:
					models.SelfShops.objects.filter(weapp_user_id=user_name).update(
						is_synced = True
						)
					response = create_response(200)
				else:
					response = create_response(500)
					response.innerErrMsg = unicode_full_stack()
			except Exception, e:
				print e
				response = create_response(500)
				response.innerErrMsg = unicode_full_stack()
			return response.get_response()

		else:
			self_shop_name = request.POST.get('self_shop_name','')
			weapp_user_id = request.POST.get('weapp_user_id','')
			settlement_type = int(request.POST.get('settlement_type',1))
			corp_account = int(request.POST.get('corp_account',1))
			split_atio = float(request.POST.get('split_atio',0))
			risk_money = float(request.POST.get('risk_money',0))
			is_sync = request.POST.get('is_sync','')
			remark = request.POST.get('remark','')
			try:
				models.SelfShops.objects.filter(weapp_user_id=weapp_user_id).update(
					settlement_type = settlement_type,
					split_atio = split_atio,
					risk_money = risk_money,
					remark = remark,
					corp_account = corp_account,
				)
				is_sync = True if is_sync == 'is_sync' else False
				if is_sync: #需要在创建时候同步
					is_synced = sync_all_product_2_new_self_shop(weapp_user_id)
					sync_all_product_2_weapp(weapp_user_id)
					if is_synced:
						models.SelfShops.objects.filter(weapp_user_id=weapp_user_id).update(
							is_synced = True
							)
						response = create_response(200)
					else:
						response = create_response(500)
						response.errMsg = u'同步失败'
						response.innerErrMsg = unicode_full_stack()
				else:
					response = create_response(200)
			except Exception, e:
				msg = unicode_full_stack()
				response = create_response(500)
				response.errMsg = u'添加自营平台失败'
				print msg
			return response.get_response()


def get_all_synced_self_shops(request,is_for_search):
	"""
	得到所有已经同步过的自营平台
	"""
	all_self_shop_value = []
	if is_for_search:
		rows = [{
			'text': u'全部',
			'value': '-1'
		}]
	else:
		rows = []
	self_shops = models.SelfShops.objects.filter(is_deleted=False).exclude(self_shop_name__in=['开发测试','财务测试'])
	for self_shop in self_shops:
		rows.append({
			'text': self_shop.self_shop_name,
			'value': self_shop.weapp_user_id
		})
		all_self_shop_value.append(self_shop.weapp_user_id)

	username = account_models.User.objects.get(id=request.user.id).username
	if username in CESHI_USERNAMES:
		rows.append({
			'text': u'开发测试',
			'value': 'devceshi'
		})
		rows.append({
			'text': u'财务测试',
			'value': 'caiwuceshi'
		})
		all_self_shop_value.append('devceshi')
		all_self_shop_value.append('caiwuceshi')
	data = {
		'rows': rows,
		'allSelfShopsValue' : all_self_shop_value
	}
	return data

def sync_all_product_2_new_self_shop(self_user_name):
	"""
	同步商品到新的自营平台
	"""
	try:
		relations = product_models.ProductSyncWeappAccount.objects.all().values('product_id').distinct()
		bulk_create = []
		for relation in relations:
			product_id = relation.get('product_id')
			t_1 = product_models.ProductSyncWeappAccount(product_id=product_id, self_user_name=self_user_name)
			bulk_create.append(t_1)
		product_models.ProductSyncWeappAccount.objects.bulk_create(bulk_create)
		return True
	except:
		return False

def sync_all_product_2_weapp(self_user_name):

	relation = product_models.SelfUsernameWeappAccount.objects.\
		filter(self_user_name=self_user_name).order_by('-id').first()
	weapp_account_id = relation.weapp_account_id
	params = {
		'new_proprietary_id': weapp_account_id
	}
	resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put(
		{
			'resource': 'panda.sync_product_new_proprietary',
			'data': params
		}
	)
	if not resp or not resp.get('code') == 200:

		watchdog.error('sync_all_product_2_weapp:{} failed!'.format(self_user_name))