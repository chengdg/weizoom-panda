# -*- coding: utf-8 -*-
__author__ = 'lihanyi'

import json
from datetime import datetime
import os
import random
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.conf import settings
from django.contrib.auth.models import User
from core import resource
from core import paginator
from util import db_util

from core.jsonresponse import create_response
from resource import models as resource_models
import models
import nav
from product_catalog import models as product_catalog_models

FIRST_NAV = 'business'
SECOND_NAV = 'business'
COUNT_PER_PAGE = 10

filter2field ={
}

class BusinessApply(resource.Resource):
	app = 'business'
	resource = 'customer_apply'
	#用户申请入驻
	def get(request):
		c = RequestContext(request, {
		})
		return render_to_response('business/business_apply_page.html', c)

	def api_get(request):
		#获得入驻类目数据
		first_catalog = []
		second_catalog = []
		second_catalog_ids = []
		catalog_qualifications = {}
		for catalog in product_catalog_models.ProductCatalog.objects.filter(level=1).order_by('-created_at'):
			first_catalog.append(catalog.name)
			this_second_catalog = []
			this_second_catalog_id = []
			second_catalogs = product_catalog_models.ProductCatalog.objects.filter(father_id=catalog.id)
			this_second_catalog = [catalog.name for catalog in second_catalogs]
			this_second_catalog_id = [catalog.id for catalog in second_catalogs]
			second_catalog.append(this_second_catalog)
			second_catalog_ids.append(this_second_catalog_id)
			
			#获得二级类目的所属特殊资质
			for catalog in second_catalogs:
				this_catalog_qualifications = []
				all_catalog_qualifications = product_catalog_models.ProductCatalogQualification.objects.filter(catalog_id=catalog.id)
				for catalog_qualification in all_catalog_qualifications:
					this_catalog_qualifications.append({
						'qualification_id': catalog_qualification.id,
						'qualification_name': catalog_qualification.name
					})
				catalog_qualifications[catalog.id] = this_catalog_qualifications
		data = {
			'first_catalog': first_catalog,
			'second_catalog': second_catalog,
			'second_catalog_ids': second_catalog_ids,
			'catalog_qualifications': catalog_qualifications
		}
		response = create_response(200)
		response.data = data
		return response.get_response()

	def api_post(request):
		post = request.POST
		company_type = models.DIRECT if post.get('company_type')=='direct' else models.AGENCY
		company_name = post.get('company_name','')
		company_money = float(post.get('company_money')) if post.get('company_money')!='' else 0
		legal_representative = post.get('legal_representative','')
		contacter = post.get('contacter','')
		phone = post.get('phone','')
		e_mail = post.get('e_mail','')
		we_chat_and_qq = post.get('we_chat_and_qq','')
		company_location = post.get('company_location','')
		address = post.get('address','')

		data_page_2 = json.loads(post.get('data_page_2'),'')
		data_page_3 = json.loads(post.get('data_page_3'),'')

		business_license = data_page_2['business_license']
		business_license_time = data_page_2['business_license_time'] if data_page_2['business_license_time'] !='' else None
		tax_registration_certificate = data_page_2['tax_registration_certificate']
		tax_registration_certificate_time = data_page_2['tax_registration_certificate_time'] if data_page_2['tax_registration_certificate_time'] !='' else None
		organization_code_certificate = data_page_2['organization_code_certificate']
		organization_code_certificate_time = data_page_2['organization_code_certificate_time'] if data_page_2['organization_code_certificate_time'] !='' else None
		account_opening_license = data_page_2['account_opening_license']
		account_opening_license_time = data_page_2['account_opening_license_time'] if data_page_2['account_opening_license_time'] !='' else None
		product_catalog_ids = '_'.join(data_page_3['selectedSortIds'])
		upload_qualifications = data_page_3['uploadQualifications'] 

		business = models.Business.objects.create(
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
			product_catalog_ids = product_catalog_ids
		)
		if company_type == models.DIRECT:
			customer_number = 'CJ'+ datetime.now().strftime("%Y") + "%06d" % business.id
		else:
			customer_number = 'DL'+ datetime.now().strftime("%Y") + "%06d" % business.id
		business.customer_number = customer_number
		business.save()
		#创建特殊资质，把提交的资质信息与商家关联起来
		for upload_qualification in upload_qualifications:
			business_qualification = models.BusinessQualification.objects.create(
				business_id = business.id,
				qualification_id = upload_qualification['qualification_id'],
				path = upload_qualification['path'],
				qualification_time = upload_qualification['time'] if upload_qualification['time'] !='' else None
			)
		response = create_response(200)
		return response.get_response()

