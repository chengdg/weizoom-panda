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
		file_name_dir = '%s' %'/panda/account/management/commands/product_module.xlsx'
		print file_name_dir,"-----------"
		table_title_list = []
		data = xlrd.open_workbook(file_name_dir)
		table = data.sheet_by_index(0)
		nrows = table.nrows              #行数
		ncols = table.ncols                 #列数
		data = table.cell(0, 1).value
		for i in range(0,ncols):
			table_content=table.cell(0,i).value
			table_title_list.append(table_content)
		print table_title_list,"=========="
		for cur_col in range(1,nrows):
			for i in range(0,ncols):
				data = table.cell(0, i).value
				if data==u'panda账号':
					account_name=table.cell(cur_col,i).value
				if data==u'微众家':
					weizoom_jia=table.cell(cur_col,i).value
				if data==u'微众妈妈':
					weizoom_mama=table.cell(cur_col,i).value
				if data==u'微众学生':
					weizoom_xuesheng=table.cell(cur_col,i).value
				if data==u'微众商城':
					weizoom_shop=table.cell(cur_col,i).value
					if weizoom_shop:
						print int(weizoom_shop),"=ssss========="
				if data==u'商品名称':
					product_name=table.cell(cur_col,i).value
				if data==u'促销标题':
					promotion_title=table.cell(cur_col,i).value
				if data==u'商品价格':
					product_price=table.cell(cur_col,i).value
				if data==u'结算价':
					clear_price=table.cell(cur_col,i).value
				if data==u'限时结算价':
					limit_clear_price=table.cell(cur_col,i).value

				if data==u'有效期':
					valid_time =table.cell(cur_col,i).value
					has_limit_time = 1
					if valid_time == u'无':
						valid_time_from = None
						valid_time_to = None
						has_limit_time = 0

				if data==u'商品重量':
					product_weight=table.cell(cur_col,i).value
				if data==u'商品库存':
					product_store=table.cell(cur_col,i).value
					if product_store == u'无限':
						product_store = -1
				if data==u'商品轮播图':
					images=table.cell(cur_col,i).value
					if images:
						images = images.split('\n')
				if data==u'详情':
					remark=table.cell(cur_col,i).value
					print remark,"=========="

			try:
				user_profile = account_models.UserProfile.objects.get(name=account_name)
				product = product_models.Product.objects.create(
					owner = user_profile.user, 
					product_name = product_name, 
					promotion_title = promotion_title, 
					product_price = product_price,
					clear_price = clear_price,
					product_weight = product_weight,
					product_store = product_store,
					has_limit_time = has_limit_time,
					limit_clear_price = limit_clear_price,
					valid_time_from = valid_time_from,
					valid_time_to = valid_time_to,
					remark = remark
				)
				if images:
					image_path2id = {}
					for image_path in images:
						image_path = '%s' %image_path
						image = resource_models.Image.objects.create(
							user = user_profile.user,
							path = image_path
						)
						image_path2id[image_path] = image.id
						print image,"---------"
					for image_path in images:
						image_path = '%s' %image_path
						product_models.ProductImage.objects.create(product=product, image_id=image_path2id[image_path])
			except Exception,e:
				print(e)
				print('===========================')
