# -*- coding: utf-8 -*-
import json
import time
import requests
import csv
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
from panda.settings import PROJECT_HOME

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
		json_data, error_rows = _read_file(file_url)
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
	data = []
	error_rows = []
	print ('file_url')
	print file_url
	file_path = os.path.join(PROJECT_HOME, '..', file_url)
	print ('file_path')
	print (file_path)

	# with open(file_path) as csvfile:
	# 	reader = csv.reader(csvfile, delimiter=':', quotechar='|')
	# 	for row in reader:
	# 		try:
	# 			if len(row) > 0:
	# 				item = dict()
	# 				row = row[0].split(',')
	# 				if not (len(row[0]) or len(row[1]) or len(row[2])):
	# 					continue
	# 				item['order_id'] = row[0].decode('gbk')
	# 				item['express_company_name'] = row[1].decode('gbk')
	# 				item['express_number'] = row[2].decode('gbk')
	# 				data.append(item)
	# 		except:
	# 			error_rows.append(', '.join(row))
	# 		# print(', '.join(row))

	# 	csvfile.close()

	# if len(error_rows) > 0:
	# 	alert_message = u"批量发货失败，读取文件错误的行为：error_rows:{}".format(error_rows)
	# 	watchdog_warning(alert_message)

	# return data, error_rows