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
		table_title_list = []
		data = xlrd.open_workbook(file_name_dir)
		table = data.sheet_by_index(0)
		nrows = table.nrows              #行数
		ncols = table.ncols                 #列数
		data = table.cell(0, 1).value
		for i in range(0,ncols):
			table_content=table.cell(0,i).value
			table_title_list.append(table_content)
		for cur_col in range(1,nrows):
			relations = {}
			for i in range(0,ncols):
				data = table.cell(0, i).value
				if data == u'panda账号':
					account_name=table.cell(cur_col,i).value
				if data == u'微众家':
					weizoom_jia = table.cell(cur_col,i).value
					if weizoom_jia:
						if ';' not in '%s'%weizoom_jia:
							weizoom_jia = int(weizoom_jia)
						relations['weizoom_jia'] = '%s'%weizoom_jia
				if data == u'微众妈妈':
					weizoom_mama = table.cell(cur_col,i).value
					if weizoom_mama:
						if ';' not in '%s'%weizoom_mama:
							weizoom_mama = int(weizoom_mama)
						relations['weizoom_mama'] = '%s'%weizoom_mama
				if data == u'微众学生':
					weizoom_xuesheng = table.cell(cur_col,i).value
					if weizoom_xuesheng:
						if ';' not in '%s'%weizoom_xuesheng:
							weizoom_xuesheng = int(weizoom_xuesheng)
						relations['weizoom_xuesheng'] = '%s'%weizoom_xuesheng
				if data == u'微众商城':
					weizoom_shop = table.cell(cur_col,i).value
					if weizoom_shop:
						if ';' not in '%s'%weizoom_shop:
							weizoom_shop = int(weizoom_shop)
						relations['weizoom_shop'] = '%s'%weizoom_shop
				if data == u'微众白富美':
					weizoom_baifumei = table.cell(cur_col,i).value
					if weizoom_baifumei:
						if ';' not in '%s'%weizoom_baifumei:
							weizoom_baifumei = int(weizoom_baifumei)
						relations['weizoom_baifumei'] = '%s'%weizoom_baifumei
				if data == u'商品名称':
					product_name = table.cell(cur_col,i).value
				if data == u'促销标题':
					promotion_title = table.cell(cur_col,i).value
				if data == u'商品价格':
					product_price = table.cell(cur_col,i).value
				if data == u'结算价':
					clear_price = table.cell(cur_col,i).value
				if data == u'限时结算价':
					limit_clear_price = table.cell(cur_col,i).value
				if data == u'有效期':
					valid_time = table.cell(cur_col,i).value
					has_limit_time = 1
					if valid_time == u'无':
						valid_time_from = None
						valid_time_to = None
						has_limit_time = 0
					else:
						valid_time = valid_time.split('/')
						valid_time_from = '%s' %valid_time[0]
						valid_time_to = '%s' %valid_time[1]
				if data == u'商品重量':
					product_weight=table.cell(cur_col,i).value
				if data == u'商品库存':
					product_store=table.cell(cur_col,i).value
					if product_store == u'无限':
						product_store = -1
				if data == u'商品轮播图':
					images = table.cell(cur_col,i).value
					if images:
						images = images.split('\n')
				if data == u'详情':
					remark = table.cell(cur_col,i).value

			try:
				#创建商品
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
				#创建轮播图
				if images:
					image_path2id = {}
					for image_path in images:
						image_path = '%s' %image_path
						image = resource_models.Image.objects.create(
							user = user_profile.user,
							path = image_path
						)
						image_path2id[image_path] = image.id
					for image_path in images:
						image_path = '%s' %image_path
						product_models.ProductImage.objects.create(product=product, image_id=image_path2id[image_path])

				#关联云商通ID
				list_create = []
				for (k,v) in relations.items():
					list_create.append(product_models.ProductHasRelationWeapp(
						product_id = product.id,
						self_user_name = k,
						weapp_product_id = v
					))
				product_models.ProductHasRelationWeapp.objects.bulk_create(list_create)
				#更新商品上架状态
				product_has_relations = product_models.ProductHasRelationWeapp.objects.exclude(weapp_product_id='')
				product_has_relations = product_has_relations.filter(product_id=product.id)
				if len(product_has_relations)>0:
					product_models.Product.objects.filter(id=product.id).update(product_status=1)#{0:未上架,1:已上架}
				else:
					product_models.Product.objects.filter(id=product.id).update(product_status=0)
				print account_name,"========sucecss========"
			except Exception,e:
				print(e)
				print account_name,"========error========"
