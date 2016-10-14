# -*- coding: utf-8 -*-
import os
import random
import xlrd
	
from collections import OrderedDict
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from product import models as product_models
from account import models as account_models
from freight_service import models as freight_models
from postage_config import models as postage_models

class Command(BaseCommand):

	def handle(self, *args, **options):
		"""
		更新客户运费模板
		"""
		account_user_profiles = account_models.UserProfile.objects.filter(is_active=True)
		user_has_freights = freight_models.UserHasFreight.objects.filter(is_deleted=False)
		user_id2free_money = {user_has_freight.user_id:user_has_freight.free_freight_money for user_has_freight in user_has_freights}
		user_id2need_money = {user_has_freight.user_id:user_has_freight.need_freight_money for user_has_freight in user_has_freights}
		
		error_user_ids = []
		for account_user_profile in account_user_profiles:
			user_id = account_user_profile.user_id
			postage_configs = postage_models.PostageConfig.objects.filter(owner_id=user_id)
			try:
				if user_id in user_id2free_money:
					#设置包邮条件的
					free_money = user_id2free_money[user_id]
					need_money = user_id2need_money[user_id] if user_id in user_id2need_money else 0
					if postage_configs:
						postage_models.PostageConfig.objects.filter(owner_id=user_id, is_used=True).update(is_used=False)
						postage_models.PostageConfig.objects.filter(owner_id=user_id, id=postage_configs[0].id).update(
							name = u'系统默认',
							first_weight = 1,
							first_weight_price = need_money,
							added_weight = 1,
							added_weight_price = 0,
							is_enable_special_config = False,
							is_enable_free_config = True,
							is_enable_added_weight = True,
							is_used = True
						)

						postage_models.FreePostageConfig.objects.filter(owner_id=user_id, postage_config_id=postage_configs[0].id).update(
							condition = 'money',
							condition_value = free_money,
							destination = '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34'
						)
					else:
						postage_config = postage_models.PostageConfig.objects.create(
							owner_id = user_id,
							name = u'系统默认',
							first_weight = 1,
							first_weight_price = need_money,
							added_weight = 1,
							added_weight_price = 0,
							is_enable_special_config = False,
							is_enable_free_config = True,
							is_enable_added_weight = True,
							is_used = True
						)
						postage_models.FreePostageConfig.objects.create(
							owner_id = user_id,
							postage_config = postage_config,
							condition = 'money',
							condition_value = free_money,
							destination = '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34'
						)
				else:
					#没有设置包邮条件的
					if postage_configs:
						postage_models.PostageConfig.objects.filter(owner_id=user_id, is_used=True).update(is_used=False)
						postage_models.PostageConfig.objects.filter(owner_id=user_id, id=postage_configs[0].id).update(
							name = u'系统默认',
							first_weight = 1,
							first_weight_price = 0,
							added_weight = 1,
							added_weight_price = 0,
							is_enable_special_config = False,
							is_enable_free_config = True,
							is_enable_added_weight = True,
							is_used = True
						)
					else:
						postage_models.PostageConfig.objects.create(
							owner_id = user_id,
							name = u'系统默认',
							first_weight = 1,
							first_weight_price = 0,
							added_weight = 1,
							added_weight_price = 0,
							is_enable_special_config = False,
							is_enable_free_config = False,
							is_enable_added_weight = True,
							is_used = True
						)
			except Exception, e:
				print e,"-----"
				error_user_ids.append(user_id)
				print user_id,"====error===="

		print error_user_ids,"-----error_user_ids-----"
		print '====sucesss===='
