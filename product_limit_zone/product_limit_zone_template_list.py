# -*- coding: utf-8 -*-
import json

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog

from core import resource
from core.jsonresponse import create_response

from account import models as account_models
from product import models as product_models
from panda.settings import EAGLET_CLIENT_ZEUS_HOST, ZEUS_SERVICE_NAME

import models
import nav

FIRST_NAV = 'limit_zone'
SECOND_NAV = 'limit_zone'
# COUNT_PER_PAGE = 10


class ProductLimitZone(resource.Resource):
	app = 'limit_zone'
	resource = 'template_list'

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
		return render_to_response('product_limit_zone/product_limit_zone.html', c)

	def api_get(request):
		rows = []

		templates = models.ProductLimitZoneTemplate.objects.filter(owner_id=request.user.id,
																   is_deleted=False)
		for template in templates:
			rows.append({"name": template.name,
						 'zone_info': '',
						 'id': template.id})
		data = {
			'rows': rows
		}
		# print '..........................................'
		# print request.user.id
		# print '..........................................'
		response = create_response(200)
		response.data = data
		return response.get_response()