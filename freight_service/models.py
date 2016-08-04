# -*- coding: utf-8 -*-
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class UserHasFreight(models.Model):
	"""
	用户是否有运费
	"""
	user_id = models.IntegerField(default=-1) #用户id
	free_freight_money = models.DecimalField(max_digits=65, decimal_places=2, null=True)  #满消费金额免运费
	need_freight_money = models.DecimalField(max_digits=65, decimal_places=2, null=True)  #需要运费金额
	is_deleted = models.BooleanField(default=False) 

	class Meta(object):
		db_table = 'user_has_freight'


class UserHasFreightRelation(models.Model):
	"""
	用户是否有运费 和云上通的中间关系
	"""
	freight_id = models.IntegerField(default=0) #panda的id
	weapp_freight_id = models.IntegerField(default=0) #云上通的id
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'user_has_freight_relation'
