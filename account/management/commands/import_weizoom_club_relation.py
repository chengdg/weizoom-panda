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
		file_name_dir = '%s' %'./account/management/commands/product_module.xlsx'
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
				product_price = -1
				limit_clear_price = -1
				if data == u'panda客户账号':
					account_name=table.cell(cur_col,i).value