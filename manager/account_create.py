# -*- coding: utf-8 -*-
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
from core import paginator
from util import db_util
from panda.settings import ZEUS_HOST
import nav
import requests
from account.models import *


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
			user_profile = UserProfile.objects.get(id=user_profile_id)
			user_profile_data = {
				'id': user_profile.id,
				'name': user_profile.name,
				'username': User.objects.get(id=user_profile.user_id).username,
				'account_type': user_profile.role,
				'note': user_profile.note,
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
		name = post.get('name','')
		username = post.get('username','')
		password = post.get('password','')
		note = post.get('note','')

		if not check_username_valid(username):
			response = create_response(500)
			response.errMsg = u'登录账号已存在，请重新输入'
			return response.get_response()
		try:
			user = User.objects.create_user(username,username+'@weizoom.com',password)
			user.first_name = name
			user.save()
			user_profile = UserProfile.objects.filter(user=user)
			user_profile.update(
				manager_id = request.user.id,
				role = account_type,
				name = name,
				note = note
			)
			
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
				print(e)

			if account_zypt_infos:
				list_create = []
				for account_zypt_info in account_zypt_infos:
					print account_zypt_info,"=========ssss2222==========="
					print account_zypt_info['store_name']
					#请求接口获得数据
					try:
						user_id = int(account_zypt_info['user_id'])
						params = {
							'owner_id': user_id,
							'name': 'p-' + user_profile[0].name,
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
									account_id = user_profile[0].id,
									store_name = account_zypt_info['store_name'],
									supplier_id = int(supplier_datas['id'])
								)
						else:
							print(res)
					except Exception,e:
						print(e)
			response = create_response(200)
		except Exception,e:
			print(e)
			print('===========================')
			response = create_response(500)
			response.errMsg = u'创建账号失败'
			response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	@login_required
	def api_post(request):
		#更新账号
		post = request.POST
		password = post.get('password','')
		note = post.get('note','')
		try:
			user_profile = UserProfile.objects.get(id=request.POST['id'])
			user_id = user_profile.user_id
			user = User.objects.get(id=user_id)
			user_profile.note = note
			user_profile.save()
			user.set_password(password)
			user.save()
		except Exception,e:
			print(e)
			print('===========================')
			response = create_response(500)
			response.errMsg = u'编辑账号失败'
			response.innerErrMsg = unicode_full_stack()
		response = create_response(200)
		return response.get_response()

def check_username_valid(username):
	"""
	创建用户时，检查登录账号是否存在
	"""
	user = User.objects.filter(username = username)
	return False if user else True