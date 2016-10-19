# -*- coding: utf-8 -*-
# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# 0不限制 1禁售 2仅售
NO_LIMIT = 0
FORBIDDEN_SALE_LIMIT = 1
ONLY_SALE_LIMIT = 2


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
	has_product_model = models.BooleanField(default=False) #是否是多规格商品
	catalog_id = models.IntegerField(default=0) #所属分类id(二级分类id)
	is_update = models.BooleanField(default=False) #是否更新
	is_refused = models.BooleanField(default=False) #是否驳回(入库驳回或修改驳回)
	refuse_reason = models.TextField(null=True) #驳回原因
	is_deleted = models.BooleanField(default=False)
	limit_zone_type = models.IntegerField(default=NO_LIMIT)
	limit_zone = models.IntegerField(default=0)  # 限制地区的模板id
	has_same_postage = models.BooleanField(default=True) #是否是统一运费{0:统一运费,1:默认模板运费}
	postage_money = models.DecimalField(max_digits=65, decimal_places=2, null=True) #统一运费金额
	postage_id = models.IntegerField(default=0)# 默认模板运费id

	class Meta(object):
		db_table = 'product_product'


class OldProduct(models.Model):
	"""
	已修改商品旧信息
	"""
	product_id = models.IntegerField(default=0)
	product_name = models.CharField(max_length=50, null=True)  #商品名称
	promotion_title = models.CharField(max_length=50, null=True)  #促销标题
	product_price = models.DecimalField(max_digits=65, decimal_places=2, null=True)  #商品价格 (元)
	clear_price = models.DecimalField(max_digits=65, decimal_places=2, null=True)  #结算价 (元)
	product_weight = models.FloatField(default=0)  #商品重量 (kg)
	product_store = models.IntegerField(default=0)  #商品库存 默认-1{大于0: 有限 ,-1:无限}
	remark = models.TextField(null=True)  #备注
	created_at = models.DateTimeField(auto_now_add=True)  #添加时间
	has_product_model = models.IntegerField(default=-1) #-1:没有更新这个属性,0:没有规格,1:有规格
	catalog_id = models.IntegerField(default=-1) #所属分类id(二级分类id)
	images = models.CharField(max_length=2048, null=True) #图片url
	product_model_ids = models.CharField(max_length=2048, null=True) #product_model id

	class Meta(object):
		db_table = 'old_product'


class ProductImage(models.Model):
	"""
	商品图片
	"""
	product = models.ForeignKey(Product)
	image_id = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'product_image'


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

class ProductSyncWeappAccount(models.Model):
    """
    商品被同步到了哪个平台（适配老逻辑）
    """
    product_id = models.IntegerField(default=0)
    self_user_name = models.CharField(max_length=50, null=True, help_text='对应平台的用户名')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        db_table = 'product_sync_weapp_account'


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

class SelfUsernameWeappAccount(models.Model):
    # 对应云上通的自营平台账户id(user_id)
    self_user_name = models.CharField(max_length=50, null=True)
    weapp_account_id = models.IntegerField(default=0)
    
    class Meta(object):
        db_table = 'self_username_weapp_account'


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
	price = models.FloatField(default=0.0)  # 商品价格 (商品售价)
	market_price = models.FloatField(default=0.0)  # 商品市场价格(商品结算价)
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
	property_id = models.IntegerField(default=0) #ProductModelProperty id
	property_value_id = models.IntegerField(default=0) #ProductModelPropertyValue id
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
	is_deleted = models.BooleanField(default=False)  # 是否已删除

	class Meta(object):
		db_table = 'product_model_has_property'


class ProductModelPropertyRelation(models.Model):
	"""
	商品模板和云上通商品模板关系
	"""
	model_property_id = models.IntegerField(help_text=u'本平台的模板id')
	weapp_property_id = models.IntegerField(help_text=u'云商通的模板id')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'product_model_property_relation'


class ProductModelPropertyValueRelation(models.Model):
	"""
	商品模板值和云上通商品模板值的对应关系(这个主要是当删除的时候更好的定位,否则无法定位)
	"""
	property_value_id = models.IntegerField()
	weapp_property_value_id = models.IntegerField()

	class Meta(object):
		db_table = 'product_model_property_value_relation'


class ProductHasLabel(models.Model):
	"""
	商品是否关联标签属性
	"""
	product_id = models.IntegerField(default=-1) # 商品id
	property_id = models.IntegerField(default=-1) # 标签分类id
	label_ids = models.CharField(max_length=1024, default='') # 标签属性值id 多个用,隔开 1,2,3

	class Meta(object):
		db_table = 'product_has_label'


class City(models.Model):
	name = models.CharField(max_length=50)
	zip_code = models.CharField(max_length=50)
	province_id = models.IntegerField(db_index=True)

	class Meta(object):
		db_table = 'city'
		verbose_name = '城市列表'
		verbose_name_plural = '城市列表'

class Province(models.Model):
	name = models.CharField(max_length=50)

	class Meta(object):
		db_table = 'province'
		verbose_name = '省份列表'
		verbose_name_plural = '省份列表'


class ProductRevokeLogs(models.Model):
	"""
	商品撤回(下架)日志
	"""
	product_id = models.IntegerField(default=-1) # 商品id
	revoke_reasons = models.CharField(max_length=1024, default='') #撤回原因
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'product_revoke_logs'


class ProductRejectLogs(models.Model):
	"""
	商品驳回日志（待入库状态被驳回）
	"""
	product_id = models.IntegerField(default=-1) # 商品id
	reject_reasons = models.CharField(max_length=1024, default='') #驳回原因
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'product_reject_logs'
