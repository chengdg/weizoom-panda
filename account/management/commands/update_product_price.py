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
		file_name_dir = '%s' %'./account/management/upload_file/update_store.xlsx'
		table_title_list = []
		data = xlrd.open_workbook(file_name_dir)
		table = data.sheet_by_index(0)
		nrows = table.nrows              #行数
		ncols = table.ncols                 #列数

		users = User.objects.all()
		user_name2user_id = {user.username:user.id for user in users}
		print "-----start-----"
		for cur_col in range(1,nrows):
			list_create = []
			for i in range(0,ncols):
				print table.cell(cur_col,i).value
				username = table.cell(cur_col,i).value
			try:
				if username in user_name2user_id:
					user_id = user_name2user_id[username]
					products = product_models.Product.objects.filter(owner_id=user_id)
					for product in products:
						clear_price = product.clear_price
						product_models.Product.objects.filter(id=product.id).update(
							product_price = clear_price
						)
			except Exception,e:
				print "-----error-----"
		print "-----success-----"
