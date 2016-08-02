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
from util import db_util
import requests

import models
import nav
from product_catalog import models as product_catalog_models


FIRST_NAV = 'business'
SECOND_NAV = 'business'

COUNT_PER_PAGE = 10

filter2field = {
}

#创建账号
class BusinessDetail(resource.Resource):
	app = 'business'
	resource = 'business_detail'

	@login_required
	def get(request):
		"""
		响应GET
		"""
		business_id = request.GET.get('id', None)
		jsons = {'items':[]}
		if business_id:
			business = models.Business.objects.get(id=business_id)
			business_data = {
				'id': business.id,
				'company_type': business.company_type,
				'company_name': business.company_name,
				'company_money': business.company_money,
				'legal_representative': business.legal_representative,
				'contacter': business.contacter,
				'phone': business.phone,
				'e_mail': business.e_mail,
				'we_chat_and_qq': business.we_chat_and_qq,
				'company_location': business.company_location,
				'address': business.address,
				'business_license': [{'id':1,'path':business.business_license}],
				'business_license_time': business.business_license_time.strftime("%Y-%m-%d %H:%M"),
				'tax_registration_certificate': [{'id':2,'path':business.tax_registration_certificate}],
				'tax_registration_certificate_time': business.tax_registration_certificate_time.strftime("%Y-%m-%d %H:%M"),
				'organization_code_certificate': [{'id':3,'path':business.organization_code_certificate}],
				'organization_code_certificate_time': business.organization_code_certificate_time.strftime("%Y-%m-%d %H:%M"),
				'account_opening_license': [{'id':4,'path':business.account_opening_license}],
				'account_opening_license_time': business.account_opening_license_time.strftime("%Y-%m-%d %H:%M")
			}
			jsons['items'].append(('business_data', json.dumps(business_data)))

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
			'jsons': jsons
		})
		return render_to_response('business/business_detail.html', c)

	@login_required
	def api_post(request):
		#修改入驻申请
		post = request.POST
		
		response = create_response(200)
		return response.get_response()