# -*- coding: utf-8 -*-
__author__ = 'lihanyi'

import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.exceptionutil import unicode_full_stack
from core import resource
from core.jsonresponse import create_response
from eaglet.utils.resource_client import Resource

from core import paginator
from eaglet.core import watchdog
from util import db_util
from panda.settings import ZEUS_HOST
import nav
import requests
from account.models import *
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST, PRODUCT_POOL_OWNER_ID


FIRST_NAV = 'manager'
SECOND_NAV = 'account-list'

COUNT_PER_PAGE = 20

filter2field = {
	'account_type': 'role'
}

#创建账号
class AccountCreate(resource.Resource):
	app = 'manager'
	resource = 'account_create'

	@login_required
	def get(request):
		"""
		响应GET
		"""
		user_profile_id = request.GET.get('id', None)
		is_edit = False
		jsons = {'items':[]}
		if user_profile_id:
			user_profile = UserProfile.objects.get(id = user_profile_id)
			# 采购方式:零售价返点(团购扣点)
			group_points = AccountHasGroupPoint.objects.filter(user_id = user_profile.user_id)
			# 采购方式:首月55分成
			rebate_proports = AccountHasRebateProport.objects.filter(user_id = user_profile.user_id)
			self_user_names = []
			if group_points and user_profile.purchase_method == 2:#采购方式:零售价返点
				for group_point in group_points:
					self_user_name = group_point.self_user_name
					self_user_names.append({
						'selfUserName': self_user_name,
						self_user_name+'_value': group_point.group_points
						})

			rebates = []
			if rebate_proports and user_profile.purchase_method == 3:#采购方式:首月55分成
				for rebate_proport in rebate_proports:
					if rebate_proport.order_money_condition:
						rebates.append({
							'orderMoneyCondition': '%.0f' %rebate_proport.order_money_condition,
							'rebateProportCondition': rebate_proport.rebate_proport_condition,
							'defaultRebateProportCondition': rebate_proport.default_rebate_proport_condition,
							'validateFromCondition': rebate_proport.valid_time_from.strftime("%Y-%m-%d %H:%M"),
							'validateToCondition': rebate_proport.valid_time_to.strftime("%Y-%m-%d %H:%M")
							})
			if user_profile.role == CUSTOMER:
				user_profile_data = {
					'id': user_profile.id,
					'name': user_profile.name,
					'company_name': user_profile.company_name,
					'company_type': user_profile.company_type if user_profile.company_type!='' else '[]',
					'purchase_method': user_profile.purchase_method,
					'points': user_profile.points,
					'contacter': user_profile.contacter,
					'phone': user_profile.phone,
					'valid_time_from': '' if not user_profile.valid_time_from else user_profile.valid_time_from.strftime("%Y-%m-%d %H:%M"),
					'valid_time_to': '' if not user_profile.valid_time_to else user_profile.valid_time_to.strftime("%Y-%m-%d %H:%M"),
					'username': User.objects.get(id=user_profile.user_id).username,
					'account_type': user_profile.role,
					'note': user_profile.note,
					'self_user_names': [] if not self_user_names else json.dumps(self_user_names),
					'rebates': [] if not rebates else json.dumps(rebates),
					'max_product': user_profile.max_product
				}
				if rebate_proports and user_profile.purchase_method == 3:#采购方式:首月55分成
					for rebate_proport in rebate_proports:
						if rebate_proport.order_money:
							user_profile_data['order_money'] = '%.0f' %rebate_proport.order_money
							user_profile_data['rebate_proport'] = rebate_proport.rebate_proport
							user_profile_data['default_rebate_proport'] = rebate_proport.default_rebate_proport
			else:
				user_profile_data = {
					'id': user_profile.id,
					'name': user_profile.name,
					'username': User.objects.get(id=user_profile.user_id).username,
					'account_type': user_profile.role,
					'note': user_profile.note
				}
			jsons['items'].append(('user_profile_data', json.dumps(user_profile_data)))
			is_edit = True
		else:
			jsons['items'].append(('user_profile_data', json.dumps(None)))
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
			'jsons': jsons,
			'is_edit': is_edit
		})

		return render_to_response('manager/account_create.html', c)

	@login_required
	def api_put(request):
		post = request.POST
		account_type = post.get('account_type','')
		if account_type == '1':
			company_name = post.get('company_name','')
			company_type = json.loads(post.get('company_type',''))
			purchase_method = int(post.get('purchase_method',1))
			points = post.get('points',0)
			contacter = post.get('contacter','')
			phone = post.get('phone','')
			valid_time_from = post.get('valid_time_from','')
			valid_time_to = post.get('valid_time_to','')
			order_money = post.get('order_money',0)
			rebate_proport = post.get('rebate_proport',0)
			default_rebate_proport = post.get('default_rebate_proport',0)
			self_user_names = post.get('self_user_names','')
			rebates = post.get('rebates','')
			max_product = post.get('max_product',3)
		name = post.get('name','')
		username = post.get('username','')
		password = post.get('password','')
		note = post.get('note','')

		if not check_username_valid(username):
			response = create_response(500)
			response.errMsg = u'登录账号已存在，请重新输入'
			return response.get_response()
		try:
			response = create_response(200)
			user = User.objects.create_user(username,username+'@weizoom.com',password)
			user.first_name = name
			user.save()
			user_id = user.id
			user_profile = UserProfile.objects.filter(user = user)
			user_profile.update(
				manager_id = request.user.id,
				role = account_type,
				name = name,
				note = note
			)
			# 云商通的账户 normal: 普通账户, divide: 55分成
			weapp_account_type = 'normal'
			if account_type == '1':
				points = 0 if not points else float(points)
				if self_user_names and purchase_method == 2: #采购方式:零售价返点
					self_user_names = json.loads(self_user_names)
					list_create = []
					for self_user in self_user_names:
						self_user_name = str(self_user['self_user_name'])
						list_create.append(AccountHasGroupPoint(
							user_id = user_id,
							self_user_name = self_user_name,
							points = points,
							group_points = float(self_user[self_user_name+'_value'])
						))
					AccountHasGroupPoint.objects.bulk_create(list_create)
				# 采购方式:首月55分成
				if purchase_method == 3:
					weapp_account_type = 'divide'
					AccountHasRebateProport.objects.create(
						user_id = user_id,
						order_money = order_money,
						rebate_proport = rebate_proport,
						default_rebate_proport = default_rebate_proport
					)
					# if rebates:
					# 	rebates = json.loads(rebates)
					# 	list_create = []
					# 	for rebate in rebates:
					# 		list_create.append(AccountHasRebateProport(
					# 			user_id = user_id,
					# 			valid_time_from = rebate['validate_from_condition'],
					# 			valid_time_to = rebate['validate_to_condition'],
					# 			order_money_condition = rebate['order_money_condition'],
					# 			rebate_proport_condition = rebate['rebate_proport_condition'],
					# 			default_rebate_proport_condition = rebate['default_rebate_proport_condition']
					# 		))
					# 	AccountHasRebateProport.objects.bulk_create(list_create)

				user_profile.update(
					company_name = company_name,
					company_type = company_type,
					purchase_method = purchase_method,
					points = points,
					contacter = contacter,
					phone = phone,
					valid_time_from = valid_time_from,
					valid_time_to = valid_time_to,
					max_product = max_product
				)
				#请求接口获得数据
				try:
					params = {
						'name': user_profile[0].name,
						'remark': note,
						'responsible_person': u'8000FT',
						'supplier_tel': phone if phone else '13112345678',
						'supplier_address': u'中国 北京',
						'type': weapp_account_type
					}
					resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put({
						'resource': 'mall.supplier',
						"data": params
					})
					if resp and resp['code'] == 200:
						supplier_datas = resp['data']
						if supplier_datas:
							account_relation = AccountHasSupplier.objects.create(
								user_id = user_id,
								account_id = user_profile[0].id,
								# store_name = account_zypt_info['store_name'].encode('utf8'),
								supplier_id = int(supplier_datas['id'])
							)
							# 同步五五分成的返点
							if purchase_method == 3:
								# user_id = user_id,
								# valid_time_from = rebate['validate_from_condition'],
								# valid_time_to = rebate['validate_to_condition'],
								# order_money_condition = rebate['order_money_condition'],
								# rebate_proport_condition = rebate['rebate_proport_condition'],
								# default_rebate_proport_condition = rebate['default_rebate_proport_condition']
								# 'owner_id', 'divide_money', 'basic_rebate', 'rebate', 'supplier_id'
								sync_create_rebate_info(user_id = user_id, account_relation = account_relation)
						pass
					else:
						User.objects.filter(id = user_id).delete()
						UserProfile.objects.filter(user_id = user_id).delete()
						response = create_response(500)
						response.errMsg = u'创建账号失败'
				except:
					msg = unicode_full_stack()
					watchdog.error('{}'.format(msg))
					print msg
					User.objects.filter(id = user_id).delete()
					UserProfile.objects.filter(user_id = user_id).delete()
					response = create_response(500)
					response.errMsg = u'创建账号失败'
					response.innerErrMsg = unicode_full_stack()
					return response.get_response()
		except:
			msg = unicode_full_stack()
			watchdog.error('{}'.format(msg))
			print msg
			response = create_response(500)
			response.errMsg = u'创建账号失败'
			response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	@login_required
	def api_post(request):
		#更新账号
		post = request.POST
		name = post.get('name','')
		password = post.get('password','')
		note = post.get('note','')
		account_type = post.get('account_type','')
		if account_type == '1':
			company_name = post.get('company_name','')
			company_type = post.get('company_type','')
			purchase_method = int(post.get('purchase_method',1))
			if purchase_method == 2:
				points = float(post.get('points',0))
			else:
				points = 0
			contacter = post.get('contacter','')
			phone = post.get('phone','')
			valid_time_from = post.get('valid_time_from','')
			valid_time_to = post.get('valid_time_to','')
			order_money = post.get('order_money',0)
			rebate_proport = post.get('rebate_proport',0)
			default_rebate_proport = post.get('default_rebate_proport',0)
			self_user_names = post.get('self_user_names','')
			max_product = post.get('max_product',3)
			# rebates = post.get('rebates','')
		try:
			user_profile = UserProfile.objects.get(id = request.POST['id'])
			user_id = user_profile.user_id
			user = User.objects.get(id = user_id)
			user_profile.note = note
			user_profile.name = name
			user_profile.save()

			if password != '':
				user.set_password(password)
			user.first_name = name
			user.save()
			supplier_relation = AccountHasSupplier.objects.filter(account_id = user_profile.id).first()
			# 不管咋地先把五五分成的删除,如果下边有需要就进行会进行添加新的.
			old_rebates = AccountHasRebateProport.objects.filter(user_id = user_id)
			old_rebate_ids = [old_rebate.id for old_rebate in old_rebates]

			if old_rebate_ids:
				# 同步把原来的删除了
				sync_delete_rebate_info(old_rebate_ids, supplier_relation)
			old_rebates.delete()
			# 云上通的账户 normal: 普通账户, divide: 55分成
			weapp_account_type = 'normal'
			if account_type == '1':
				UserProfile.objects.filter(id = request.POST['id']).update(
					company_name = company_name,
					company_type = company_type,
					purchase_method = purchase_method,
					points = points,
					contacter = contacter,
					phone = phone,
					valid_time_from = valid_time_from,
					valid_time_to = valid_time_to,
					max_product = post.get('max_product',3)
				)

				if self_user_names and purchase_method == 2: #采购方式:零售价返点
					self_user_names = json.loads(self_user_names)
					AccountHasGroupPoint.objects.filter(user_id = user_id).delete()
					list_create = []
					for self_user in self_user_names:
						self_user_name = str(self_user['self_user_name'])
						list_create.append(AccountHasGroupPoint(
							user_id = user_id,
							self_user_name = self_user_name,
							points = points,
							group_points = float(self_user[self_user_name+'_value'])
						))
					AccountHasGroupPoint.objects.bulk_create(list_create)
				# 采购方式:首月55分成
				if purchase_method == 3:
					weapp_account_type = 'divide'
					AccountHasRebateProport.objects.create(
						user_id = user_id,
						order_money = order_money,
						rebate_proport = rebate_proport,
						default_rebate_proport = default_rebate_proport
					)
					# if rebates:
					# 	rebates = json.loads(rebates)
					# 	list_create = []
					# 	for rebate in rebates:
					# 		list_create.append(AccountHasRebateProport(
					# 			user_id = user_id,
					# 			valid_time_from = rebate['validate_from_condition'],
					# 			valid_time_to = rebate['validate_to_condition'],
					# 			order_money_condition = rebate['order_money_condition'],
					# 			rebate_proport_condition = rebate['rebate_proport_condition'],
					# 			default_rebate_proport_condition = rebate['default_rebate_proport_condition']
					# 		))
					# AccountHasRebateProport.objects.bulk_create(list_create)

					# 同步新的rebate info
					sync_create_rebate_info(user_id, supplier_relation)

				if supplier_relation:
					params = {
						'name': user_profile.name,
						'remark': note,
						'supplier_id': supplier_relation.supplier_id,
						'responsible_person': user_profile.contacter,
						'supplier_tel': phone if phone else '',
						'supplier_address': u'中国 北京',
						# 55分成
						'type': weapp_account_type
					}
					resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post({
						'resource': 'mall.supplier',
						"data": params
					})
					# if resp and resp['code'] == 200:
					# 	response = create_response(200)
				if not supplier_relation:
					params = {
						'name': user_profile.name,
						'remark': note,
						'responsible_person': user_profile.contacter if user_profile.contacter else '8000FT',
						'supplier_tel': phone if phone else '',
						'supplier_address': u'中国 北京',
						'type': weapp_account_type
					}
					resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put({
						'resource': 'mall.supplier',
						"data": params
					})
					if resp and resp['code'] == 200:
						supplier_datas = resp['data']
						if supplier_datas:
							AccountHasSupplier.objects.create(
								user_id=user_id,
								account_id=user_profile.id,
								# store_name = account_zypt_info['store_name'].encode('utf8'),
								supplier_id=int(supplier_datas['id'])
							)
			
		except:
			msg = unicode_full_stack()
			watchdog.error('{}'.format(msg))

			response = create_response(500)
			response.errMsg = u'编辑账号失败'
			response.innerErrMsg = msg
		response = create_response(200)
		return response.get_response()

