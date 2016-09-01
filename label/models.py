# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class LabelProperty(models.Model):
	"""
	LabelProperty:标签分类属性
	"""
	user_id = models.IntegerField(default=0)
	name = models.CharField(max_length=256,null=True)  # 标签分类名
	is_deleted = models.BooleanField(default=False)  # 是否删除
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

	class Meta(object):
		db_table = 'label_property'
		verbose_name = '标签分类属性'
		verbose_name_plural = '标签分类属性'


class LabelPropertyValue(models.Model):
	"""
	LabelPropertyValue:标签属性值
	"""
	property_id = models.IntegerField(default=0) #LabelProperty id
	name = models.CharField(max_length=256)  # 规格属性值
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

	class Meta(object):
		db_table = 'label_property_value'
		verbose_name = '标签属性值'
		verbose_name_plural = '标签属性值'