# -*- coding: utf-8 -*-
from django.db import models

DIRECT = 1
AGENCY = 2
TYPE = (
	(DIRECT, u'厂家直销'),
	(AGENCY, u'代理/贸易/分销')
)
TYPE2NAME = dict(TYPE)

REVIEW = 1
PASSED = 2
UNPASSED = 3
STATUS = (
	(REVIEW, u'待审核'),
	(PASSED, u'审核通过'),
	(UNPASSED, u'已驳回')
)
STATUS2NAME = dict(STATUS)

#===============================================================================
# Business ： 商家入驻
#===============================================================================
class Business(models.Model):
	customer_number = models.CharField(max_length=20, default='') #客户编号两位字母（厂家为CJ，代理/贸易/分销为DL）+年份四位数+6位数字（000001-999999）
	company_type = models.IntegerField(default=AGENCY,choices=TYPE) #企业类型
	company_name = models.CharField(max_length=32, default='') #公司名称
	company_money = models.FloatField(default=0) #注册资本
	legal_representative = models.CharField(max_length=32, default='') #法人代表
	contacter = models.CharField(max_length=32, default='') #联系人
	phone = models.CharField(max_length=32, default='') #手机号
	e_mail = models.CharField(max_length=32, default='') #E-mail
	we_chat_and_qq = models.CharField(max_length=32, default='') #微信/qq
	company_location = models.CharField(max_length=32, default='') #公司所在地
	address = models.CharField(max_length=32, default='') #详细地址
	business_license = models.CharField(max_length=1024, default='') #营业执照url
	business_license_time = models.DateTimeField(null=True)  #营业执照有效期
	tax_registration_certificate = models.CharField(max_length=1024, default='') #税务登记证url
	tax_registration_certificate_time = models.DateTimeField(null=True)  #税务登记证有效期
	organization_code_certificate = models.CharField(max_length=1024, default='') #组织机构代码证url
	organization_code_certificate_time = models.DateTimeField(null=True)  #组织机构代码证有效期
	account_opening_license = models.CharField(max_length=1024, default='') #开户许可证url
	account_opening_license_time = models.DateTimeField(null=True)  #开户许可证有效期
	product_catalog_ids = models.CharField(max_length=1024, default='') #入驻类目【以下划线分割】
	status = models.IntegerField(default=REVIEW,choices=STATUS) #状态
	reason = models.CharField(max_length=1024, default='') #驳回原因
	created_at = models.DateTimeField(auto_now_add=True) #创建日期

	class Meta(object):
		db_table = 'business_business'

#===============================================================================
# BusinessQualification ： 入驻商家特殊资质
#===============================================================================
class BusinessQualification(models.Model):
	business_id = models.IntegerField(default=0) #商家business_id
	qualification_id = models.IntegerField(default=0) #特殊资质id
	path = models.CharField(max_length=1024, default='') #特殊资质url
	qualification_time = models.DateTimeField(null=True)  #特殊资质有效期
	created_at = models.DateTimeField(auto_now_add=True) #创建日期

	class Meta(object):
		db_table = 'business_business_qualification'