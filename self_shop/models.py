# -*- coding: utf-8 -*-
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
#注释代码 误删
# class SelfShopHasRebate(models.Model):
# 	"""
# 	自营平台是否有扣点基数
# 	"""
# 	self_shop_name = models.CharField(max_length=50, null=True)  #平台名称
# 	user_name = models.CharField(max_length=50, null=True)  #user_name
# 	rebate_value = models.FloatField(default=0, null=True)#扣点基数
# 	remark = models.TextField(null=True)#备注
# 	is_deleted = models.BooleanField(default=False) 

# 	class Meta(object):
# 		db_table = 'self_shop_has_rebate'