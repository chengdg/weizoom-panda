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
	manager_id = models.IntegerField(default=0) #创建该用户的系统用户的id
	role = models.IntegerField(default=CUSTOMER,choices=ROLES) #角色
	name = models.CharField(max_length=32) #账号名称
	is_active = models.BooleanField(default=True, verbose_name='用户是否有效')
	note = models.CharField(max_length=1024, default='') #备注

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