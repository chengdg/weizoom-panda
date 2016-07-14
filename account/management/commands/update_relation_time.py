# -*- coding: utf-8 -*-
__author__ = 'lihanyi'

import json
import os
import random
import time
import datetime
import requests
from collections import OrderedDict
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from fans import models as fans_models
from account import models as account_models
from product import models as product_models
from panda.settings import ZEUS_HOST

#####################################
#更新历史数据，同步商品开始投放日期(商品weapp上架时间)
#####################################
class Command(BaseCommand):
	def handle(self, **options):
		all_sellers = account_models.UserProfile.objects.filter(role=account_models.CUSTOMER)
		user_ids = [seller.user_id for seller in all_sellers]
		all_products = product_models.Product.objects.filter(owner_id__in=user_ids)
		product_ids = ['%s'%product.id for product in all_products]
		product_has_relations = product_models.ProductHasRelationWeapp.objects.filter(product_id__in=product_ids).exclude(weapp_product_id='')
		weapp_product_ids = []
		for product_has_relation in product_has_relations:
			product_id = product_has_relation.weapp_product_id.split(';')
			for p in product_id:
				weapp_product_ids.append(p)
		try:
			weapp_product_ids = '_'.join(weapp_product_ids)
			params = {
				'product_ids': weapp_product_ids
			}
			r = requests.post(ZEUS_HOST+'/mall/product_status/',data=params)
			res = json.loads(r.text)
			if res['code'] == 200:
				weapp_pid2created_at = res['data']
		except Exception,e:
			print(e)
			print ("====="+'error in zeus'+"=====")

		for product_has_relation in product_has_relations:
			product_id = product_has_relation.weapp_product_id.split(';')
			for p in product_id:
				weapp_pid = p
				old_created_at = product_has_relation.created_at.strftime("%Y-%m-%d %H:%M:%S")
				if weapp_pid2created_at.has_key(weapp_pid):
					if weapp_pid2created_at[weapp_pid] < old_created_at:
						actual_created_at = datetime.datetime.strptime(weapp_pid2created_at[weapp_pid],"%Y-%m-%d %H:%M:%S")
						product_models.ProductHasRelationWeapp.objects.filter(weapp_product_id=weapp_pid).update(created_at=actual_created_at)

		print ("====="+'success'+"=====")