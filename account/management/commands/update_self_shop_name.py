# -*- coding: utf-8 -*-

import os
import subprocess
import random

from collections import OrderedDict
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from product import models as product_models

class Command(BaseCommand):
	def handle(self, **options):
		product_models.ProductRelation.objects.all().delete()
		self_shops = OrderedDict()
		self_shops = {
			'weizoom_jia': u'微众家',
			'weizoom_mama': u'微众妈妈',
			'weizoom_xuesheng': u'微众学生',
			'weizoom_baifumei': u'微众白富美',
			'weizoom_shop': u'微众商城'
		}
		list_create = []
		for (k,v) in self_shops.items():
			list_create.append(product_models.ProductRelation(
				self_user_name = k,
				self_first_name = v
			))
		product_models.ProductRelation.objects.bulk_create(list_create)
		print "==="+u'自营商城'+"==="