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
from product import models as product_models
from product_catalog import models as catalog_models

class Command(BaseCommand):
	def handle(self, **options):
		file_name_dir = '%s' %'./account/management/upload_file/import_product_catalog.xlsx'
		table_title_list = []
		data = xlrd.open_workbook(file_name_dir)
		table = data.sheet_by_index(0)
		nrows = table.nrows              #行数
		ncols = table.ncols                 #列数
		for i in range(0,ncols):
			table_content=table.cell(0,i).value
			table_title_list.append(table_content)
		print "-----start-----"
		index = 0
		successs_index = 0
		for cur_col in range(1,nrows):
			for i in range(0,ncols):
				data = table.cell(0, i).value
				if data == u'二级分类':
					catalog_name = table.cell(cur_col,i).value.encode('utf8')
					
				if data == u'商品名称':
					index += 1
					product_name = table.cell(cur_col,i).value.encode('utf8')

			try:
				product_catalog = catalog_models.ProductCatalog.objects.filter(name=catalog_name)
				if product_catalog:
					catalog_id = product_catalog[0].id
					product_models.Product.objects.filter(product_name=product_name).update(
						catalog_id = catalog_id
					)
					successs_index += 1
			except Exception, e:
				print index,"====error===="

		print index,"-----all_count-----"
		print successs_index,'====sucesss_count===='