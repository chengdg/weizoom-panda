# -*- coding: utf-8 -*-
from django.db import models

#===============================================================================
# ProductCatalog ： 商品分类
#===============================================================================
class ProductCatalog(models.Model):
	catalog_name = models.CharField(max_length=48, default='') #分类名称
	father_catalog = models.IntegerField(default=-1) #父级分类的id，-1为一级分类
	note = models.CharField(max_length=1024, default='') #备注
	created_at = models.DateTimeField(auto_now_add=True) #创建时间

	class Meta(object):
		db_table = 'product_catalog'