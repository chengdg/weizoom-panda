# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from core import resource
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack
from core import paginator
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog

from util import string_util
from util import db_util
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
from account import models as account_models
from product import models as product_models

import nav
import models

FIRST_NAV = 'postage_config'
SECOND_NAV = 'postage_list'
COUNT_PER_PAGE = 20

class PostageList(resource.Resource):
	"""
	运费模板列表
	"""
	app = 'postage_config'
	resource = 'postage_list'

	@login_required
	def get(request):
		postage_configs = models.PostageConfig.objects.filter(owner_id=request.user.id, is_deleted=False).order_by('-id')
		postages = []
		for postage_config in postage_configs:
			postages.append({
				"postageId": postage_config.id,
				"hasSpecialConfig": postage_config.is_enable_special_config,
				"hasFreeConfig": postage_config.is_enable_free_config,
				"isUsed": postage_config.is_used
			})

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
			'postages': json.dumps(postages)
		})
		return render_to_response('postage_list/postage_list.html', c)

	@login_required
	def api_get(request):
		postage_id = request.GET.get('postage_id', -1)
		postage_configs = models.PostageConfig.objects.filter(id=postage_id, is_deleted=False)
		postage_config_specials = models.SpecialPostageConfig.objects.filter(postage_config_id=postage_id, owner_id=request.user.id)
		free_postage_configs = models.FreePostageConfig.objects.filter(postage_config_id=postage_id, owner_id=request.user.id)
		
		postages = []
		for postage_config in postage_configs:
			postages.append({
				'postageMethod': u'普通快递',
				'postageDestination': u'其他地区',
				'firstWeight': postage_config.first_weight,
				'firstWeightPrice': postage_config.first_weight_price,
				'addedWeight': postage_config.added_weight,
				'addedWeightPrice': postage_config.added_weight_price
			})

		for postage_config_special in postage_config_specials:
			postages.append({
				'postageMethod': u'普通快递',
				'postageDestination': u'全国',
				'firstWeight': postage_config_special.first_weight,
				'firstWeightPrice': postage_config_special.first_weight_price,
				'addedWeight': postage_config_special.added_weight,
				'addedWeightPrice': postage_config_special.added_weight_price
			})

		data = {
			'rows': postages
		}	

		# 构造response
		response = create_response(200)
		response.data = data
		return response.get_response()

	@login_required
	def api_post(request):
		postage_id = request.POST.get('postage_id', -1)
		models.PostageConfig.objects.filter(is_used=True).update(is_used=False)
		models.PostageConfig.objects.filter(id=postage_id).update(is_used=True)
		data = {
			'postageId': postage_id
		}
		response = create_response(200)
		response.data = data
		return response.get_response()

	@login_required
	def api_delete(request):
		postage_id = request.POST.get('postage_id', -1)
		models.PostageConfig.objects.filter(id=postage_id).update(is_deleted=True)
		data = {
			'postageId': postage_id
		}
		response = create_response(200)
		response.data = data
		return response.get_response()