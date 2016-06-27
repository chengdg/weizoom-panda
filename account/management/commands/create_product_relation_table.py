# -*- coding: utf-8 -*-

import os
import subprocess
import random
import json

from collections import OrderedDict
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from product import models as product_models
from panda.settings import ZEUS_HOST
import requests
from account.models import *

class Command(BaseCommand):
	def handle(self, **options):
		user_profiles = UserProfile.objects.filter(role=1)
		print "=====start======"
		for user_profile in user_profiles:
			try:
				account_zypt_infos = []
				params = {
					'mall_type': 1
				}
				r = requests.get(ZEUS_HOST+'/account/zypt_info/',params=params)
				res = json.loads(r.text)
				if res['code'] == 200:
					account_zypt_infos = res['data']
				else:
					print(res)
			except Exception,e:
				print "=====[/account/zypt_info]error====="
				print(e)

			if account_zypt_infos:
				list_create = []
				for account_zypt_info in account_zypt_infos:
					#请求接口获得数据
					try:
						user_id = int(account_zypt_info['user_id'])
						params = {
							'owner_id': user_id,
							'name': 'p-' + user_profile.name,
							'remark': '',
							'responsible_person': u'8000FT',
							'supplier_tel': '13112345678',
							'supplier_address': u'中国 北京'
						}
						r = requests.post(ZEUS_HOST+'/mall/supplier/?_method=put',params=params)
						res = json.loads(r.text)
						if res['code'] == 200:
							supplier_datas = res['data']
							if supplier_datas:
								AccountHasSupplier.objects.create(
									user_id = user_id,
									account_id = user_profile.id,
									store_name = account_zypt_info['store_name'],
									supplier_id = int(supplier_datas['id'])
								)
								print account_zypt_info['store_name'],"===success==="
						else:
							print(res)
					except Exception,e:
						print "=====[/mall/supplier]error====="
						print(e)
		print "=====end====="