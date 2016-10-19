# -*- coding: utf-8 -*-
import json

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response

from product import models as product_models
from account import models as account_models
from util import sync_util
import nav
import models

FIRST_NAV = 'postage_config'
SECOND_NAV = 'shipper_manage'
COUNT_PER_PAGE = 20

class ExpressBill(resource.Resource):
	"""
	运费模板列表
	"""
	app = 'postage_config'
	resource = 'express_bill'

	@login_required
	def api_get(request):
		express_bill_accounts = models.ExpressBillAccount.objects.filter(owner=request.user)
		messages = []
		for express_bill_account in express_bill_accounts:
			messages.append({
				'expressId': express_bill_account.id,
				'expressName': express_bill_account.express_name,
				'customerName': express_bill_account.customer_name,
				'customerPwd': express_bill_account.customer_pwd,
				'logisticsNumber': express_bill_account.logistics_number,
				'remark': express_bill_account.remark
			})

		data = {
			'rows': messages
		}	

		# 构造response
		response = create_response(200)
		response.data = data
		return response.get_response()

	@login_required
	def api_put(request):
		express_name = request.POST.get('express_name','')
		customer_name = request.POST.get('customer_name','')
		customer_pwd = request.POST.get('customer_pwd','')
		logistics_number = request.POST.get('logistics_number','')
		remark = request.POST.get('remark','')

		models.ExpressBillAccount.objects.create(
			owner = request.user,
			express_name = express_name,
			customer_name = customer_name,
			customer_pwd = customer_pwd,
			logistics_number = logistics_number,
			remark = remark
		)
		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		express_id = request.POST.get('express_id',-1)
		express_name = request.POST.get('express_name','')
		customer_name = request.POST.get('customer_name','')
		customer_pwd = request.POST.get('customer_pwd','')
		logistics_number = request.POST.get('logistics_number','')
		remark = request.POST.get('remark','')

		models.ExpressBillAccount.objects.filter(id=express_id).update(
			express_name = express_name,
			customer_name = customer_name,
			customer_pwd = customer_pwd,
			logistics_number = logistics_number,
			remark = remark
		)
		response = create_response(200)
		return response.get_response()

	@login_required
	def api_delete(request):
		express_id = request.POST.get('express_id',-1)
		models.ExpressBillAccount.objects.filter(id=express_id).delete()
		response = create_response(200)
		return response.get_response()

