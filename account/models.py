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
	(CUSTOMER, u'体验客户'),
	(AGENCY, u'代理'),
	(YUN_YING, u'运营')
)
ROLE2NAME = dict(ROLES)

#===============================================================================
# UserProfile ： 用户信息
#===============================================================================

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	name = models.CharField(max_length=32) #账号名称
	manager_id = models.IntegerField(default=0) #创建该用户的系统用户的id
	role = models.IntegerField(default=MANAGER,choices=ROLES) #角色
	company_name = models.CharField(max_length=32, default='') #公司名称
	company_type = models.CharField(max_length=1024, default='') #经营类目
	purchase_method = models.IntegerField(default=1) #采购方式
	points = models.FloatField(default=0) #零售价返点
	contacter = models.CharField(max_length=32, default='') #联系人
	phone = models.CharField(max_length=16, default='') #手机号
	valid_time_from = models.DateTimeField(null=True) #有效范围开始时间
	valid_time_to = models.DateTimeField(null=True) #有效范围结束时间
	note = models.CharField(max_length=1024, default='') #备注
	status = models.IntegerField(default=1) #账号状态 1开启中，0停用中
	is_active = models.BooleanField(default=True, verbose_name='用户是否有效') #是否删除
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

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
	supplier_id = models.IntegerField(default=0) # 供货商id
	store_name = models.CharField(max_length=1024, default='') #供货商名称

	class Meta(object):
		db_table = 'account_has_supplier'