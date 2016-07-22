# -*- coding: utf-8 -*-
# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
	"""
	商品信息
	"""
	owner = models.ForeignKey(User)
	product_name = models.CharField(max_length=50, null=True)  #商品名称
	promotion_title = models.CharField(max_length=50, null=True)  #促销标题
	product_price = models.DecimalField(max_digits=65, decimal_places=2, null=True)  #商品价格 (元)
	clear_price = models.DecimalField(max_digits=65, decimal_places=2, null=True)  #结算价 (元)
	product_weight = models.FloatField(default=0)  #商品重量 (kg)
	product_store = models.IntegerField(default=0)  #商品库存 默认-1{大于0: 有限 ,-1:无限}
	product_status = models.IntegerField(default=0)  #商品状态 {0: 未上架 ,1:已上架}
	remark = models.TextField(null=True)  #备注
	valid_time_from = models.DateTimeField(null=True)  #有效范围开始时间
	valid_time_to = models.DateTimeField(null=True)  #有效范围结束时间
	limit_clear_price = models.DecimalField(max_digits=65, decimal_places=2, null=True)  #限时结算价 (元)
	has_limit_time = models.BooleanField(default=False)  #限时结算价是否需要 有效范期
	created_at = models.DateTimeField(auto_now_add=True)  #添加时间

	class Meta(object):
		db_table = 'product_product'



class ProductImage(models.Model):
	"""
	商品图片
	"""
	product = models.ForeignKey(Product)
	image_id = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'product_image'


class ProductRelation(models.Model):
	"""
	自营商城名称
	"""
	self_user_name = models.CharField(max_length=50, null=True)
	self_first_name = models.CharField(max_length=50, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'product_relation'


class ProductHasRelationWeapp(models.Model):
	"""
	商品关联云商通ID
	"""
	product_id = models.IntegerField(default=0)
	self_user_name = models.CharField(max_length=50, null=True)
	weapp_product_id = models.CharField(max_length=50, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'product_has_relation_weapp'



PRODUCT_MODEL_PROPERTY_TYPE_TEXT = 0
PRODUCT_MODEL_PROPERTY_TYPE_IMAGE = 1

class ProductModelProperty(models.Model):
	"""
	ProductModelProperty：商品规格属性
	"""
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=256,null=True)  # 商品规格属性名
	type = models.IntegerField(default=PRODUCT_MODEL_PROPERTY_TYPE_TEXT)  # 属性类型
	is_deleted = models.BooleanField(default=False)  # 是否删除
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

	class Meta(object):
		db_table = 'product_model_property'
		verbose_name = '商品规格属性'
		verbose_name_plural = '商品规格属性'


class ProductModelPropertyValue(models.Model):
	"""
	ProductModelPropertyValue：商品规格属性值
	"""
	property_id = models.IntegerField(default=0) #ProductModelProperty id
	name = models.CharField(max_length=256)  # 规格属性值
	pic_url = models.CharField(max_length=1024)  # 商品图
	is_deleted = models.BooleanField(default=False)  # 是否已删除
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

	class Meta(object):
		db_table = 'product_model_property_value'
		verbose_name = '商品规格属性值'
		verbose_name_plural = '商品规格属性值'


#########################################################################
# ProductModel：商品规格
#########################################################################
class ProductModel(models.Model):
	owner = models.ForeignKey(User)
	product = models.ForeignKey(Product)
	name = models.CharField(max_length=255, db_index=True)  # 商品规格名
	is_standard = models.BooleanField(default=True)  # 是否是标准规格
	price = models.FloatField(default=0.0)  # 商品价格
	market_price = models.FloatField(default=0.0)  # 商品市场价格
	weight = models.FloatField(default=0.0)  # 重量
	# stock_type = models.IntegerField(
	# 	default=PRODUCT_STOCK_TYPE_UNLIMIT)  # 0:无限 1:有限
	stocks = models.IntegerField(default=0)  # 有限：数量
	user_code = models.CharField(max_length=256, default='')  # 编码
	valid_time_from = models.DateTimeField(null=True)  #有效范围开始时间
	valid_time_to = models.DateTimeField(null=True)  #有效范围结束时间
	limit_clear_price = models.DecimalField(max_digits=65, decimal_places=2, null=True)  #限时结算价 (元)
	is_deleted = models.BooleanField(default=False)  # 是否已删除
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

	class Meta(object):
		db_table = 'product_model'
		verbose_name = '商品规格属性'
		verbose_name_plural = '商品规格属性'

	def __getitem__(self, name):
		return getattr(self, name, None)


#########################################################################
# ProductModelHasProperty: <商品规格，商品规格属性值>关系
#########################################################################
class ProductModelHasPropertyValue(models.Model):
	model = models.ForeignKey(ProductModel)
	property_id = models.IntegerField(default=0)
	property_value_id = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

	class Meta(object):
		db_table = 'product_model_has_property'