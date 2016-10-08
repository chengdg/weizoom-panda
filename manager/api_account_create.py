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
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog

from core import resource
from core.jsonresponse import create_response
from util import db_util
from panda.settings import ZEUS_HOST
import nav
import requests

from account.models import *
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
from product_catalog import models as product_catalog_models
from manager.account_create import check_username_valid, sync_create_rebate_info, sync_add_retail_rebate_info
from eaglet.decorator import param_required

# ================================================
# 渠道创建账号使用的接口
# ================================================

class AccountCreateApi(resource.Resource):
	app = 'manager'
	resource = 'account_create_api'
	
	def api_put(request):
		"""
		新建账号
		"""
		args = request.POST
		name = args['name']
		username = args['username']
		password = args['password']
		company_name = args['company_name']
		company_type = args['company_type']
		purchase_method = int(args['purchase_method'])
		contacter = args['contacter']
		phone = args['phone']
		valid_time_from = args['valid_time_from']
		valid_time_to = args['valid_time_to']
		note = args.get('note', '')

		#默认采购方式只是固定低价
		points = args.get('points', 0)
		order_money = args.get('order_money', 0)
		rebate_proport = args.get('rebate_proport', 0)
		default_rebate_proport = args.get('default_rebate_proport', 0)

		if company_type == '' or company_type == '[]' or company_type == '[None]':
			response = create_response(500)
			response.errMsg = u'请选择经营类目'
			return response.get_response()
		
		if not check_username_valid(username):
			response = create_response(500)
			response.errMsg = u'登录账号已存在，请重新输入'
			return response.get_response()
		try:
			user = User.objects.create_user(username,username+'@weizoom.com',password)
			user.first_name = name
			user.save()
			user_id = user.id
			user_profile = UserProfile.objects.filter(user=user)
			points = 0 if points == '' else points

			# 云商通的账户 fixed: 固定低价, divide: 55分成, 零售扣点:retail
			weapp_account_type = 'fixed'
			if purchase_method == 2:
				weapp_account_type = 'retail'
				if points == '':
					response = create_response(500)
					response.errMsg = u'请输入零售扣点'
					return response.get_response()
				else:
					points = float(points)
			if purchase_method == 3:
				if order_money == '' or rebate_proport == '' or default_rebate_proport == '':
					response = create_response(500)
					response.errMsg = u'请输入55分成配置'
					return response.get_response()
				else:
					order_money = int(order_money)
					rebate_proport = int(rebate_proport)
					default_rebate_proport = int(default_rebate_proport)
				weapp_account_type = 'divide'
				AccountHasRebateProport.objects.create(
					user_id = user_id,
					order_money = order_money,
					rebate_proport = rebate_proport,
					default_rebate_proport = default_rebate_proport
				)
			user_profile.update(
				manager_id = 2,
				role = 1,
				name = name,
				note = note,
				company_name = company_name,
				company_type = company_type,
				purchase_method = purchase_method, #默认采购方式只是固定低价
				points = points,
				contacter = contacter,
				phone = phone,
				valid_time_from = valid_time_from,
				valid_time_to = valid_time_to,
				customer_from = 1
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
							sync_create_rebate_info(user_id=user_id, account_relation=account_relation)
						# 同步零售返点
						if purchase_method == 2:
							sync_add_retail_rebate_info(account_relation, user_id=-1, rebate=points)
						response = create_response(200)
						response.data = {
							'supplier_id': int(supplier_datas['id']),
							'account_id': user_profile[0].id
						}
						return response.get_response()
					else:
						User.objects.filter(id=user_id).delete()
						UserProfile.objects.filter(user_id=user_id).delete()
						response = create_response(500)
						response.errMsg = u'创建账号失败'
						return response.get_response()
				else:
					User.objects.filter(id=user_id).delete()
					UserProfile.objects.filter(user_id=user_id).delete()
					response = create_response(500)
					response.errMsg = u'ZEUS创建账号失败'
					return response.get_response()
			except:
				watchdog.error(unicode_full_stack())
				User.objects.filter(id=user_id).delete()
				UserProfile.objects.filter(user_id=user_id).delete()
				response = create_response(500)
				response.errMsg = u'PANDA创建账号失败'
				return response.get_response()
		except:
			watchdog.error(unicode_full_stack())
			User.objects.filter(id=user_id).delete()
			UserProfile.objects.filter(user_id=user_id).delete()
			response = create_response(500)
			response.errMsg = u'PANDA创建账号失败'
			return response.get_response()

	def api_post(request):
		"""
		修改密码
		"""
		args = request.POST
		account_id = args['account_id']
		password = args['password']
		try:
			user_profile = UserProfile.objects.get(id=account_id)
			user_id = user_profile.user_id
			user = User.objects.get(id=user_id)
			user.set_password(password)
			user.save()
			response = create_response(200)
			response.data = u"修改密码成功"
			return response.get_response()
		except Exception,e:
			print e
			response = create_response(200)
			response.data = u"该账号不存在"
			return response.get_response()

class GetAllFirstCatalog(resource.Resource):
	app = 'manager'
	resource = 'get_all_first_catalog_api'

	def api_get(request):
		"""
		获得一级经营类目
		"""
		catalogs = product_catalog_models.ProductCatalog.objects.filter(father_id=-1).order_by('-created_at')
		rows = []
		for catalog in catalogs:
			rows.append({
				'text': catalog.name,
				'value': catalog.id
			})
		response = create_response(200)
		response.data = rows
		return response.get_response()