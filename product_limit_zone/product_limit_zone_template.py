# -*- coding: utf-8 -*-
import json

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.core import watchdog

from core import resource
from core.jsonresponse import create_response

from account import models as account_models
from product import models as product_models

import models
import nav
from util import sync_util
from panda.settings import PRODUCT_POOL_OWNER_ID

FIRST_NAV = 'limit_zone'
SECOND_NAV = 'limit_zone'
# COUNT_PER_PAGE = 10


class ProductLimitZone(resource.Resource):
	app = 'product_limit_zone'
	resource = 'template'

	@login_required
	def get(request):
		"""

		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV
		})
		return render_to_response('product_limit_zone/product_limit_zone.html', c)

	def api_get(request):
		rows = []
		data = {
			'rows': rows
		}
		response = create_response(200)
		response.data = data
		return response.get_response()

	def api_put(request):
		post = request.POST
		name = post.get('name')
		db_model = None
		try:
			db_model = models.ProductLimitZoneTemplate.objects.create(name=name,
																	  owner_id=request.user.id)
			params = {
				'name': name,
				'owner_id': PRODUCT_POOL_OWNER_ID
			}
			resp, resp_data = sync_util.sync_zeus(params=params, resource='mall.product_limit_zone_template',
												  method='put')

			if resp and resp_data:
				# 创建中间关系
				models.ProductLimitZoneTemplateRelation.objects.create(
					template_id=db_model.id,
					weapp_template_id=resp_data.get('template').get('id')
				)
				response = create_response(200)
			else:
				models.ProductLimitZoneTemplate.objects.filter(id=db_model).delete()
				response = create_response(500)

		except:
			msg = unicode_full_stack()
			watchdog.error('product_limit_zone.template_PUT{}'.format(msg))
			if db_model:
				models.ProductLimitZoneTemplate.objects.filter(id=db_model).delete()
			response = create_response(500)
		return response.get_response()

	def api_post(request):
		post = request.POST
		name = post.get('name')
		template_id = post.get('id')

		flag = post.get('flag', 'name')
		try:
			models.ProductLimitZoneTemplate.objects.filter(id=template_id).update(name=name)
			# 同步到weapp的参数
			weapp_cities = []
			weapp_provinces = []
			if flag != 'name':
				selected_data = json.loads(post.get('selected_data', ''))

				provinces = selected_data.get('provinces')
				# 先删除
				models.LimitTemplateHasZone.objects.filter(template_id=template_id).delete()
				# 创建模板的数据
				bulk_create = []

				for province in provinces:
					# 前段传递的数据如果是全选了省，那么cities是空的
					cities = province.get('cities')
					weapp_provinces.append(province.get('provinceId'))
					if not cities:
						bulk_create.append(models.LimitTemplateHasZone(template_id=template_id,
																	   province=province.get('provinceId'),
																	   ))
					else:
						bulk_create += [models.LimitTemplateHasZone(template_id=template_id,
																	province=province.get('provinceId'),
																	city=city.get('cityId')) for city in cities]
						weapp_cities += [city.get('cityId') for city in cities]
				models.LimitTemplateHasZone.objects.bulk_create(bulk_create)
				# 同步更新到weapp
			relation = models.ProductLimitZoneTemplateRelation.objects.filter(template_id=template_id).first()

			if relation:
				params = {
					'owner_id': PRODUCT_POOL_OWNER_ID,
					'name': name,
					'cities': ','.join(weapp_cities),
					'template_id': relation.weapp_template_id,
					'provinces': ','.join(weapp_provinces)
				}
				sync_util.sync_zeus(params=params, resource='mall.product_limit_zone_template',
										method='post')
			response = create_response(200)
		except:
			msg = unicode_full_stack()
			watchdog.error('product_limit_zone.template_POST{}'.format(msg))
			response = create_response(500)
		return response.get_response()

	def api_delete(request):
		post = request.POST
		template_id = post.get('id')

		try:
			models.ProductLimitZoneTemplate.objects.filter(id=template_id).update(is_deleted=True)
			response = create_response(200)
		except:
			msg = unicode_full_stack()
			watchdog.error('product_limit_zone.template_DELETE{}'.format(msg))
			response = create_response(500)
		return response.get_response()