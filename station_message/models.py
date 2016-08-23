# -*- coding: utf-8 -*-
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

#
# class Product(models.Model):
# 	"""
# 	商品信息
# 	"""
# 	owner = models.ForeignKey(User)
# 	product_name = models.CharField(max_length=50, null=True)  # 商品名称
# 	promotion_title = models.CharField(max_length=50, null=True)  # 促销标题
# 	product_price = models.DecimalField(max_digits=65, decimal_places=2, null=True)  # 商品价格 (元)
# 	clear_price = models.DecimalField(max_digits=65, decimal_places=2, null=True)  # 结算价 (元)
# 	product_weight = models.FloatField(default=0)  # 商品重量 (kg)
# 	product_store = models.IntegerField(default=0)  # 商品库存 默认-1{大于0: 有限 ,-1:无限}
# 	product_status = models.IntegerField(default=0)  # 商品状态 {0: 未上架 ,1:已上架}
# 	remark = models.TextField(null=True)  # 备注
# 	valid_time_from = models.DateTimeField(null=True)  # 有效范围开始时间
# 	valid_time_to = models.DateTimeField(null=True)  # 有效范围结束时间
# 	limit_clear_price = models.DecimalField(max_digits=65, decimal_places=2, null=True)  # 限时结算价 (元)
# 	has_limit_time = models.BooleanField(default=False)  # 限时结算价是否需要 有效范期
# 	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
# 	has_product_model = models.BooleanField(default=False)  # 是否是多规格商品
# 	catalog_id = models.IntegerField(default=0)  # 所属分类id(二级分类id)
# 	is_deleted = models.BooleanField(default=False)
#
# 	class Meta(object):
# 		db_table = 'product_product'

class Message(models.Model):
	"""
	消息
	"""
	# 发送者id
	send_id = models.IntegerField(default=0)
	# 接收者id(默认-1表示系统消息)
	receive_id = models.IntegerField(default=-1)
	# 消息的详细内容id
	text_id = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	is_deleted = models.BooleanField(default=False)

	class Meta(object):
		db_table = 'message'


class MessageText(models.Model):
	"""
	消息详情
	"""
	# title
	title = models.CharField(default='', max_length=100)
	text = models.TextField()
	message_id = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'message_text'


class MessageAttachment(models.Model):
	"""
	消息附件
	"""
	# 消息id Message
	message_id = models.IntegerField()
	document_id = models.IntegerField()

	class Meta(object):
		db_table = 'message_attachment'


MESSAGE_READED = 1

class UserMessage(models.Model):
	"""
	用户的message
	"""
	# 用户id
	user_id = models.IntegerField()
	# Message
	message_id = models.IntegerField()
	# 0 未读
	status = models.IntegerField(default=0)

	class Meta(object):
		db_table = 'user_message'
