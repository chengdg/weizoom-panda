# -*- coding: utf-8 -*-
import json
import os
import random
import time
import datetime
import requests
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
			id_start_with_min = 1
			id_start_with_max = 2
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
		print ("====="+'today create supplier ids:'+"=====")
		print today_supplier_ids
		print ("====================================")
		#请求接口，获得今天需要投放的供应商id本期(1周)对应的订单数
		try:
			today_supplier_ids = '_'.join(today_supplier_ids)
			date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			start_time = (datetime.datetime.now()-datetime.timedelta(weeks=1)).strftime("%Y-%m-%d %H:%M:%S")
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
			print ("====="+'error in zeus'+"=====")

		#根据每个今天需要投放的用户进行粉丝投放
		for seller in all_sellers:
			total_order_number = 0
			supplier_ids = []
			order_ids = []
			supplier = account_models.AccountHasSupplier.objects.filter(user_id=seller.user_id)
			supplier_ids = [s.supplier_id for s in supplier]
			for supplier_id in supplier_ids:
				total_order_number += len(supplier_id2orders[supplier_id])
				for order in supplier_id2orders[supplier_id]:
					order_ids.append(order['order_id'])

			fans_count = int(total_order_number/0.2) #每次投放粉丝数
			if fans_count < 210:
				fans_count = 210 #投放人数下限不能低于210
			
			user_has_fans = fans_models.UserHasFans.objects.filter(user_id=seller.user_id)
			if user_has_fans.count() > 0:
				except_fans_ids = [u.fans_id for u in user_has_fans]
				fans = fans_models.Fans.objects.all().exclude(id__in=except_fans_ids)[0:fans_count+500]
			else:
				fans = fans_models.Fans.objects.all()[0:fans_count+1000]
			selected_fans_ids = []
			all_fans_ids = [fan.id for fan in fans]
			selected_fans_ids = random.sample(all_fans_ids,fans_count) #从id池中随机获取fans_count个元素
			
			#已妥投，未阅读
			delivered_fans_ids = selected_fans_ids[0:int(fans_count*0.18)]
			list_create = []
			for delivered_fans_id in delivered_fans_ids:
				list_create.append(fans_models.UserHasFans(
					user_id = seller.user_id,
					fans_id = delivered_fans_id,
					status = fans_models.DELIVERED
				))
			fans_models.UserHasFans.objects.bulk_create(list_create)
			
			#已阅读，未分享
			readed_fans_ids = selected_fans_ids[int(fans_count*0.18):int(fans_count*0.25)]
			list_create = []
			for readed_fans_id in readed_fans_ids:
				list_create.append(fans_models.UserHasFans(
					user_id = seller.user_id,
					fans_id = readed_fans_id,
					status = fans_models.READED
				))
			fans_models.UserHasFans.objects.bulk_create(list_create)
			
			#已阅读，已分享
			shared_fans_ids = selected_fans_ids[int(fans_count*0.25):int(fans_count*0.37)]
			list_create = []
			for shared_fans_id in shared_fans_ids:
				list_create.append(fans_models.UserHasFans(
					user_id = seller.user_id,
					fans_id = shared_fans_id,
					status = fans_models.SHARED
				))
			fans_models.UserHasFans.objects.bulk_create(list_create)

			#已下单
			actual_ordered_fans_ids = selected_fans_ids[int(fans_count*0.37):][0:total_order_number] #[投放粉丝池中剩下的全部][0:订单数]
			ordered_fans_ids = actual_ordered_fans_ids[0:int(len(actual_ordered_fans_ids)*0.8)] #未推荐：云商通实际下单人数的80%
			recommend_fans_ids = actual_ordered_fans_ids[int(len(actual_ordered_fans_ids)*0.8):] #已推荐：云商通实际下单人数的20%
			#已下单，未推荐
			list_create = []
			i = 0
			for ordered_fans_id in ordered_fans_ids:
				list_create.append(fans_models.UserHasFans(
					user_id = seller.user_id,
					fans_id = ordered_fans_id,
					status = fans_models.ORDERED,
					related_order_id = order_ids[i]
				))
				i+=1
			fans_models.UserHasFans.objects.bulk_create(list_create)

			#已下单，已推荐
			list_create = []
			for recommend_fans_id in recommend_fans_ids:
				list_create.append(fans_models.UserHasFans(
					user_id = seller.user_id,
					fans_id = recommend_fans_id,
					status = fans_models.RECOMMEND,
					related_order_id = order_ids[i]
				))
				i+=1
			fans_models.UserHasFans.objects.bulk_create(list_create)
			already_create_fans_ids = delivered_fans_ids+readed_fans_ids+shared_fans_ids+ordered_fans_ids+recommend_fans_ids
			remain_fans_ids = list(set(selected_fans_ids).difference(set(already_create_fans_ids)))
			if len(remain_fans_ids)>0:
				#如果还有剩余未投放的粉丝（订单数过少导致）
				#已妥投，未阅读
				list_create = []
				for remain_fans_id in remain_fans_ids:
					list_create.append(fans_models.UserHasFans(
						user_id = seller.user_id,
						fans_id = remain_fans_id,
						status = fans_models.DELIVERED
					))
				fans_models.UserHasFans.objects.bulk_create(list_create)

			print ("====="+'create user_has_fans success, user_id:' + str(seller.user_id) +"=====")
		
		print ("====="+'create user_has_fans all success'+"=====")