# -*- coding: utf-8 -*-
__author__ = 'zph'


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
from product import models as product_models

import xlrd
import sys

#####################################
#清除商品过期促销标题
#####################################
class Command(BaseCommand):
	def handle(self, **options):
		data = xlrd.open_workbook(u'./account/management/商品池含有过期信息的商品清单20170227.xls')
		table = data.sheet_by_index(0)
		nrows = table.nrows
		names = []
		for row in range(1,nrows):
			name = table.cell(row,1).value
			names.append(name)
		products = product_models.Product.objects.filter(product_name__in=names).update(promotion_title='')