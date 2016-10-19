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

class Shipper(resource.Resource):
	"""
	运费模板列表
	"""
	app = 'postage_config'
	resource = 'shipper'

	@login_required
	def api_get(request):
		shipper_id = request.GET.get('shipper_id', None)
		shipper_messages = models.ShipperMessages.objects.filter(owner=request.user, is_deleted=False)
		if shipper_id:
			shipper_messages = shipper_messages.filter(id=shipper_id)
		
		messages = []
		for shipper_message in shipper_messages:
			messages.append({
				'shipperId': shipper_message.id,
				'shipperName': shipper_message.shipper_name,
				'telNumber': shipper_message.tel_number,
				'destination': shipper_message.destination,
				'address': shipper_message.address,
				'postcode': shipper_message.postcode,
				'companyName': shipper_message.company_name,
				'remark': shipper_message.remark
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
		shipper_name = request.POST.get('shipper_name','')
		address = request.POST.get('address','')
		postcode = request.POST.get('postcode','')
		tel_number = request.POST.get('tel_number','')
		company_name = request.POST.get('company_name','')
		remark = request.POST.get('remark','')

		models.ShipperMessages.objects.create(
			owner = request.user,
			shipper_name = shipper_name,
			tel_number = tel_number,
			destination = '',
			address = address,
			postcode = postcode,
			company_name= company_name,
			remark = remark
		)
		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		shipper_id = request.POST.get('shipper_id',-1)
		shipper_name = request.POST.get('shipper_name','')
		address = request.POST.get('address','')
		postcode = request.POST.get('postcode','')
		tel_number = request.POST.get('tel_number','')
		company_name = request.POST.get('company_name','')
		remark = request.POST.get('remark','')

		models.ShipperMessages.objects.filter(id=shipper_id).update(
			shipper_name = shipper_name,
			tel_number = tel_number,
			destination = '',
			address = address,
			postcode = postcode,
			company_name= company_name,
			remark = remark
		)
		response = create_response(200)
		return response.get_response()

	@login_required
	def api_delete(request):
		shipper_id = request.POST.get('shipper_id',-1)
		models.ShipperMessages.objects.filter(id=shipper_id).update(is_deleted=True)
		response = create_response(200)
		return response.get_response()