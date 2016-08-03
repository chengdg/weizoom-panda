# -*- coding: utf-8 -*-
__author__ = 'huangjian'

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
from account import models as account_models
from product import models as product_models

#####################################
#修复bug 造成的部分商品没有结算价
#####################################
class Command(BaseCommand):
	def handle(self, **options):
		all_users = account_models.UserProfile.objects.filter(role=account_models.CUSTOMER)
		user_id2purchase_method = {user.user_id:user.purchase_method for user in all_users}
		user_id2points = {user.user_id:user.points for user in all_users}
		products = product_models.Product.objects.filter(id__gte=1651,id__lte=1761)
		i = 0
		for product in products:
			product_id = product.id
			owner_id = product.owner_id
			clear_price = product.clear_price
			product_price = float(product.product_price)
			if owner_id in user_id2purchase_method:
				purchase_method = user_id2purchase_method[owner_id]
				if purchase_method ==2 and clear_price==0:
					i += 1
					points = 0 if owner_id not in user_id2points else user_id2points[owner_id]
					per_points = points/100
					clear_price = product_price*(1-per_points)
					clear_price = round(clear_price,2)
					product_models.Product.objects.filter(id=product_id).update(clear_price=clear_price)
					print "======successs======",product_id
		print "=====count=====",i