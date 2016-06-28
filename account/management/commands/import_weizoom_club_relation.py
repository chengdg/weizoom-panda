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
from account.models import *

class Command(BaseCommand):
	def handle(self, **options):
		file_name_dir = '%s' %'./account/management/commands/weizoom_club.xlsx'
		table_title_list = []
		data = xlrd.open_workbook(file_name_dir)
		table = data.sheet_by_index(0)
		nrows = table.nrows              #行数
		ncols = table.ncols                 #列数
		data = table.cell(0, 1).value
		for i in range(0,ncols):
			table_content=table.cell(0,i).value
			table_title_list.append(table_content)
		print "-----start-----"
		for cur_col in range(1,nrows):
			#关联云商通ID
			list_create = []
			for i in range(0,ncols):
				data = table.cell(0, i).value
				if data == u'俱乐部ID':
					club_weapp_id = table.cell(cur_col,i).value
				if data == u'体验系统id':
					product_id = table.cell(cur_col,i).value
			try:
				product_models.ProductHasRelationWeapp.objects.create(
					product_id = product_id,
					self_user_name = 'weizoom_club',
					weapp_product_id = club_weapp_id
				)
				print product_id,"===sucess=="
			except Exception,e:
				print(e)
				print "===error=="
		print "-----end-----"