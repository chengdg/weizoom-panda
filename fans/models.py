# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class Fans(models.Model):
	weibo_id = models.CharField(max_length=24, default='') #粉丝id
	name = models.CharField(max_length=2048, default='') #粉丝名称
	fans_url = models.CharField(max_length=2048, default='') #粉丝头像
	male = models.BooleanField(default=True) #性别,1-男:0-女
	purchasing_index = models.FloatField(default=0) #购买指数
	spread_index = models.FloatField(default=0) #传播指数
	created_at = models.DateTimeField(auto_now_add=True) #创建日期

	class Meta(object):
		db_table = 'fans_fans'

class UserHasFans(models.Model):
	user_id = models.IntegerField(default=0) #用户id
	fans_id = models.IntegerField(default=0) #粉丝id
	status = models.IntegerField(default=0) #投放状态
	related_order_id = models.CharField(max_length=1024, default='') #关联订单号
	pushed_date = models.DateTimeField() #投放日期

	class Meta(object):
		db_table = 'fans_user_has_fans'