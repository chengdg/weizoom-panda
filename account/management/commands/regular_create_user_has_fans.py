# -*- coding: utf-8 -*-

import os
import random
import time
import datetime
from collections import OrderedDict
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from fans import models as fans_models
from account import models as account_models
from panda.settings import ZEUS_HOST

class Command(BaseCommand):
	def handle(self, **options):
		day_of_week = datetime.datetime.now().weekday() #0-6是星期一到星期日
		if day_of_week == 0:#周一
			# id_start_with_min = 1
			# id_start_with_max = 2
			id_start_with_min = 3
			id_start_with_max = 4
		elif day_of_week == 1:#周二
			id_start_with_min = 3
			id_start_with_max = 4
		elif day_of_week == 2:#周三
			id_start_with_min = 5
			id_start_with_max = 6
		elif day_of_week == 3:#周四
			id_start_with_min = 7
			id_start_with_max = 8
		elif day_of_week == 4:#周五
			id_start_with = 9
		
		if day_of_week != 4:
			all_sellers_min = account_models.UserProfile.objects.filter(id__startswith=id_start_with_min,role=account_models.CUSTOMER)
			all_sellers_max = account_models.UserProfile.objects.filter(id__startswith=id_start_with_max,role=account_models.CUSTOMER)
			all_sellers = all_sellers_min | all_sellers_max
		else:
			all_sellers =account_models.UserProfile.objects.filter(id__startswith=id_start_with,role=account_models.CUSTOMER)
		user_ids = [seller.user_id for seller in all_sellers]
		account_has_suppliers = account_models.AccountHasSupplier.objects.filter(user_id__in=user_ids)
		today_supplier_ids = []
		supplier_id2orders = {}
		for account_has_supplier in account_has_suppliers:
			if str(account_has_supplier.supplier_id) not in today_supplier_ids:
				today_supplier_ids.append(str(account_has_supplier.supplier_id))
		print 'today_supplier_ids'
		print today_supplier_ids
		
		#请求接口，获得今天需要投放的供应商id本期(1周)对应的订单数
		try:
			today_supplier_ids = '_'.join(today_supplier_ids)
			date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			start_time = datetime.datetime.now()-datetime.timedelta(weeks=1).strftime("%Y-%m-%d %H:%M:%S")
			params = {
				'supplier_ids': today_supplier_ids,
				'start_time': start_time,
				'end_time': date_now
			}
			r = requests.post(ZEUS_HOST+'/panda/order_export_by_supplier/',data=params)
			res = json.loads(r.text)
			if res['code'] == 200:
				orders = res['data']['orders']
				if orders:
					for order in orders:
						if order['supplier'] not in supplier_id2orders:
							supplier_id2orders[order['supplier']] = [order]
						else:
							supplier_id2orders[order['supplier']].append(order)
		except Exception,e:
			print(e)
			print "====="+u'请求接口出错'+"====="
		
		#根据每个今天需要投放的用户进行粉丝投放
		for seller in all_sellers:
			fans_count = 0
			supplier_ids = []
			supplier = account_models.AccountHasSupplier.objects.filter(user_id=seller.user_id)
			supplier_ids = [s.supplier_id for s in supplier]
			fans_count = 0 #每次投放粉丝数
			print "====="+u'投放粉丝完毕'+"====="