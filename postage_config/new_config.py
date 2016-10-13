# -*- coding: utf-8 -*-
import json

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response

from product import models as product_models
from account import models as account_models
from util import sync_util
import nav
import models
from panda.settings import PRODUCT_POOL_OWNER_ID

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
		postage_id = request.GET.get('postage_id', None)
		#获取省份
		provinces = product_models.Province.objects.all()
		province_id2name = {province.id:province.name for province in provinces}

		jsons = {'items':[]}
		if postage_id:
			postages = {
				'postage_id': postage_id,
				'postage_name': '',
				'default_postages':[],
				'special_postages':[],
				'free_postages':[]
			}

			#默认运费配置
			postage_configs = models.PostageConfig.objects.filter(id=postage_id, is_deleted=False)
			for postage_config in postage_configs:
				postages['postage_name'] = postage_config.name
				postages['default_postages'].append({
					'firstWeight': '%s' %postage_config.first_weight,
					'firstWeightPrice': '%s' %postage_config.first_weight_price,
					'addedWeight': '%s' %postage_config.added_weight,
					'addedWeightPrice': '%s' %postage_config.added_weight_price,
				})

			#特殊地区运费配置
			postage_config_specials = models.SpecialPostageConfig.objects.filter(postage_config_id=postage_id)
			for postage_config_special in postage_config_specials:
				destinations = postage_config_special.destination.split(',')
				postages['special_postages'].append({
					'firstWeight': '%s' %postage_config_special.first_weight,
					'firstWeightPrice': '%s' %postage_config_special.first_weight_price,
					'addedWeight': '%s' %postage_config_special.added_weight,
					'addedWeightPrice': '%s' %postage_config_special.added_weight_price,
					'selectedIds': destinations
				})

			#包邮配置
			free_postage_configs = models.FreePostageConfig.objects.filter(postage_config_id=postage_id)
			for free_postage_config in free_postage_configs:
				destinations = free_postage_config.destination.split(',')
				postages['free_postages'].append({
					'condition': free_postage_config.condition,
					'conditionValue': '%s' %free_postage_config.condition_value,
					'selectedIds': destinations
				})
			jsons['items'].append(('postages', json.dumps(postages)))
		else:
			jsons['items'].append(('postages', json.dumps(None)))


		provinceId2name = {
			'province_id2name': province_id2name
		}
		jsons['items'].append(('provinceId2name', json.dumps(provinceId2name)))
		c = RequestContext(request, {
			'jsons': jsons,
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
		# 同步
		if postage_config:
			user_relation = account_models.AccountHasSupplier.objects.filter(user_id=request.user.id).last()
			if user_relation:
				params = organize_postage_config_params(postage_config=postage_config,
														user_relation=user_relation)

				resp, resp_data = sync_util.sync_zeus(params=params, resource='mall.postage_config', method='put')
				if not resp:
					models.PostageConfig.objects.filter(id=postage_config.id).delete()
				else:
					# 存储模板的中间关系
					weapp_postage_config = resp_data.get('postage_config')

					models.PostageConfigRelation.objects.create(postage_config_id=postage_config.id,
																weapp_config_relation_id=weapp_postage_config.get('id'))
					# 同步特殊运费和普通运费
					if special_postages:
						for special_postage in special_postage_create:
							params = organize_special_postage_config(weapp_postage_config_id=weapp_postage_config.get('id'),
																	 special_postage=special_postage)

							sync_util.sync_zeus(params=params, resource='mall.special_postage_config', method='put')
					if free_postages:
						for free_postage in free_postage_create:
							params = organize_free_postage_config(weapp_postage_config_id=weapp_postage_config.get('id'),
																  free_postage=free_postage)

							sync_util.sync_zeus(params=params, resource='mall.free_postage_config', method='put')

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		postage_id = int(request.POST.get('postage_id', -1))
		postage_name = request.POST.get('postage_name', '')
		default_postages = json.loads(request.POST.get('default_postages'))
		special_postages = json.loads(request.POST.get('special_postages'))
		free_postages = json.loads(request.POST.get('free_postages'))
		
		models.PostageConfig.objects.filter(id=postage_id, is_deleted=False).update(
			name = postage_name,
			first_weight = default_postages[0].get('firstWeight'),
			first_weight_price = default_postages[0].get('firstWeightPrice'),
			added_weight = default_postages[0].get('addedWeight'),
			added_weight_price = default_postages[0].get('addedWeightPrice'),
			is_enable_special_config = True if special_postages else False,
			is_enable_free_config = True if free_postages else False,
			is_enable_added_weight = True if default_postages[0].get('addedWeight')>0 else False,
		)

		#特殊地区运费配置
		models.SpecialPostageConfig.objects.filter(postage_config_id=postage_id).delete()
		if special_postages:
			special_postage_create = []
			for special_postage in special_postages:
				selected_ids = [str(selected_id) for selected_id in special_postage['selectedIds']]
				special_postage_create.append(models.SpecialPostageConfig(
					owner = request.user,
					postage_config_id = postage_id,
					first_weight = special_postage['firstWeight'],
					added_weight = special_postage['addedWeight'],
					first_weight_price = special_postage['firstWeightPrice'],
					added_weight_price = special_postage['addedWeightPrice'],
					destination = ','.join(selected_ids)
				))
			models.SpecialPostageConfig.objects.bulk_create(special_postage_create)

		#包邮配置
		models.FreePostageConfig.objects.filter(postage_config_id=postage_id).delete()
		if free_postages:
			free_postage_create = []
			for free_postage in free_postages:
				selected_ids = [str(selected_id) for selected_id in free_postage['selectedIds']]
				free_postage_create.append(models.FreePostageConfig(
					owner = request.user,
					postage_config_id = postage_id,
					condition = free_postage['condition'],
					condition_value = free_postage['conditionValue'],
					destination = ','.join(selected_ids)
				))
			models.FreePostageConfig.objects.bulk_create(free_postage_create)
		# 同步
		postage_config = models.PostageConfig.objects.filter(id=postage_id).first()
		user_relation = account_models.AccountHasSupplier.objects.filter(user_id=request.user.id).last()
		if postage_config and user_relation:

			params = organize_postage_config_params(postage_config=postage_config, user_relation=user_relation)
			postage_config_relation = models.PostageConfigRelation.objects\
				.filter(postage_config_id=postage_config.id,).last()
			params.update(postage_config_id=postage_config_relation.weapp_config_relation_id)
			resp, resp_data = sync_util.sync_zeus(params=params, resource='mall.postage_config', method='post')
			weapp_config_relation_id = postage_config_relation.weapp_config_relation_id
			if resp:
				special_params = {
					'owner_id': PRODUCT_POOL_OWNER_ID,
					'postage_config_id': weapp_config_relation_id
				}
				sync_util.sync_zeus(params=special_params, resource='mall.special_postage_config', method='delete')
				if special_postages:
					for special_postage in special_postage_create:
						params = organize_special_postage_config(weapp_postage_config_id=weapp_config_relation_id,
																 special_postage=special_postage)

						sync_util.sync_zeus(params=params, resource='mall.special_postage_config', method='put')
				if free_postages:
					free_params = {
						'owner_id': PRODUCT_POOL_OWNER_ID,
						'postage_config_id': weapp_config_relation_id
					}
					sync_util.sync_zeus(params=free_params, resource='mall.free_postage_config', method='delete')
					for free_postage in free_postage_create:
						params = organize_free_postage_config(weapp_postage_config_id=weapp_config_relation_id,
															  free_postage=free_postage)

						sync_util.sync_zeus(params=params, resource='mall.free_postage_config', method='put')
		response = create_response(200)
		return response.get_response()


def organize_postage_config_params(postage_config=None, user_relation=None):
	"""
	组织运费模板参数
	"""
	params = {
		'name': postage_config.name,
		'owner_id': PRODUCT_POOL_OWNER_ID,
		'supplier_id': user_relation.supplier_id,
		'first_weight': postage_config.first_weight,
		'first_weight_price': postage_config.first_weight_price,
		'is_enable_added_weight': 'true' if postage_config.is_enable_added_weight else 'false',
		'added_weight': postage_config.added_weight,
		'added_weight_price': postage_config.added_weight_price,
		'is_used': 'true' if postage_config.is_used else 'false',
		'is_enable_special_config': 'true' if postage_config.is_enable_special_config else 'false',
		'is_enable_free_config': 'true' if postage_config.is_enable_free_config else 'false',
	}
	return params


def organize_special_postage_config(weapp_postage_config_id=None, special_postage=None):
	"""
	组织运费模板中的特殊设置参数
	"""
	params = {
		'owner_id': PRODUCT_POOL_OWNER_ID,
		'postage_config_id': weapp_postage_config_id,
		'destination': special_postage.destination,
		'first_weight_price': special_postage.first_weight_price,
		'first_weight': special_postage.first_weight,
		'added_weight': special_postage.added_weight,
		'added_weight_price': special_postage.added_weight_price,
	}
	return params


def organize_free_postage_config(weapp_postage_config_id=None, free_postage=None):
	"""

	"""
	if free_postage.condition == 'count':
		condition_value = int(free_postage.condition_value)
	else:
		condition_value = float(free_postage.condition_value)
	params = {
		'owner_id': PRODUCT_POOL_OWNER_ID,
		'postage_config_id': weapp_postage_config_id,
		'destination': free_postage.destination,
		'condition': free_postage.condition,
		'condition_value': condition_value,
	}
	return params
