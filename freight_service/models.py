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