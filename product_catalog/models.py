# -*- coding: utf-8 -*-
from django.db import models


# ===============================================================================
# ProductCatalog ： 商品分类
# ===============================================================================
class ProductCatalog(models.Model):
	name = models.CharField(max_length=48, default='') #分类名称
	level = models.IntegerField(default=1) #默认为一级分类
	father_id = models.IntegerField(default=-1) #父级分类的id，-1为一级分类
	note = models.CharField(max_length=1024, default='') #备注
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

	class Meta(object):
		db_table = 'product_catalog'


class ProductCatalogRelation(models.Model):
	"""
	分类的中间关系（pana和weapp）
	"""

	catalog_id = models.IntegerField(help_text='panda这边的分类id')
	weapp_catalog_id = models.IntegerField(help_text='weapp这边的分类id')

	class Meta(object):
		db_table = 'product_catalog_relation'


# ===============================================================================
# ProductCatalogQualification ： 商品分类-特殊资质
# ===============================================================================
class ProductCatalogQualification(models.Model):
	catalog_id = models.IntegerField(default=-1) #所属二级分类
	name = models.CharField(max_length=48, default='') #资质名称
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

	class Meta(object):
		db_table = 'product_catalog_qualification'