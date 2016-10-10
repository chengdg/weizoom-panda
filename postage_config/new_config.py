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

class NewConfig(resource.Resource):
	"""
	运费模板列表
	"""
	app = 'postage_config'
	resource = 'new_config'

	@login_required
	def get(request):
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV
		})
		return render_to_response('new_config/new_config.html', c)

	@login_required
	def api_put(request):
		postage_name = request.POST.get('postage_name', '')
		default_postages = json.loads(request.POST.get('default_postages'))
		special_postages = json.loads(request.POST.get('special_postages'))
		free_postages = json.loads(request.POST.get('free_postages'))
		
		postage_config = models.PostageConfig.objects.create(
			owner = request.user,
			name = postage_name,
			first_weight = default_postages[0].get('firstWeight'),
			first_weight_price = default_postages[0].get('firstWeightPrice'),
			added_weight = default_postages[0].get('addedWeight'),
			added_weight_price = default_postages[0].get('addedWeightPrice'),
			is_enable_special_config = True if special_postages else False,
			is_enable_free_config = True if free_postages else False,
			is_enable_added_weight = True if default_postages[0].get('addedWeight')>0 else False,
			is_used = False
		)

		if special_postages:
			#特殊地区运费配置
			special_postage_create = []
			for special_postage in special_postages:
				selected_ids = [str(selected_id) for selected_id in special_postage['selectedIds']]
				special_postage_create.append(models.SpecialPostageConfig(
					owner = request.user,
					postage_config = postage_config,
					first_weight = special_postage['firstWeight'],
					added_weight = special_postage['addedWeight'],
					first_weight_price = special_postage['firstWeightPrice'],
					added_weight_price = special_postage['addedWeightPrice'],
					destination = ','.join(selected_ids)
				))
			models.SpecialPostageConfig.objects.bulk_create(special_postage_create)

		if free_postages:
			#包邮配置
			free_postage_create = []
			for free_postage in free_postages:
				selected_ids = [str(selected_id) for selected_id in free_postage['selectedIds']]
				free_postage_create.append(models.FreePostageConfig(
					owner = request.user,
					postage_config = postage_config,
					condition = free_postage['condition'],
					condition_value = free_postage['conditionValue'],
					destination = ','.join(selected_ids)
				))
			models.FreePostageConfig.objects.bulk_create(free_postage_create)

		response = create_response(200)
		return response.get_response()