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
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
from eaglet.utils.resource_client import Resource
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
		user_has_freight = models.UserHasFreight.objects.filter(user_id=request.user.id)
		free_freight_money = '' if not user_has_freight else user_has_freight[0].free_freight_money
		need_freight_money = '' if not user_has_freight else user_has_freight[0].need_freight_money
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
		response = create_response(200)
		data = {}
		try:
			user_profile = account_models.UserProfile.objects.filter(user_id=user_id).first()

			relation = account_models.AccountHasSupplier.objects.filter(account_id=user_profile.id).first()
			user_has_freight = models.UserHasFreight.objects.filter(user_id=user_id)
			free_freight_money = free_freight_money if free_freight_money.strip() else 0
			if user_has_freight:
				user_has_freight.update(
					free_freight_money= float(free_freight_money),
					need_freight_money= float(need_freight_money)
				)
				# 商户同步了说明
				if relation:
					freight_relation = models.UserHasFreightRelation.objects\
						.filter(freight_id=user_has_freight.first().id).first()
					if not freight_relation:
						# 调用增加接偶
						params = {
							"supplier_id": relation.supplier_id,
							"condition_type": 'money',
							"postage": float(need_freight_money),
							"condition_money": float(free_freight_money),
						}
						sync_add(params, user_has_freight.first())
					else:
						params = {
							'id': freight_relation.weapp_freight_id,
							"supplier_id": relation.supplier_id,
							"condition_type": 'money',
							"postage": float(need_freight_money),
							"condition_money": float(free_freight_money),
						}
						sync_update(params)

			else:
				db_model = models.UserHasFreight.objects.create(
					user_id= request.user.id,
					free_freight_money= float(free_freight_money),
					need_freight_money= float(need_freight_money)
				)

				if relation:

					params = {
						'id': freight_relation.weapp_freight_id,
						"supplier_id": relation.supplier_id,
						"condition_type": 'money',
						"postage": float(need_freight_money),
						"condition_money": float(free_freight_money),
					}
					result = sync_update(params, db_model)
					if not result:
						data['code'] = 500
						return response.get_response()

			data['code'] = 200
			response.data = data
		except:
			print unicode_full_stack()
			data['code'] = 500
			response.data=data
			response.innerErrMsg = unicode_full_stack()
		return response.get_response()


def sync_add(params, user_has_freight):
	"""
	新增同步
	"""
	resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put({
		'resource': 'mall.supplier_postage_config',
		"data": params
	})

	if resp and resp.get('code') == 200 and resp.get('data').get('postage_config'):
		models.UserHasFreightRelation.objects.create(freight_id=user_has_freight.id,
													 weapp_freight_id=resp.get('data')
													 .get('postage_config').get('id'))
		return True
	else:
		user_has_freight.delete()
		return False

def sync_update(params):
	"""
	更新同步
	"""
	resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post({
		'resource': 'mall.supplier_postage_config',
		"data": params
	})

	if resp and resp.get('code') == 200 and resp.get('data').get('change_rows') != -1:
		return True
	else:
		return False
