# -*- coding: utf-8 -*-
__author__ = 'huangjian'

import json
import math
import os
import random
import time
import datetime
import requests
from collections import OrderedDict
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from account import models as account_models
from product import models as product_models

#####################################
#修复老数据固定扣点供货商商品没有结算价
#####################################
class Command(BaseCommand):
	def handle(self, **options):
		all_users_55rebatep = account_models.UserProfile.objects.filter(role=account_models.CUSTOMER,purchase_method =3)
		user_ids_55rebateps = [user.user_id for user in all_users_55rebatep]		
		account_has_rebatep_roports = account_models.AccountHasRebateProport.objects.filter(user_id__in=user_ids_55rebateps)
		for account_has_rebatep_roport in account_has_rebatep_roports:
			account_models.UserProfile.objects.filter(user_id = account_has_rebatep_roport.user_id).update(purchase_method =2,points=account_has_rebatep_roport.default_rebate_proport)

		all_users = account_models.UserProfile.objects.filter(role=account_models.CUSTOMER,purchase_method =2)
		user_ids = [user.user_id for user in all_users]
		user_id2points = {user.user_id:user.points for user in all_users}

		products = product_models.Product.objects.filter(owner_id__in=user_ids,has_product_model=0)		
		for product in products:
			try:
				clear_price = round(float(product.product_price)*float(100-(user_id2points[product.owner_id])))/100
				product_id = product.id
				product_info =product_models.Product.objects.get(id =product_id)
				product_info.clear_price = clear_price
				product_info.save()
			except Exception,e:
				print "==="+'error:user is not exsit:'+str(product.id)+"==="

		productmodels = product_models.ProductModel.objects.filter(owner_id__in=user_ids)		
		for productmodel in productmodels:
			try:
				market_price = round(float(productmodel.price)*float(100-(user_id2points[product.owner_id])))/100
				productmodel_id = productmodel.id
				productmodel_info =product_models.ProductModel.objects.get(id =productmodel_id)
				productmodel_info.market_price = market_price
				productmodel_info.save()
			except Exception,e:
				print "==="+'error:user is not exsit:'+str(productmodel.id)+"==="