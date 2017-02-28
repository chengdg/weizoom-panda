# -*- coding: utf-8 -*-

import os
import json
from hashlib import md5
from core.dateutil import get_current_time_in_millis

from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals
from django.conf import settings
from django.db.models import F

from core import dateutil

MANAGER = 0
CUSTOMER = 1
AGENCY = 2
YUN_YING = 3
ROLES = (
	(MANAGER, u'管理员'),
	(CUSTOMER, u'合作客户'),
	(AGENCY, u'代理商'),
	(YUN_YING, u'运营')
)
ROLE2NAME = dict(ROLES)

#账号状态
STATUS_STOPED = 0
STATUS_RUNNING = 1
STATUS_NOT_IN_VALID_TIME = 2

#采购方式
METHOD = (
	(1, u'固定底价'),
	(2, u'零售价返点'),
	(3, u'首月55分成'),
	(4, u'高佣直采')
)
METHOD2NAME = dict(METHOD)

# 结算账期  1【自然月】   2【15天】   3【自然周】
SETTLEMENT_PERIOD_MONTH = 1
SETTLEMENT_PERIOD_15TH_DAY = 2
SETTLEMENT_PERIOD_WEEK = 3
#===============================================================================
# UserProfile ： 用户信息
#===============================================================================

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	name = models.CharField(max_length=32) #账号名称
	manager_id = models.IntegerField(default=0) #创建该用户的系统用户的id
	role = models.IntegerField(default=CUSTOMER,choices=ROLES) #角色
	company_name = models.CharField(max_length=32, default='') #公司名称
	company_type = models.CharField(max_length=1024, default='') #经营类目(catalog表的id构成的list，例如[1,2])
	purchase_method = models.IntegerField(default=1) #采购方式
	points = models.FloatField(default=0) #零售价返点
	contacter = models.CharField(max_length=32, default='') #联系人
	phone = models.CharField(max_length=16, default='') #手机号
	valid_time_from = models.DateTimeField(null=True) #有效范围开始时间
	valid_time_to = models.DateTimeField(null=True) #有效范围结束时间
	note = models.CharField(max_length=1024, default='') #备注
	status = models.IntegerField(default=1) #账号状态 0停用中，1开启中，2不在有效期内
	is_active = models.BooleanField(default=True, verbose_name='用户是否有效') #是否删除
	created_at = models.DateTimeField(auto_now_add=True) #创建时间
	pre_sale_tel = models.CharField(max_length=32, default='') #售前电话
	after_sale_tel = models.CharField(max_length=32, default='') #售后电话
	max_product = models.IntegerField(default=10) #最多可创建商品
	customer_from = models.IntegerField(default=0) #客户来源 0 PANDA ，1 渠道
	product_count = models.IntegerField(default=0) #客户商品数量
	settlement_period = models.IntegerField(default=SETTLEMENT_PERIOD_MONTH) #结算账期  1【自然月】   2【15天】   3【自然周】
	corpid = models.CharField(max_length=100, default='') #corpid
	customer_service_tel = models.CharField(max_length=32, default='') #客服电话
	customer_service_qq_first = models.CharField(max_length=32, default='') #客服qq-1
	customer_service_qq_second = models.CharField(max_length=32, default='') #客服qq-2

	class Meta(object):
		db_table = 'account_user_profile'
		verbose_name = '用户配置'
		verbose_name_plural = '用户配置'

	@property
	def is_manager(self):
		return (self.user_id == self.manager_id) or (self.manager_id == 2) #2 is manager's id


def create_profile(instance, created, **kwargs):
	"""
	自动创建user profile
	"""
	if created:
		if instance.username == 'admin':
			return
		if UserProfile.objects.filter(user=instance).count() == 0:
			profile = UserProfile.objects.create(user = instance)
			

signals.post_save.connect(create_profile, sender=User, dispatch_uid = "account.create_profile")


class AccountHasSupplier(models.Model):
	user_id = models.IntegerField(default=0) #对应自营平台user_id
	account_id = models.IntegerField(default=0) #UserProfile id
	supplier_id = models.IntegerField(default=0) # 云上通的供货商id
	store_name = models.CharField(max_length=1024, default='') # y供货商名称

	class Meta(object):
		db_table = 'account_has_supplier'


class AccountHasGroupPoint(models.Model):
	"""
	采购方式:零售价返点(团购扣点)
	"""
	user_id = models.IntegerField(default=0) #user_id
	self_user_name = models.CharField(max_length=50, null=True) #自营商城名
	points = models.FloatField(default=0.0) #零售价返点
	group_points = models.FloatField(default=0.0) #团购扣点

	class Meta(object):
		db_table = 'account_has_group_point'

class AccountHasRebateProport(models.Model):
	"""
	采购方式:首月55分成
	"""
	user_id = models.IntegerField(default=0) #user_id
	valid_time_from = models.DateTimeField(null=True) #有效范围开始时间
	valid_time_to = models.DateTimeField(null=True) #有效范围结束时间
	order_money = models.DecimalField(max_digits=65, decimal_places=2, null=True) #销售额
	rebate_proport = models.FloatField(default=0.0) #扣点比例
	default_rebate_proport = models.FloatField(default=0.0) ##效果通最低让利
	order_money_condition = models.DecimalField(max_digits=65, decimal_places=2, null=True) #(添加条件)销售额
	rebate_proport_condition = models.FloatField(default=0.0) #(添加条件)返点比例
	default_rebate_proport_condition = models.FloatField(default=0.0) #(添加条件)基础扣点

	class Meta(object):
		db_table = 'account_has_rebate_proport'


class AccountRebateProportRelation(models.Model):
	"""
	采购方式:首月55分成(中间关系)
	"""
	panda_proport_id = models.IntegerField()
	weapp_divide_id = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'account_rebate_relation'
