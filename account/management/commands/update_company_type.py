# -*- coding: utf-8 -*-
import os
import subprocess
import random
import xlrd

from collections import OrderedDict
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from account import models as account_models
from product_catalog import models as product_catalog_models

#对已有的云商通8000客户统一处理经营类目
class Command(BaseCommand):
	def handle(self, **options):
		datas = []
		file_name_dir = '%s' %'./account/management/upload_file/panda_customer_catalog.xlsx'
		data = xlrd.open_workbook(file_name_dir)
		table = data.sheet_by_index(0)
		nrows = table.nrows              #行数
		errors = []
		print "====="+'loading xlsx file'+"====="
		for i in range(1,nrows):
			item = dict()
			item['name'] = table.cell(i,0).value.strip()
			item['catalog_name'] = table.cell(i,1).value.strip()
			datas.append(item)

		catalogs = product_catalog_models.ProductCatalog.objects.filter(level=1)
		catalog_name2id = {catalog.name:int(catalog.id) for catalog in catalogs}
		for data in datas:
			try:
				account_info = account_models.UserProfile.objects.filter(name=data['name'])
				catalog_names = data['catalog_name'].split(';')
				company_type = []
				for catalog_name in catalog_names:
					if catalog_name in catalog_name2id:
						company_type.append(catalog_name2id[catalog_name])
					else:
						errors.append({
							'name': data['name'],
							'catalog_name': data['catalog_name']
							})
						print "==="+'error-------------:name:'+data['name']+"==="
				account_info.update(
					company_type = company_type
				)
				print "====="+'customer_catalog update'+data['name']+"====="
			except Exception,e:
				print e
				print "==="+'error-------------:name:'+data['name']+"==="
		if errors:
			print "====="+'error info'+"====="
			print errors
		else:
			print "====="+'customer_catalogs all success'+"====="