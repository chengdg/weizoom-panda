# -*- coding: utf-8 -*-
from django.db import models


class ProductLimitZoneTemplate(models.Model):
	"""
	模板
	"""
	name = models.CharField(max_length=48, default='')
	created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
	owner_id = models.IntegerField(default=0)
	is_deleted = models.BooleanField(default=False)

	class Meta(object):
		db_table = 'product_limit_zone_template'


class ProductLimitZoneTemplateRelation(models.Model):
	template_id = models.IntegerField()
	weapp_template_id = models.IntegerField()

	class Meta(object):
		db_table = 'product_limit_zone_template_relation'


class LimitTemplateHasZone(models.Model):
	"""
	模板所保函的地区
	"""
	template_id = models.IntegerField()
	province = models.IntegerField(null=False)
	city = models.IntegerField(null=True)

	class Meta(object):
		db_table = 'template_has_zone'
