# -*- coding: utf-8 -*-
__author__ = 'lihanyi'

import os
import xlrd
import random
from collections import OrderedDict
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from account import models as account_models
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
from eaglet.utils.resource_client import Resource

#批量处理公司名称
class Command(BaseCommand):
	def handle(self, **options):
		datas = []
		file_name_dir = '%s' %'./account/management/upload_file/company_name.xls'
		data = xlrd.open_workbook(file_name_dir)
		table = data.sheet_by_index(0)
		nrows = table.nrows   #行数
		errors = []
		print "====="+'loading xlsx file'+"====="
		for i in range(1,nrows):
			item = dict()
			item['account_id'] = int(table.cell(i,0).value)
			item['company_name'] = table.cell(i,2).value.strip()
			datas.append(item)
		
		for data in datas:
			try:
				account_info = account_models.UserProfile.objects.get(id=data['account_id'])
				account_info.company_name = data['company_name']
				account_info.save()
				print "==="+'updating company_name:'+str(data['account_id'])+"==="
			except Exception,e:
				errors.append({
					'account_id': data['account_id']
				})
				print "==="+'error:user is not exsit:'+str(data['account_id'])+"==="
			
		if errors:
			print "====="+'error info'+"====="
			print errors
		else:
			print "====="+'updating company_name all success'+"====="