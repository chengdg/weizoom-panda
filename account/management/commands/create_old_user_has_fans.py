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
from product import models as product_models
from panda.settings import ZEUS_HOST

class Command(BaseCommand):
	def handle(self, **options):
		#FOR TEST
		# all_sellers = account_models.UserProfile.objects.filter(id=3,role=account_models.CUSTOMER)
		all_sellers = account_models.UserProfile.objects.filter(role=account_models.CUSTOMER)
		user_ids = [seller.user_id for seller in all_sellers]
		all_products = product_models.Product.objects.filter(owner_id__in=user_ids)
		product_ids = ['%s'%product.id for product in all_products]
		product_has_relations = product_models.ProductHasRelationWeapp.objects.filter(product_id__in=product_ids).exclude(weapp_product_id='')
		
		#获取用户id与panda商品id之间的关系
		product_id2user_id = {}
		for product in all_products:
			if product.id not in product_id2user_id:
				product_id2user_id[product.id] = product.owner_id
		
		#获取用户id与开始推广时间之间的关系
		user_id2brand_time = {}
		for product_has_relation in product_has_relations:
			product_id = product_has_relation.product_id
			user_id = product_id2user_id[product_id]
			if user_id not in user_id2brand_time:
				user_id2brand_time[user_id] = product_has_relation.created_at
			else:
				#选择同步数据库内时间最早的一条数据作为开始推广时间
				if product_has_relation.created_at < user_id2brand_time[user_id]:
					user_id2brand_time[user_id] = product_has_relation.created_at

		#需要补投放的
		account_ids = []
		for seller in all_sellers:
			if user_id2brand_time.has_key(seller.user_id):
				account_ids.append(seller.id)

		#根据每个今天需要投放的用户进行粉丝投放
		push_sellers = all_sellers.filter(id__in=account_ids)
		for seller in push_sellers:
			account_has_suppliers = account_models.AccountHasSupplier.objects.filter(account_id=seller.id)
			today_supplier_ids = []
			supplier_id2orders = {}
			if user_id2brand_time.has_key(seller.user_id):
				brand_time = user_id2brand_time[seller.user_id]
				yesterday_time = datetime.datetime.now()-datetime.timedelta(days=1)
				
				if (yesterday_time-brand_time) > datetime.timedelta(days=35):
					need_day = 35
					start_time = brand_time
					end_time = brand_time + datetime.timedelta(days=35)
				else:
					need_day = int((yesterday_time-brand_time).days)
					start_time = brand_time
					end_time = yesterday_time
			
			for account_has_supplier in account_has_suppliers:
				if str(account_has_supplier.supplier_id) not in today_supplier_ids:
					today_supplier_ids.append(str(account_has_supplier.supplier_id))
			
			print ("====="+'today create supplier ids:'+"=====")
			print today_supplier_ids
			print ("====================================")

			try:
				supplier_ids = '_'.join(today_supplier_ids)
				params = {
					'supplier_ids': supplier_ids,
					'start_time': start_time.strftime("%Y-%m-%d %H:%M:%S"),
					'end_time': end_time.strftime("%Y-%m-%d %H:%M:%S")
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

			total_order_number = 0
			supplier_ids = []
			order_ids = []
			supplier = account_models.AccountHasSupplier.objects.filter(account_id=seller.id)
			supplier_ids = [s.supplier_id for s in supplier]
			for supplier_id in supplier_ids:
				if supplier_id in supplier_id2orders:
					total_order_number += len(supplier_id2orders[supplier_id])
					for order in supplier_id2orders[supplier_id]:
						order_ids.append(order['order_id'])

			fans_count_per_day = int(total_order_number/need_day/0.2)
			if fans_count_per_day < 33:
				fans_count = 33*need_day #投放人数下限不能低于33
			else:
				fans_count = int(total_order_number/need_day/0.2)*need_day

			user_has_fans = fans_models.UserHasFans.objects.filter(user_id=seller.user_id)
			if user_has_fans.count() > 0:
				except_fans_ids = [u.fans_id for u in user_has_fans]
				fans = fans_models.Fans.objects.all().exclude(id__in=except_fans_ids)[0:fans_count+500]
			else:
				fans = fans_models.Fans.objects.all()[0:fans_count+500]
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
			ordered_index = 0
			for ordered_fans_id in ordered_fans_ids:
				list_create.append(fans_models.UserHasFans(
					user_id = seller.user_id,
					fans_id = ordered_fans_id,
					status = fans_models.ORDERED,
					related_order_id = order_ids[ordered_index]
				))
				ordered_index += 1

			fans_models.UserHasFans.objects.bulk_create(list_create)
			
			
			#已下单，已推荐
			list_create = []
			recommend_index = ordered_index
			for recommend_fans_id in recommend_fans_ids:
				list_create.append(fans_models.UserHasFans(
					user_id = seller.user_id,
					fans_id = recommend_fans_id,
					status = fans_models.RECOMMEND,
					related_order_id = order_ids[recommend_index]
				))
				recommend_index += 1
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

			print ("====="+'create user_has_fans success, account_id:' + str(seller.id) +"=====")
			print ("====="+'create user_has_fans success, need_day:' + str(need_day) +"=====")
		
		print ("====="+'create user_has_fans all success'+"=====")