# -*- coding: utf-8 -*-
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class PostageConfig(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=256)  # 名称
	first_weight = models.FloatField(default=0.0)  # 首重
	first_weight_price = models.FloatField(default=0.0)  # 首重价格
	is_enable_added_weight = models.BooleanField(default=True)  # 是否启用续重机制
	added_weight = models.FloatField(max_length=255, default='0')  # 续重
	added_weight_price = models.FloatField(max_length=255, default='0')  # 续重价格
	# display_index = models.IntegerField(default=1, db_index=True)  # 显示的排序
	is_used = models.BooleanField(default=True)  # 是否启用
	# is_system_level_config = models.BooleanField(default=False)  # 是否是系统创建的不可修改的配置
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
	# v2
	# update_time = models.DateTimeField(auto_now=True)  # 更新时间
	is_enable_special_config = models.BooleanField(default=True)  # 是否启用续重机制
	is_enable_free_config = models.BooleanField(default=True)  # 是否启用包邮机制
	is_deleted = models.BooleanField(default=False) #是否删除
	# supplier_id = models.IntegerField(default=0) # 供货商的id

	class Meta(object):
		db_table = 'postage_config'
		verbose_name = '运费配置'
		verbose_name_plural = '运费配置'

	def get_special_configs(self):
		return SpecialPostageConfig.objects.filter(postage_config=self)

	def get_free_configs(self):
		return FreePostageConfig.objects.filter(postage_config=self)


#########################################################################
# SpecialPostageConfig：特殊地区运费配置
#########################################################################


class SpecialPostageConfig(models.Model):
	owner = models.ForeignKey(User)
	postage_config = models.ForeignKey(PostageConfig)
	first_weight_price = models.FloatField(default=0.0)  # 首重价格
	added_weight_price = models.FloatField(max_length=255)  # 续重价格
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
	# v2
	destination = models.CharField(max_length=512)  # 目的省份的id集合
	first_weight = models.FloatField(default=0.0)  # 首重
	added_weight = models.FloatField(default=0.0)  # 续重

	class Meta(object):
		db_table = 'postage_config_special'
		verbose_name = '运费特殊配置'
		verbose_name_plural = '运费特殊配置'


#########################################################################
# FreePostageConfig：特殊地区包邮配置
#########################################################################


class FreePostageConfig(models.Model):
	owner = models.ForeignKey(User)
	postage_config = models.ForeignKey(PostageConfig)
	destination = models.CharField(max_length=512)  # 目的省份的id集合
	condition = models.CharField(
		max_length=25,
		default='count')  # 免邮条件类型, 共有'count', 'money'两种
	condition_value = models.FloatField(max_length=25)  # 免邮条件值
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间

	class Meta(object):
		db_table = 'free_postage_config'
		verbose_name = '特殊地区包邮配置'
		verbose_name_plural = '特殊地区包邮配置'


class PostageConfigRelation(models.Model):
	"""

	"""
	postage_config_id = models.IntegerField()
	weapp_config_relation_id = models.IntegerField()

	class Meta(object):
		db_table = 'postage_config_relation'


class ShipperMessages(models.Model):
	"""	
	发货人信息
	"""
	owner = models.ForeignKey(User)
	shipper_name = models.CharField(max_length=50) #发货人
	tel_number = models.CharField(max_length=15) #手机号
	destination = models.CharField(max_length=512)  #发货地区 (目的省份的id集合 )
	address = models.CharField(max_length=256) #详细地址
	postcode = models.CharField(max_length=50) #邮政编码
	company_name = models.CharField(max_length=50) #单位名称
	remark = models.TextField(null=True) #备注
	is_active = models.BooleanField(default=False) #是否默认
	is_deleted = models.BooleanField(default=False) #是否删除

	class Meta(object):
		db_table = 'shipper_messages'


class ExpressBillAccounts(models.Model):
	"""	
	电子面单账号
	"""
	owner = models.ForeignKey(User)
	express_name = models.CharField(max_length=50) #快递公司
	customer_name = models.CharField(max_length=256) #CustomerName
	customer_pwd = models.CharField(max_length=256)  #CustomerPwd
	logistics_number = models.CharField(max_length=256) #物流月结号
	remark = models.TextField(null=True) #备注
	is_deleted = models.BooleanField(default=False) #是否删除

	class Meta(object):
		db_table = 'express_bill_accounts'