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
from postage_config import new_config
from util import sync_util


class Command(BaseCommand):

	def handle(self, *args, **options):
		"""
		同步没有同步客户运费模板
		"""
		postage_configs = postage_models.PostageConfig.objects.filter(is_deleted=False)
		relations = postage_models.PostageConfigRelation.objects.all()
		free_postage_configs = postage_models.FreePostageConfig.objects.all()
		special_postage_configs = postage_models.SpecialPostageConfig.objects.all()
		relation_postage_ids = [relation.postage_config_id for relation in relations]
		user_relations = account_models.AccountHasSupplier.objects.all()
		count = 0
		for postage_config in postage_configs:
			if postage_config.id not in relation_postage_ids:
				user_relation = user_relations.filter(user_id=postage_config.owner_id).last()
				if user_relation:
					postage_params = new_config.organize_postage_config_params(postage_config=postage_config,
															  user_relation=user_relation)

					resp, resp_data = sync_util.sync_zeus(params=postage_params, resource='mall.postage_config', method='put')

					free_configs = free_postage_configs.filter(postage_config_id=postage_config.id)
					if resp:

						count += 1
						weapp_postage_config_id = resp_data.get('postage_config').get('id')
						postage_models.PostageConfigRelation.objects.create(postage_config_id=postage_config.id,
																	weapp_config_relation_id=weapp_postage_config_id)
						for free_config in free_configs:

							params = new_config.organize_free_postage_config(weapp_postage_config_id=weapp_postage_config_id,
																			 free_postage=free_config)
							resp, resp_data = sync_util.sync_zeus(params=params, resource='mall.free_postage_config',
																  method='put')
						for special_postage in special_postage_configs:
							params = new_config.organize_special_postage_config(weapp_postage_config_id=weapp_postage_config_id,
																				special_postage=special_postage)
							resp, resp_data = sync_util.sync_zeus(params=params, resource='mall.special_postage_config',
																  method='put')
						print 'postage config {} is ok!'.format(postage_config.id)
		print '>>>>>>>>>>>>>>>ALL is OK!<<<<<<<<<<<<<<<<<<<<'
		print '>>>>>>>>>>>>>>>count is {}!<<<<<<<<<<<<<<<<<<<<'.format(count)
