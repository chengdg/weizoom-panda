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

#对已有的云商通8000客户商品更新商品价格等于结算价
class Command(BaseCommand):
	def handle(self, **options):
		accounts = account_models.UserProfile.objects.filter(role=1)
		for account in accounts:
			product_count = product_models.Product.objects.filter(owner_id=account.user_id, is_deleted=False).count()
			account_models.UserProfile.objects.filter(id=account.id).update(product_count=product_count)