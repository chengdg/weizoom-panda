# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from eaglet.core import watchdog

import nav
from account.models import *
from core import resource
from core.exceptionutil import unicode_full_stack
from core.jsonresponse import create_response
from panda.settings import PRODUCT_POOL_OWNER_ID
from product import models as product_models
from product_catalog import models as catalog_models
from util import sync_util
import models

FIRST_NAV = 'label'
SECOND_NAV = 'label-manager'

#标签管理
class LabelManager(resource.Resource):
	app = 'label'
	resource = 'label_manager'

	@login_required
	def get(request):
		"""
		显示标签列表
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
		})

		return render_to_response('label/label_manager.html', c)

	def api_get(request):
		label_groups = models.LabelGroup.objects.filter(is_deleted=False)
		label_group_values = models.LabelGroupValue.objects.filter(is_deleted=False)
		property_id2name = {}
		for label_property_value in label_group_values:
			if label_property_value.property_id not in property_id2name:
				property_id2name[label_property_value.property_id] = [{
					'label_value_id': label_property_value.id,
					'name': label_property_value.name
				}]
			else:
				property_id2name[label_property_value.property_id].append({
					'label_value_id': label_property_value.id,
					'name': label_property_value.name
				})

		rows = []
		for label_property in label_groups:
			rows.append({
				'id': label_property.id,
				'labelName': label_property.name,
				'labelValues': [] if label_property.id not in property_id2name else json.dumps(property_id2name[label_property.id])
				})
		data = {
			'rows': rows
		}

		# 构造response
		response = create_response(200)
		response.data = data
		return response.get_response()

	def api_put(request):
		try:
			label_group = models.LabelGroup.objects.create(
				user_id= request.user.id
			)
			params = {
				'owner_id': PRODUCT_POOL_OWNER_ID,
			}
			resp, resp_data = sync_util.sync_zeus(params=params, resource='mall.product_label_group', method='put')
			if not resp or not resp_data:
				models.LabelGroup.objects.filter(id=label_group.id).update(is_deleted=True)
				response = create_response(500)
			else:
				models.LabelGroupRelation.objects.create(
					label_group_id=label_group.id,
					weapp_label_group_id=resp_data.get('group').get('id')
				)
				response = create_response(200)
		except:
			response = create_response(500)
			msg = unicode_full_stack()
			watchdog.error(msg)
		return response.get_response()

	def api_post(request):
		label_id = request.POST.get('label_id', -1)
		name = request.POST.get('name', '')
		try:
			models.LabelGroup.objects.filter(id=int(label_id)).update(
				name= name
			)

			response = create_response(200)
			relation = models.LabelGroupRelation.objects.filter(label_group_id=label_id).first()
			if relation:
				weapp_label_group_id = relation.weapp_label_group_id

				params = {
					'owner_id': PRODUCT_POOL_OWNER_ID,
					'name': name,
					'product_label_group_id': weapp_label_group_id
				}
				resp, resp_data = sync_util.sync_zeus(params=params, resource='mall.product_label_group', method='post')
				if not resp:

					response = create_response(500)

		except:
			response = create_response(500)
			msg = unicode_full_stack()
			watchdog.error(msg)
		return response.get_response()

	def api_delete(request):
		label_id = request.POST.get('label_id', 0)
		response = create_response(500)
		try:
			if label_id != 0:
				models.LabelGroup.objects.filter(id=label_id).update(is_deleted=True)
				label_group_values = models.LabelGroupValue.objects.filter(property_id=label_id)
				label_group_values.update(is_deleted=True)
				product_models.ProductHasLabel.objects.filter(property_id=label_id).delete()
				catalog_models.ProductCatalogHasLabel.objects.filter(property_id=label_id).delete()

				response = create_response(200)
				relation = models.LabelGroupRelation.objects.filter(label_group_id=label_id).first()
				if relation:
					weapp_label_group_id = relation.weapp_label_group_id
					params = {
						'owner_id': PRODUCT_POOL_OWNER_ID,
						'product_label_group_id': weapp_label_group_id
					}
					# 先删除weapp的标签分组
					resp, resp_data = sync_util.sync_zeus(params=params, resource='mall.product_label_group',
														  method='delete')
					if not resp:
						watchdog.error('sync_delete_label_group: %s failed' % label_id)
					# 同步删除标签
					for label_group_value in label_group_values:
						value_relation = models.LabelGroupValueRelation.objects.filter(label_value_id=label_group_value.id).first()
						if not value_relation:
							continue
						params = {
							'owner_id': PRODUCT_POOL_OWNER_ID,
							'product_label_id': value_relation.weapp_label_value_id
						}
						resp, resp_data = sync_util.sync_zeus(params=params, resource='mall.product_label',
															  method='delete')
						if not resp:
							watchdog.error('sync_delete_label_: %s failed' % label_group_value.id)
						# 将有这个标签的商品的标签去掉
						params = {
							'owner_id': PRODUCT_POOL_OWNER_ID,
							'label_id': value_relation.weapp_label_value_id
						}
						resp, resp_data = sync_util.sync_zeus(params=params, resource='mall.disable_product_label',
															  method='delete')
						if not resp:
							watchdog.error('sync_disable_product_label: %s failed' % label_group_value.id)
						# 将有这个标签的类目的标签删掉
						params = {
							'owner_id': PRODUCT_POOL_OWNER_ID,
							'label_id': value_relation.weapp_label_value_id
						}
						resp, resp_data = sync_util.sync_zeus(params=params, resource='mall.classification_has_label',
															  method='delete')
		except:
			msg = unicode_full_stack()
			watchdog.error(msg)
			response.innerErrMsg = msg
		return response.get_response()