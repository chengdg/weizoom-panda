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
		all_sellers = account_models.UserProfile.objects.filter(role=CUSTOMER)
		account_has_suppliers = account_models.AccountHasSupplier.objects.all()
		all_supplier_ids = []
		supplier_id2orders = {}
		for account_has_supplier in account_has_suppliers:
			if str(account_has_supplier.supplier_id) not in all_supplier_ids:
				all_supplier_ids.append(str(account_has_supplier.supplier_id))
		
		#请求接口，获得所有的供应商id对应的订单数
		try:
			params = {
				'supplier_ids': supplier_ids
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
		
		#根据每个用户进行粉丝投放
		for seller in all_sellers:
			fans_count = 0
			supplier_ids = []
			supplier = account_models.AccountHasSupplier.objects.filter(user_id=seller.user_id)
			supplier_ids = [s.supplier_id for s in supplier]
			fans_count = 0 #每次投放粉丝数
			print "====="+u'投放粉丝完毕'+"====="