def check_username_valid(username):
	"""
	创建用户时，检查登录账号是否存在
	"""
	user = User.objects.filter(username = username)
	return False if user else True


def sync_create_rebate_info(user_id, account_relation):
	"""
	同步五五分成
	"""
	rebates = AccountHasRebateProport.objects.filter(user_id = user_id)
	for rebate in rebates:

		rebate_params = {
			'supplier_id': account_relation.supplier_id,
			'owner_id': PRODUCT_POOL_OWNER_ID,
			'divide_money': int(rebate.order_money),
			'basic_rebate': int(rebate.default_rebate_proport),
			'rebate': int(rebate.rebate_proport),
		}
		# print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.'
		# print rebate_params
		# print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.'
		resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put({
			'resource': 'mall.supplier_divide_rebate_info',
			"data": rebate_params
		})
		if not resp or resp.get('code') != 200:
			AccountHasRebateProport.objects.filter(user_id=user_id).delete()
			raise Exception('Sync create rebate info failed!')
		else:

			AccountRebateProportRelation.objects.create(panda_proport_id = rebate.id,
														weapp_divide_id = resp.get('data').get('info').get('id'))


def sync_delete_rebate_info(old_rebate_ids, account_relation):
	"""
	删除weapp那边的五五分成详情.

	"""
	# print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.'
	# print old_rebate_ids
	# print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.'
	rebate_relations = AccountRebateProportRelation.objects.filter(panda_proport_id__in = old_rebate_ids)
	for relation in rebate_relations:
		params = {
			'id': relation.weapp_divide_id,
			'supplier_id': account_relation.supplier_id
		}
		resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).delete({
			'resource': 'mall.supplier_divide_rebate_info',
			"data": params
		})
		if not resp or resp.get('code') != 200:
			raise Exception('Sync update rebate info failed!')