class Business(resource.Resource):
	app = 'business'
	resource = 'manager'
	
	#管理员管理入驻申请
	@login_required
	def get(request):
		"""
		显示入驻申请列表
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV
		})
		
		return render_to_response('business/business_manager.html', c)

	@login_required
	def api_get(request):
		cur_page = request.GET.get('page', 1)
		businesses = models.Business.objects.all().order_by('-created_at')
		catalog_id2name = dict((str(catalog.id),catalog.name) for catalog in product_catalog_models.ProductCatalog.objects.filter(level=2))
		filters = dict([(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET if key.startswith('__f-')])
		customer_number = filters.get('customer_number','')
		company_name = filters.get('company_name','')
		product_catalog = filters.get('product_catalog','')
		company_type = filters.get('company_type','')
		phone = filters.get('phone','')
		status = filters.get('status','')
		company_location = filters.get('company_location','')
		if customer_number:
			businesses = businesses.filter(customer_number__icontains=customer_number)
		if company_name:
			businesses = businesses.filter(company_name__icontains=company_name)
		if product_catalog:
			filter_catalogs = product_catalog_models.ProductCatalog.objects.filter(level=2,name__icontains=product_catalog)
			filter_catalogs_ids = [str(filter_catalog.id) for filter_catalog in filter_catalogs]
			filter_business_ids = []
			for business in businesses:
				#得到商家的经营类目
				catalog_ids = business.product_catalog_ids.split('_')
				for filter_catalogs_id in filter_catalogs_ids:
					#判断是否类目是在筛选条件之内
					if filter_catalogs_id in catalog_ids:
						filter_business_ids.append(business.id)
			businesses = businesses.filter(id__in=filter_business_ids)
		if company_type:
			businesses = businesses.filter(company_type=int(company_type))
		if phone:
			businesses = businesses.filter(phone__icontains=phone)
		if status:
			businesses = businesses.filter(status=int(status))
		if company_location:
			businesses = businesses.filter(company_location__icontains=company_location)

		rows = []
		for business in businesses:
			catalog_name = []
			product_catalog_ids = business.product_catalog_ids.split('_')
			for product_catalog in product_catalog_ids:
				catalog_name.append(catalog_id2name[product_catalog])
			catalog_name = ';'.join(catalog_name)
			rows.append({
				'id': business.id,
				'customer_number': business.customer_number,
				'company_name': business.company_name,
				'company_location': business.company_location,
				'company_type': models.TYPE2NAME[business.company_type],
				'product_catalogs': catalog_name,
				'contacter': business.contacter,
				'phone': business.phone,
				'status': models.STATUS2NAME[business.status] if business.status!=3 else models.STATUS2NAME[business.status]+'('+business.reason+')'
			})
		pageinfo, businesses = paginator.paginate(businesses, cur_page, COUNT_PER_PAGE, query_string=request.META['QUERY_STRING'])
		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}
		response = create_response(200)
		response.data = data
		return response.get_response()

	@login_required
	def api_post(request):
		#审核通过
		business_id = request.POST.get('id','')
		try:
			models.Business.objects.filter(id = business_id).update(
				status = models.PASSED
			)
			response = create_response(200)
			return response.get_response()
		except:
			response = create_response(500)
			response.errMsg = u'该记录不存在，请检查'
			return response.get_response()

	@login_required
	def api_put(request):
		#驳回
		business_id = request.POST.get('id','')
		reason = request.POST.get('reason','')
		try:
			models.Business.objects.filter(id = business_id).update(
				status = models.UNPASSED,
				reason = reason
			)
			response = create_response(200)
			return response.get_response()
		except:
			response = create_response(500)
			response.errMsg = u'该记录不存在，请检查'
			return response.get_response()

	@login_required
	def api_delete(request):
		business_id = request.POST.get('id','')
		try:
			models.Business.objects.filter(id = business_id).delete()
			response = create_response(200)
			return response.get_response()
		except:
			response = create_response(500)
			response.errMsg = u'该记录不存在，请检查'
			return response.get_response()

class BusinessImage(resource.Resource):
    """
    图片
    """
    app = 'business'
    resource = 'upload_image'

    def __get_file_name(file_name):
        """
        基于上传的文件的文件名file_name，生成一个server端唯一的文件名
        """
        pos = file_name.rfind('.')
        if pos == -1:
            suffix = ''
        else:
            suffix = file_name[pos:]
            
        return '%s_%d%s' % (str(time.time()).replace('.', '0'), random.randint(1, 1000), suffix)
    
    def post(request):
        file = request.FILES.get('image', None)

        #读取二进制内容
        content = []
        if file:
            for chunk in file.chunks():
                content.append(chunk)

        #获取存储图片的目录和文件信息
        file_name = BusinessImage.__get_file_name(file.name)
        store_dir = time.strftime('%Y%m%d')
        dir_path = os.path.join(settings.UPLOAD_DIR, store_dir)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_path = os.path.join(dir_path, file_name)

        #写图片文件内容
        dst_file = open(file_path, 'wb')
        print >> dst_file, ''.join(content)
        dst_file.close()

        #保存图片信息到mysql中
        image_path = '/static/upload/%s/%s' % (store_dir, file_name)
        image = resource_models.Image.objects.create(
            user = User.objects.filter(is_staff=1).first(),
            path = image_path
        )

        response = create_response(200)
        response.data = {
            'id': image.id,
            'path': image_path
        }
        return response.get_response()
