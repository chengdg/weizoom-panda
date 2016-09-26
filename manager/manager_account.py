# -*- coding: utf-8 -*-
__author__ = 'lihanyi'

import json
import time
import datetime
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
import nav
import requests
from account.models import *
from product.models import *
from product_catalog import models as catalog_models
from excel_response import ExcelResponse
from panda.settings import AXE_HOST

FIRST_NAV = 'manager'
SECOND_NAV = 'account-list'

COUNT_PER_PAGE = 20

filter2field = {
	'account_type': 'role'
}

#账号管理列表
class ManagerAccount(resource.Resource):
	app = 'manager'
	resource = 'account'

	@login_required
	def get(request):
		"""
		响应GET
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV
		})
		
		return render_to_response('manager/account_list.html', c)

	@login_required
	def api_get(request):
		is_for_list = True if request.GET.get('is_for_list') else False #是列表还是导出
		cur_page = request.GET.get('page', 1)
		accounts = UserProfile.objects.filter(is_active=True).exclude(role=MANAGER).order_by('-id')
		catalogs = catalog_models.ProductCatalog.objects.filter(father_id=-1)
		catalog_id2name = dict((catalog.id,catalog.name) for catalog in catalogs)
		filters = dict([(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET if key.startswith('__f-')])
		company_name = filters.get('companyName','')
		username = filters.get('username','')
		role = filters.get('accountType','')
		status = filters.get('status','')
		# customer_from = filters.get('customerFrom','')
		if company_name:
			accounts = accounts.filter(company_name__icontains=company_name)
		if username:
			user_ids = [user.id for user in User.objects.filter(username__icontains=username)]
			accounts = accounts.filter(user_id__in=user_ids)
		if role:
			accounts = accounts.filter(role=role)
		if status:
			if status == '1':
				accounts = accounts.filter(status=status)
			else:
				accounts = accounts.exclude(status=1)
		# if customer_from: 客户来源暂时渠道没有接口实现，先注释
		# 	print customer_from
		if is_for_list:
			pageinfo, accounts = paginator.paginate(accounts, cur_page, COUNT_PER_PAGE)

		user_ids = [account.user_id for account in accounts]
		user_id2username = {user.id: user.username for user in User.objects.filter(id__in=user_ids)}
		rows = []
		date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		#从渠道接口获得客户来源字段
		company_name2info = {}
		company_names = []
		for account in accounts:
			if account.company_name != '':
				company_names.append(account.company_name)
		company_names = '_'.join(company_names)
		company_name2info = get_info_from_axe(company_names)

		for account in accounts:
			#关闭已过期的账号/开启可以登录的账号
			if account.valid_time_from and account.valid_time_to:
				valid_time_from = account.valid_time_from.strftime("%Y-%m-%d %H:%M:%S")
				valid_time_to = account.valid_time_to.strftime("%Y-%m-%d %H:%M:%S")
				if valid_time_from <= date_now and date_now < valid_time_to and account.status != 0:
					account.status = 1
					account.save()
				elif date_now >= valid_time_to or date_now <= valid_time_from:
					account.status = 2
					account.save()

			customerFrom = '--' 
			if account.role == 1 :
				catalog_names = []
				if account.company_type != '':
					#获得经营类目的名称
					catalog_ids = json.loads(account.company_type)
					for catalog_id in catalog_ids:
						catalog_names.append(catalog_id2name.get(catalog_id, ''))
				catalog_names = ','.join(catalog_names)

				#客户来源
				if company_name2info.has_key(account.company_name):
					customerFrom = company_name2info[account.company_name]
				else:
					customerFrom = '渠道' if account.customer_from == 1 else '--' #如果从渠道没有找到匹配的，给默认值
			else:
				catalog_names = '--'
			if is_for_list:
				rows.append({
					'id': account.id,
					'name': account.name,
					'companyName': account.company_name,
					'username': user_id2username[account.user_id],
					'companyType': catalog_names,
					'purchaseMethod': METHOD2NAME[account.purchase_method] if account.role == 1 else '--',
					'accountType': ROLE2NAME[account.role],
					'status': account.status,
					'maxProduct': account.max_product if account.role == CUSTOMER else '--',
					'customerFrom': customerFrom
				})
			else: #导出
				rows.append({
					'id': account.id,
					'user_id': account.user_id,
					'phone': account.phone,
					'name': account.name,
					'contacter': account.contacter,
					'purchase_method': METHOD2NAME[account.purchase_method] if account.role == 1 else '--',
					'username': user_id2username[account.user_id],
					'role': ROLE2NAME[account.role],
					'note': account.note,
					'company_name': account.company_name,
					'companyType': catalog_names
				})
		if is_for_list:
			data = {
				'rows': rows,
				'pagination_info': pageinfo.to_dict()
			}
			#构造response
			response = create_response(200)
			response.data = data
			return response.get_response()
		else:
			return rows

	@login_required
	def api_post(request):
		#更新账户状态
		account_id = request.POST.get('id','')
		status = request.POST.get('method','')
		if status == 'close':
			change_to_status = 0
		else:
			change_to_status = 1
		try:
			UserProfile.objects.filter(id=account_id).update(
				status = change_to_status
			)
			response = create_response(200)
			return response.get_response()
		except:
			response = create_response(500)
			response.errMsg = u'该账号不存在，请检查'
			return response.get_response()

	@login_required
	def api_delete(request):
		account_id = request.POST.get('id','')
		try:
			user_profile = UserProfile.objects.filter(id=account_id)
			user_profile.update(is_active=False)
			user_id = user_profile.first().user_id
			User.objects.filter(id=user_id).update(
				username= 'del_at_'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), #为了删除之后能创建相同username的账号，把用户名改成时间戳
				is_active=False
				)
			products = Product.objects.filter(owner_id=user_id)
			if products:
				products.update(is_deleted=True)
				product_ids = [product.id for product in products]
				ProductHasRelationWeapp.objects.filter(product_id__in=product_ids).delete()
			AccountHasSupplier.objects.filter(account_id=account_id).delete()
			response = create_response(200)
			return response.get_response()
		except Exception,e:
			print e
			response = create_response(500)
			response.errMsg = u'该账号不存在，请检查'
			return response.get_response()

class ExportAccounts(resource.Resource):
	app = 'manager'
	resource = 'account_export'

	@login_required
	def get(request):
		accounts = ManagerAccount.api_get(request)
		titles = [
			u'账号id', u'对应user_id', u'账号类型', u'账号名称', u'登录账号', u'公司名称',
			u'联系人', u'手机号', u'采购方式', u'备注', u"经营类目"
		]
		table = []
		table.append(titles)
		for account in accounts:
			table.append([
				account['id'],
				account['user_id'],
				account['role'],
				account['name'],
				account['username'],
				account['company_name'],
				account['contacter'],
				account['phone'],
				account['purchase_method'],
				account['note'],
				account['companyType']
			])
		return ExcelResponse(table, output_name=u'账号管理文件'.encode('utf8'), force_csv=False)

#从渠道获得账号列表的客户来源信息
def get_info_from_axe(company_names):
	company_name2info = {}
	params = {
		'name': company_names
	}
	try:
		r = requests.post(AXE_HOST + '/api/customers/', data=params, timeout=8)
		res = json.loads(r.text)
		if res and res['code'] == 200:
			axe_datas = res['data']
			for axe_data in axe_datas:
				for (k,v) in axe_data.items():
					agengt2sale = v['agent']+'-'+v['sale']
					company_name2info[k] = agengt2sale
	except:
		pass
	return company_name2info

#从渠道获得公司信息
class GetCompanyInfoFromAxe(resource.Resource):
	app = 'manager'
	resource = 'get_company_info_from_axe'

	@login_required
	def api_get(request):
		company_name = request.GET.get('companyName','')
		params = {
			'name': company_name
		}
		r = requests.post(AXE_HOST + '/api/customers/', data=params)
		res = json.loads(r.text)

		rows = []
		if res and res['code'] == 200:
			axe_datas = res['data']
			#因为reactman的FormSelect没有onClick事件，只有onChange事件，不添加第一个默认值的话无法触发onChange事件
			if len(axe_datas) > 0:
				rows.append({
					'text': '请选择已有公司',
					'value': ''+ '/' +''
				})
			for axe_data in axe_datas:
				for (k,v) in axe_data.items():
					rows.append({
						'text': v['name'],
						'value': v['contact']+ '/' +v['tel']  #把联系人、手机号通过“/”分割开传到前台
					})
		data = {
			'rows': rows
		}
		response = create_response(200)
		response.data = data
		return response.get_response()