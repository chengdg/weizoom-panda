# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class LabelGroup(models.Model):
	"""
	LabelGroup:标签分类
	"""
	user_id = models.IntegerField(default=0)
	name = models.CharField(max_length=256,null=True)  # 标签分类名
	is_deleted = models.BooleanField(default=False)  # 是否删除
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

	class Meta(object):
		db_table = 'label_group'
		verbose_name = '标签分类'
		verbose_name_plural = '标签分类'


class LabelGroupValue(models.Model):
	"""
	LabelGroupValue:标签分类值
	"""
	property_id = models.IntegerField(default=0) #LabelGroup id
	name = models.CharField(max_length=256)  # 规格属性值
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
	is_deleted = models.BooleanField(default=False)  # 是否删除

	class Meta(object):
		db_table = 'label_group_value'
		verbose_name = '标签分类值'
		verbose_name_plural = '标签分类值'