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
		current_all_fans = fans_models.Fans.objects.all()
		already_has_weibo_ids = [fans.weibo_id for fans in current_all_fans]
		print "====="+'loading xlsx file'+"====="
		for i in range(0,nrows):
			item = dict()
			weibo_id = str(int(table.cell(i,0).value))[:7]
			if weibo_id not in already_has_weibo_ids:
				item['weibo_id'] = weibo_id
				item['name'] = table.cell(i,1).value
				item['fans_url'] = table.cell(i,2).value
				datas.append(item)
		for data in datas:
			fans = fans_models.Fans.objects.create(
				weibo_id = data['weibo_id'],
				name = data['name'],
				fans_url = data['fans_url'],
				purchasing_index = get_5_98_random(),
				spread_index = get_5_98_random()
			)
			print "==="+'creating fans:'+data['weibo_id']+"==="
		print "====="+'creating fans success'+"====="
		print "====="+'total create fans amount:'+str(len(datas))+"====="

def get_5_98_random():
	random_float = float("%.1f" % (random.random()*10))
	if random_float > 9.8:
		return random_float - 1
	elif random_float < 5:
		return random_float + 5
	return random_float