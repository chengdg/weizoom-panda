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

filter2field = {
}

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
		apply_catalogs = []
		upload_business_qualifications = []
		if business_id:
			business = models.Business.objects.get(id=business_id)
			#得到所属的二级分类数据
			product_catalog_ids = business.product_catalog_ids.split('_')
			for product_catalog_id in product_catalog_ids:
				apply_catalogs.append(product_catalog_id)

			#得到商家上传的特殊资质
			all_qualifications = product_catalog_models.ProductCatalogQualification.objects.filter(catalog_id__in=product_catalog_ids)
			qualification_id2name = dict((qualification.id,qualification.name) for qualification in all_qualifications)
			qualification_id2catalog_id = dict((qualification.id,qualification.catalog_id) for qualification in all_qualifications)

			qualifications = models.BusinessQualification.objects.filter(business_id=business_id)
			for qualification in qualifications:
				upload_business_qualifications.append({
					'belong_catalog_id': qualification_id2catalog_id[qualification.qualification_id],
					'qualification_id': qualification.qualification_id,
					'qualification_name': qualification_id2name[qualification.qualification_id],
					'img': [{'id':1,'path':qualification.path}],
					'qualification_time': qualification.qualification_time.strftime("%Y-%m-%d %H:%M")
				})
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
				'tax_registration_certificate': [{'id':1,'path':business.tax_registration_certificate}],
				'tax_registration_certificate_time': business.tax_registration_certificate_time.strftime("%Y-%m-%d %H:%M"),
				'organization_code_certificate': [{'id':1,'path':business.organization_code_certificate}],
				'organization_code_certificate_time': business.organization_code_certificate_time.strftime("%Y-%m-%d %H:%M"),
				'account_opening_license': [{'id':1,'path':business.account_opening_license}],
				'account_opening_license_time': business.account_opening_license_time.strftime("%Y-%m-%d %H:%M"),
				'apply_catalogs': apply_catalogs,
				'upload_business_qualifications': upload_business_qualifications
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
		print post
		print '================='
		business_id = post.get('id')
		company_type = int(post.get('company_type',2))
		company_name = post.get('company_name','')
		company_money = float(post.get('company_money')) if post.get('company_money')!='' else 0
		legal_representative = post.get('legal_representative','')
		contacter = post.get('contacter','')
		phone = post.get('phone','')
		e_mail = post.get('e_mail','')
		we_chat_and_qq = post.get('we_chat_and_qq','')
		company_location = post.get('company_location','')
		address = post.get('address','')
		business_license = json.loads(post.get('business_license',''))[0]['path']
		business_license_time = post.get('business_license_time','')
		tax_registration_certificate = json.loads(post.get('tax_registration_certificate',''))[0]['path']
		tax_registration_certificate_time = post.get('tax_registration_certificate_time','')
		organization_code_certificate = json.loads(post.get('organization_code_certificate',''))[0]['path']
		organization_code_certificate_time = post.get('organization_code_certificate_time','')
		account_opening_license = json.loads(post.get('account_opening_license',''))[0]['path']
		account_opening_license_time = post.get('account_opening_license_time','')
		
		try:
			business = models.Business.objects.filter(id=business_id).update(
				company_type = company_type,
				company_name = company_name,
				company_money = company_money,
				legal_representative = legal_representative,
				contacter = contacter,
				phone = phone,
				e_mail = e_mail,
				we_chat_and_qq = we_chat_and_qq,
				company_location = company_location,
				address = address,
				business_license = business_license,
				business_license_time = business_license_time,
				tax_registration_certificate = tax_registration_certificate,
				tax_registration_certificate_time = tax_registration_certificate_time,
				organization_code_certificate = organization_code_certificate,
				organization_code_certificate_time = organization_code_certificate_time,
				account_opening_license = account_opening_license,
				account_opening_license_time = account_opening_license_time,
				# product_catalog_ids = product_catalog_ids
			)
			new_business_info = models.Business.objects.get(id=business_id)
			#如果更换了企业类型，把客户编号也更改过来
			if (new_business_info.customer_number[:2]=='CJ' and new_business_info.company_type==2 ) or (new_business_info.customer_number[:2]=='DL' and new_business_info.company_type==1 ):
				old_customer_number = new_business_info.customer_number
				if new_business_info.company_type == models.DIRECT:
					new_customer_number = 'CJ'+ old_customer_number[2:]
				else:
					new_customer_number = 'DL'+ old_customer_number[2:]
				new_business_info.customer_number = new_customer_number
				new_business_info.save()
			response = create_response(200)
		except Exception,e:
			print e
			response = create_response(500)
			response.innerErrMsg = unicode_full_stack()

		return response.get_response()

class GetQualifications(resource.Resource):
	app = 'business'
	resource = 'get_qualifications'

	@login_required
	def api_get(request):
		business_id =  request.GET.get('business_id')
		catalog_ids = request.GET.get('catalog_ids').split(',')
		business_qualifications = []
		business = models.Business.objects.get(id=business_id)
		already_upload_catalog_ids = business.product_catalog_ids.split('_')
		already_upload_qualifications = models.BusinessQualification.objects.filter(business_id=business_id)
		all_qualifications = product_catalog_models.ProductCatalogQualification.objects.all()
		all_need_qualifications_catalog_ids = [str(all_qualification.catalog_id) for all_qualification in all_qualifications]
		qualification_id2name = dict((qualification.id,qualification.name) for qualification in all_qualifications)
		qualification_id2catalog_id = dict((qualification.id,qualification.catalog_id) for qualification in all_qualifications)
		
		for catalog_id in catalog_ids:
			#判断是否需要特殊资质
			if catalog_id in all_need_qualifications_catalog_ids:
				#根据现在所选择的商品类目，判断是否已经上传过特殊资质
				if catalog_id in already_upload_catalog_ids:
					#得到商家已经上传过特殊资质
					qualifications = all_qualifications.filter(catalog_id=catalog_id)
					qualifications_ids = [qualification.id for qualification in qualifications]
					already_upload_qualifications.filter(qualification_id__in=qualifications_ids)
					for already_upload_qualification in already_upload_qualifications:
						business_qualifications.append({
							'belong_catalog_id': qualification_id2catalog_id[already_upload_qualification.qualification_id],
							'qualification_id': already_upload_qualification.qualification_id,
							'qualification_name': qualification_id2name[already_upload_qualification.qualification_id],
							'img': [{'id':1,'path':already_upload_qualification.path}],
							'qualification_time': already_upload_qualification.qualification_time.strftime("%Y-%m-%d %H:%M")
						})
				else:
					qualifications = all_qualifications.filter(catalog_id=catalog_id)
					for qualification in qualifications:
						business_qualifications.append({
							'belong_catalog_id': qualification.catalog_id,
							'qualification_id': '-1',
							'qualification_name': qualification.name,
							'img': [],
							'qualification_time': '到期时间'
						})
		data = {
			'rows': business_qualifications
		}
		response = create_response(200)
		response.data = data
		return response.get_response()