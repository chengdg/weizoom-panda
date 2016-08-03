# -*- coding: utf-8 -*-
__author__ = 'lihanyi'

import json
import time
import requests
import xlrd
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from core import resource
from core.jsonresponse import create_response
from core import paginator
from core.exceptionutil import unicode_full_stack
from util import db_util
from eaglet.utils.resource_client import Resource
from resource import models as resource_models
from account.models import *
from util import string_util
from panda.settings import BASE_DIR
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST

text2express_company_name = {
	'':'',
	u'申通快递': 'shentong',
	u'EMS': 'ems' ,
	u'圆通速递': 'yuantong',
	u'顺丰速运': 'shunfeng',
	u'中通速递': 'zhongtong',
	u'天天快递': 'tiantian',
	u'韵达快运': 'yunda',
	u'百世快递': 'huitongkuaidi',
	u'全峰快递': 'quanfengkuaidi',
	u'德邦物流': 'debangwuliu',
	u'宅急送': 'zhaijisong',
	u'快捷速递': 'kuaijiesudi',
	u'比利时邮政': 'bpost',
	u'速尔快递': 'suer',
	u'国通快递': 'guotongkuaidi',
	u'邮政包裹/平邮': 'youzhengguonei',
	u'如风达': 'rufengda',
	u'优速物流': 'youshuwuliu'
}

class OrderShipInformations(resource.Resource):
	app = 'order'
	resource = 'order_ship_informations'

	@login_required
	def api_put(request):
		#给接口传递发货的参数
		__method = request.POST.get('__method','')
		params = {
			'order_id' : request.POST.get('order_id',''),
			'express_company_name' : request.POST.get('express_company_name',''),
			'express_number' : request.POST.get('express_number',''),
			'leader_name' : request.POST.get('leader_name',''),
			'operator_name' : request.user.username
		}
		if __method == 'put':
			#发货
			res = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put(
				{
					'resource': 'mall.delivery',
					'data': params
				}
			)
		else:
			#修改物流
			res = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post(
				{
					'resource': 'mall.delivery',
					'data': params
				}
			)
		if res and res['data']['result'] == u'SUCCESS':
			response = create_response(200)
			return response.get_response()
		else:
			response = create_response(500)
			response.errMsg = res['data']['msg']
			return response.get_response()

class OrderCompleteShip(resource.Resource):
	app = 'order'
	resource = 'order_complete_ship'

	@login_required
	def api_post(request):
		#修改订单状态（目前仅支持完成）
		params = {
			'order_id' : request.POST.get('order_id',''),
			'action' : 'finish',
			'operator_name' : request.user.username
		}
		res = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post(
			{
				'resource': 'mall.order',
				'data': params
			}
		)
		if res and res['data']['result'] == u'SUCCESS':
			response = create_response(200)
			return response.get_response()
		else:
			response = create_response(500)
			response.errMsg = res['data']['msg']
			return response.get_response()

class OrderBatchDelivery(resource.Resource):
	app = 'order'
	resource = 'order_batch_delivery'

	@login_required
	def api_post(request):
		#给接口传递批量发货的参数
		file_url = request.POST.get('document_path','')
		# 读取文件
		datas, error_rows = _read_file(file_url[1:])
		if error_rows:
			response = create_response(500)
			error_rows = ','.join(error_rows)
			response.errMsg = u'文件第'+error_rows+u'行格式错误'
			return response.get_response()
		datas = json.dumps(datas)
		params = {
			'datas' : datas
		}
		#发货
		res = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put(
			{
				'resource': 'panda.batch_delivery',
				'data': params
			}
		)
		if res and res['code'] == 200:
			err_msg = ''
			datas = res['data']
			order_ids = []
			for data in datas:
				if not data['result']:
					order_ids.append(data['order_id'])
			for data in datas:
				if not data['result']:
					order_id_str = ','.join(order_ids)
					err_msg = u"订单:"+order_id_str+','+data['msg']
			if err_msg!='':
				response = create_response(500)
				response.errMsg = err_msg
				return response.get_response()
			else:
				response = create_response(200)
				return response.get_response()
		else:
			response = create_response(500)
			response.errMsg = res['data']['msg']
			return response.get_response()

def _read_file(file_url):
	datas = []
	error_rows = []
	file_url_dictionary = file_url.split('/')[2]
	file_name = file_url.split('/')[3]
	file_path = os.path.join(BASE_DIR,'static','upload',file_url_dictionary,file_name)
	
	data = xlrd.open_workbook(file_path)
	table = data.sheet_by_index(0)
	nrows = table.nrows   #行数
	for i in range(1,nrows):
		item = dict()
		order_id = table.cell(i,1).value
		express_company_name = table.cell(i,2).value
		express_number = table.cell(i,3).value
		
		#EXCEL中直接输入的数字可能会被当成浮点数
		if type(order_id) == float:
			order_id = str(int(order_id))
		if type(express_number) == float:
			express_number = str(int(express_number))
		
		if (order_id and express_company_name and express_number)!= '':
			item['order_id'] = order_id
			if express_company_name not in text2express_company_name:
				error_rows.append(str(i))
			else:
				item['express_company_name'] = text2express_company_name[express_company_name]
				item['express_number'] = express_number
				datas.append(item)
		else:
			error_rows.append(str(i))

	return datas, error_rows