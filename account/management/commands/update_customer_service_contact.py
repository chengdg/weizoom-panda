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

#对已有的云商通8000客户商品更新商品价格等于结算价
class Command(BaseCommand):
	def handle(self, **options):
		file_name_dir = '%s' %'./account/management/upload_file/update_customer_service_contact.xls'
		table_title_list = []
		data = xlrd.open_workbook(file_name_dir)
		table = data.sheet_by_index(0)
		nrows = table.nrows              #行数
		ncols = table.ncols                 #列数

		users = User.objects.all()
		user_name2user_id = {user.username:user.id for user in users}
		print "-----start-----"
		total_account = 0
		sucess_account = 0
		for cur_col in range(1,nrows):
			for i in range(0,ncols):
				data_name = table.cell(0,i).value
				data_value = table.cell(cur_col,i).value
				if data_name == u'登录账号':
					username = data_value
				if data_name == u'客服电话':
					if data_value and '-' in str(data_value):
						data_value = '%s'% data_value
					elif data_value and '-' not in str(data_value):
						data_value = '%s'% int(data_value)
					else:
						data_value = ''
					customer_service_tel = data_value 
				if data_name == u'客服qq':
					customer_service_qq = '' if not data_value else '%s'% int(data_value)
			try:
				if username in user_name2user_id:
					user_id = user_name2user_id[username]
					account_models.UserProfile.objects.filter(user_id=user_id).update(
						customer_service_tel = customer_service_tel,
						customer_service_qq_first = customer_service_qq
					)
					sucess_account += 1
					print username,customer_service_tel,customer_service_qq,"========="
			except Exception,e:
				print "-----error-----"
			total_account+=1
		print total_account,"-----total_account-----"
		print sucess_account,"-----sucess_account-----"
