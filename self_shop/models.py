# -*- coding: utf-8 -*-
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class SelfShops(models.Model):
	"""
	自营平台
	"""
	self_shop_name = models.CharField(max_length=50, null=True)  #平台名称
	user_name = models.CharField(max_length=50, null=True)  #user_name
	remark = models.TextField(null=True) #备注
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'self_shop_self_shops'