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

#对已有的云商通8000客户统一处理经营类目
class Command(BaseCommand):
	def handle(self, **options):
		datas = []
		file_name_dir = '%s' %'./account/management/upload_file/panda_customer_catalog.xlsx'
		data = xlrd.open_workbook(file_name_dir)
		table = data.sheet_by_index(0)
		nrows = table.nrows              #行数
		print "====="+'loading xlsx file'+"====="
		for i in range(1,nrows):
			item = dict()
			item['name'] = table.cell(i,0).value
			item['catalog_name'] = str(int(table.cell(i,1).value))
			datas.append(item)