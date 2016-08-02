# -*- coding: utf-8 -*-
__author__ = 'lihanyi'

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
from eaglet.utils.resource_client import Resource

from core import paginator
from util import db_util
import requests

import models
import nav
from product_catalog import models as product_catalog_models


FIRST_NAV = 'business'
SECOND_NAV = 'business'

COUNT_PER_PAGE = 10

filter2field = {
}

#创建账号
class BusinessDetail(resource.Resource):
	app = 'business'
	resource = 'business_detail'

	@login_required
	def get(request):
		"""
		响应GET
		"""
		business_id = request.GET.get('id', None)
		jsons = {'items':[]}
		if business_id:
			business = models.Business.objects.get(id=business_id)
			business_data = {
				# 'id': user_profile.id,
				# 'name': user_profile.name,
				# 'username': User.objects.get(id=user_profile.user_id).username,
				# 'account_type': user_profile.role,
				# 'note': user_profile.note
			}
			jsons['items'].append(('business_data', json.dumps(business_data)))

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
			'jsons': jsons
		})
		return render_to_response('business/business_detail.html', c)

	@login_required
	def api_post(request):
		#修改入驻申请
		post = request.POST
		
		response = create_response(200)
		return response.get_response()