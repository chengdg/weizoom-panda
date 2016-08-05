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


class Command(BaseCommand):
	def handle(self, **options):
		product_ids = [2, 6, 7, 8, 16, 17, 18, 20, 21, 186, 187, 188, 189,
					   190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202,
					   204, 205, 208, 209, 210, 211, 212, 213, 214]
		products = product_models.Product.objects.filter(id__in=product_ids)
		for product in products:
			remark = product.remark
			if remark.find('http'):
				continue
			if remark.find('chaozhi'):
				continue
			new_remark = remark.replace('/static', 'http://chaozhi.weizoom.com/static')
			product_models.Product.objects.filter(id=product.id).update(remark=new_remark)
			# product.update(remark=new_remark)
			print '================================product:%s SUCCESS!' % product.id
		print '==============================ALL is OK==============================='