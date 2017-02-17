# -*- coding: utf-8 -*-
import os
import subprocess
import random
import xlrd

from collections import OrderedDict
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from product import models as product_models
from account import models as account_models
from resource import models as resource_models
from self_shop import models as self_shop_models



#对已有的云商通8000客户商品更新库存为 9999
class Command(BaseCommand):
	def handle(self, **options):
		self_shops = self_shop_models.SelfShops.objects.all()
		for self_shop in self_shops:
			try:
				weapp_account = product_models.SelfUsernameWeappAccount.objects.get(self_user_name=self_shop.weapp_user_id)
				weapp_user_id = weapp_account.weapp_account_id
				self_shop.weapp_user_id = weapp_user_id
				self_shop.save()
				print 'success', self_shop.weapp_user_id
			except:
				print 'fail' , self_shop.weapp_user_id
