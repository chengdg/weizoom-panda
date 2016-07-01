# -*- coding: utf-8 -*-
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
from resource import models as resource_models
from account.models import *
from util import string_util
from panda.settings import ZEUS_HOST
from panda.settings import BASE_DIR

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
			r = requests.post(ZEUS_HOST+'/mall/delivery/?_method=put',data=params)
		else:
			#修改物流
			r = requests.post(ZEUS_HOST+'/mall/delivery/?_method=post',data=params)
		res = json.loads(r.text)
		print('res!!!!!!!')
		print(res)
		if res['data']['result'] == u'SUCCESS':
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
		r = requests.post(ZEUS_HOST+'/mall/order/?_method=post',data=params)
		res = json.loads(r.text)
		print('res!!!!!!!')
		print(res)
		if res['data']['result'] == u'SUCCESS':
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
		json_data, error_rows = _read_file(file_url[1:])
		print json_data
		print ('json_data')

		response = create_response(200)
		return response.get_response()
		
		#发货
		# r = requests.post(ZEUS_HOST+'/mall/delivery/?_method=put',data=params)
		# res = json.loads(r.text)
		# print(res)
		# if res['data']['result'] == u'SUCCESS':
		# 	response = create_response(200)
		# 	return response.get_response()
		# else:
		# 	response = create_response(500)
		# 	response.errMsg = res['data']['msg']
		# 	return response.get_response()

def _read_file(file_url):
	datas = []
	error_rows = []
	file_url_dictionary = file_url.split('/')[2]
	file_name = file_url.split('/')[3]
	file_path = os.path.join(BASE_DIR,'static','upload',file_url_dictionary,file_name)
	print ('file_path')
	print (file_path)
	
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
			item['express_company_name'] = express_company_name
			item['express_number'] = express_number
			datas.append(item)
		else:
			error_rows.append(', '.join(i))

	return datas, error_rows