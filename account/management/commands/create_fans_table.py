# -*- coding: utf-8 -*-

import os
import xlrd
import random
from collections import OrderedDict
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from fans import models as fans_models

class Command(BaseCommand):
	def handle(self, **options):
		datas = []
		file_name_dir = '%s' %'./account/management/commands/fans_info.xlsx'
		data = xlrd.open_workbook(file_name_dir)
		table = data.sheet_by_index(0)
		nrows = table.nrows   #行数

		for i in range(0,nrows):
			item = dict()
			item['weibo_id'] = str(int(table.cell(i,0).value))
			item['name'] = table.cell(i,1).value
			item['fans_url'] = table.cell(i,2).value
			datas.append(item)

		for data in datas:
			fans = fans_models.Fans.objects.create(
				weibo_id = data['weibo_id'],
				name = data['name'],
				fans_url = data['fans_url'],
				male = random.choice([True, False])
			)
			print "==="+u'导入粉丝'+data['weibo_id']+"==="
		print "====="+u'导入粉丝完毕'+"====="