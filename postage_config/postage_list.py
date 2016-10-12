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
from new_config import organize_postage_config_params

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
				"postageName": postage_config.name,
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
		
		#获取省份
		provinces = product_models.Province.objects.all()
		province_id2name = {province.id:province.name for province in provinces}

		postages = []
		destination = u'全国'
		if len(postage_config_specials)>0 or len(free_postage_configs)>0:
			destination = u'其他地区'

		for postage_config in postage_configs:
			postages.append({
				'postageMethod': u'普通快递',
				'postageDestination':  destination,
				'firstWeight': postage_config.first_weight,
				'firstWeightPrice': postage_config.first_weight_price,
				'addedWeight': postage_config.added_weight,
				'addedWeightPrice': postage_config.added_weight_price
			})

		for postage_config_special in postage_config_specials:
			destinations = postage_config_special.destination.split(',')
			destination_text = []
			for destination_id in destinations:
				if int(destination_id) in province_id2name:
					destination_text.append(province_id2name[int(destination_id)])
			
			postages.append({
				'postageMethod': u'普通快递',
				'postageDestination': u'；'.join(destination_text),
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
		# 必须在这里查,查之前用的模板
		old_used_config = models.PostageConfig.objects.filter(owner_id=request.user.id,
															  is_used=True).last()
		models.PostageConfig.objects.filter(is_used=True,
											owner_id=request.user.id).update(is_used=False)

		models.PostageConfig.objects.filter(id=postage_id).update(is_used=True)
		new_use_config = models.PostageConfig.objects.filter(id=postage_id).last()
		user_relation = account_models.AccountHasSupplier.objects.filter(user_id=request.user.id).last()
		# 同步
		if old_used_config and user_relation:
			params = organize_postage_config_params(postage_config=old_used_config, user_relation=user_relation)
			postage_config_relation = models.PostageConfigRelation.objects \
				.filter(postage_config_id=old_used_config.id, ).last()
			params.update({'postage_config_id': postage_config_relation.weapp_config_relation_id,
						   'is_used': 'false'})

			if postage_config_relation:
				sync_util.sync_zeus(params=params, resource='mall.postage_config', method='post')
		if new_use_config and user_relation:

			params = organize_postage_config_params(postage_config=new_use_config, user_relation=user_relation)
			postage_config_relation = models.PostageConfigRelation.objects \
				.filter(postage_config_id=new_use_config.id, ).last()
			params.update({'postage_config_id': postage_config_relation.weapp_config_relation_id})

			if postage_config_relation:
				sync_util.sync_zeus(params=params, resource='mall.postage_config', method='post')
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
		# 同步

		user_relation = account_models.AccountHasSupplier.objects.filter(user_id=request.user.id).last()
		relation = models.PostageConfigRelation.objects.filter(postage_config_id=postage_id).last()

		if relation and user_relation:
			params = {
				'owner_id': PRODUCT_POOL_OWNER_ID,
				'postage_config_id': relation.weapp_config_relation_id,
				'supplier_id': user_relation.supplier_id
			}
			sync_util.sync_zeus(params=params, resource='mall.postage_config', method='delete')
		response = create_response(200)
		response.data = data
		return response.get_response()