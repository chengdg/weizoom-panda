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


class Command(BaseCommand):
	def handle(self, **options):
		datas = []
		file_name_dir = '%s' %'./account/management/commands/sync_customer_phone_1.xlsx'
		data = xlrd.open_workbook(file_name_dir)
		table = data.sheet_by_index(0)
		nrows = table.nrows   #行数
		print "====="+'loading xlsx file'+"====="
		for i in range(0,nrows):
			item = dict()
			item['username'] = table.cell(i,0).value
			item['phone'] = str(int(table.cell(i,1).value))
			datas.append(item)
		for data in datas:
			print data
			try:
				user_id = User.objects.get(username=data['username']).id
				account = account_models.UserProfile.objects.filter(user_id=user_id).update(
					phone = data['phone']
				)
				new_relation = [re.supplier_id for re in account_models.AccountHasSupplier.objects.filter(user_id=user_id)]
				old_relation = [re.supplier_id for re in account_models.AccountHasSupplier.objects.filter(user_id=-user_id)]
				supplier_ids = old_relation + new_relation
				for supplier_id in supplier_ids:
					param = {
						'name': account.name,
						'remark': '',
						'responsible_person': u'8000FT',
						'supplier_tel': account.phone,
						'supplier_address': u'中国 北京',
						'supplier_id': supplier_id
					}

					resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post({
						'resource': 'mall.supplier',
						"data": param
					})
					if resp and resp.get('code') == 200:
						print '++++++++++++++++++++++++++++++++++++++++++++++='

				print "==="+'changing user:'+data['username']+"==="
			except:
				print "==="+'error:user is not exsit'+data['username']+"==="
			
		print "====="+'changing user success'+"====="
		print "====="+'total changing users amount:'+str(len(datas))+"====="