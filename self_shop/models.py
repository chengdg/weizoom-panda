# -*- coding: utf-8 -*-
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class SelfShops(models.Model):
	"""
	自营平台
	"""
	self_shop_name = models.CharField(max_length=50, null=True)  #平台名称
	weapp_user_id = models.CharField(max_length=50, null=True)  #weapp_user_id,历史记录存的是【weizoom_****】字符串
	settlement_type = models.IntegerField(default=1) #结算类型
	corp_account = models.IntegerField(default=1) #收款账户
	split_atio = models.FloatField(default=0) #扣点比例 /分成比例/同时批量加价
	risk_money = models.FloatField(default=0) #风险金额
	remark = models.TextField(null=True) #备注
	is_synced = models.BooleanField(default=False) #是否已同步过
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'self_shop_self_shops'