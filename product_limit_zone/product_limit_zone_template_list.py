# -*- coding: utf-8 -*-
import json
from collections import defaultdict

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog

from core import resource
from core.jsonresponse import create_response

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
		template_ids = [template.id for template in templates]

		all_zone_info = models.LimitTemplateHasZone.objects.filter(template_id__in=template_ids)
		provinces = product_models.Province.objects.all()
		provinces = {province.id: province.name for province in provinces}
		cities = product_models.City.objects.all()
		cities = {city.id: city.name for city in cities}
		for template in templates:
			zone_info = filter(lambda key: key.template_id == template.id, all_zone_info)
			zone_list = [str(zone.province) if not zone.city else '_'.join([str(zone.province), str(zone.city)])
						 for zone in zone_info]
			limit_zone_info = defaultdict(list)

			for z in zone_info:
				limit_zone_info[z.province].append(z.city)
			limit_zone_info_text = []
			# print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.'
			# print type(limit_zone_info)
			# print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.'
			for k, v in limit_zone_info.items():

				limit_zone_info_text.append({
					'province': provinces.get(k),
					'cities': '全选' if len(v) == 1 and v[0] == 0 else ','.join([cities.get(city) for city in v if city])
				})

			rows.append({"name": template.name,
						 'limit_zone_info_text': limit_zone_info_text,
						 'zone_list': zone_list,
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