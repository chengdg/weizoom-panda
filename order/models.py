# -*- coding: utf-8 -*-
__author__ = 'bert'

import copy
from datetime import datetime, timedelta
from django.db import models

ORDER_STATUS_NOT = 0  # 待支付：已下单，未付款
ORDER_STATUS_CANCEL = 1  # 已取消：取消订单(回退销量)
ORDER_STATUS_PAYED_SUCCESSED = 2  # 已支付：已下单，已付款，已不存此状态
ORDER_STATUS_PAYED_NOT_SHIP = 3  # 待发货：已付款，未发货
ORDER_STATUS_PAYED_SHIPED = 4  # 已发货：已付款，已发货
ORDER_STATUS_SUCCESSED = 5  # 已完成：自下单10日后自动置为已完成状态
ORDER_STATUS_REFUNDING = 6  # 退款中
ORDER_STATUS_REFUNDED = 7  # 退款完成(回退销量)
ORDER_STATUS_GROUP_REFUNDING = 8 #团购退款（没有退款完成按钮）
ORDER_STATUS_GROUP_REFUNDED = 9 #团购退款完成

# 权重小的优先
ORDER_STATUS2DELIVERY_ITEM_WEIGHT = {
	ORDER_STATUS_NOT: 1,
	ORDER_STATUS_PAYED_NOT_SHIP: 2,
	ORDER_STATUS_PAYED_SHIPED: 3,
	ORDER_STATUS_REFUNDING: 4,
	ORDER_STATUS_SUCCESSED: 5,
	ORDER_STATUS_REFUNDED:6,
	ORDER_STATUS_CANCEL: 7
}

# Create your models here.
ORDER_BILL_TYPE_NONE = 0  # 无发票
ORDER_BILL_TYPE_PERSONAL = 1  # 个人发票
ORDER_BILL_TYPE_COMPANY = 2  # 公司发票
STATUS2TEXT = {
	ORDER_STATUS_NOT: u'待支付',
	ORDER_STATUS_CANCEL: u'已取消',
	ORDER_STATUS_PAYED_SUCCESSED: u'已支付',
	ORDER_STATUS_PAYED_NOT_SHIP: u'待发货',
	ORDER_STATUS_PAYED_SHIPED: u'已发货',
	ORDER_STATUS_SUCCESSED: u'已完成',
	ORDER_STATUS_REFUNDING: u'退款中',
	ORDER_STATUS_REFUNDED: u'退款成功',
	ORDER_STATUS_GROUP_REFUNDING: u'退款中',
	ORDER_STATUS_GROUP_REFUNDED: u'退款成功',
}

AUDIT_STATUS2TEXT = {
	ORDER_STATUS_REFUNDING: u'退款中',
	ORDER_STATUS_REFUNDED: u'退款成功',
	ORDER_STATUS_GROUP_REFUNDING: u'团购退款',
}

REFUND_STATUS2TEXT = {
	ORDER_STATUS_REFUNDING: u'退款中',
	ORDER_STATUS_REFUNDED: u'退款成功'
}

ORDERSTATUS2TEXT = STATUS2TEXT

ORDERSTATUS2MOBILETEXT = copy.copy(ORDERSTATUS2TEXT)
ORDERSTATUS2MOBILETEXT[ORDER_STATUS_PAYED_SHIPED] = u'待收货'

class Order(models.Model):
	"""
	订单

	表名: mall_order
	"""
	order_id = models.CharField(max_length=100)  # 订单号
	webapp_user_id = models.IntegerField()  # WebApp用户的id 商城会员id 用于统计复购等信息
	webapp_id = models.CharField(max_length=20, verbose_name='店铺ID')  # webapp,订单成交的店铺id
	buyer_name = models.CharField(max_length=100)  # 购买人姓名
	buyer_tel = models.CharField(max_length=100)  # 购买人电话
	ship_name = models.CharField(max_length=100)  # 收货人姓名
	ship_tel = models.CharField(max_length=100)  # 收货人电话
	ship_address = models.CharField(max_length=200)  # 收货人地址
	area = models.CharField(max_length=100)
	status = models.IntegerField(default=ORDER_STATUS_NOT)  # 订单状态
	remark = models.TextField()  # 备注
	supplier_remark = models.TextField()  # 供应商备注
	product_price = models.FloatField(default=0.0)  # 商品金额
	postage = models.FloatField(default=0.0)  # 运费
	final_price = models.FloatField(default=0.0)
	pay_interface_type = models.IntegerField(default=-1)  # 支付方式
	express_company_name = models.CharField(max_length=50, default='')  # 物流公司名称
	express_number = models.CharField(max_length=100)  # 快递单号
	leader_name = models.CharField(max_length=256)  # 订单负责人
	customer_message = models.CharField(max_length=1024)  # 商家留言
	payment_time = models.DateTimeField(blank=True)  # 订单支付时间
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
	reason = models.CharField(max_length=256, default='')  # 取消订单原因
	# origin_order_id=-1表示有子订单，>0表示有父母订单，=0为默认数据
	supplier = models.IntegerField(default=0) # 订单供货商，用于微众精选拆单
	#is_100 = models.BooleanField(default=True) # 是否"coupon_id":"是快递100能够查询的快递(是否使用快递查询服务,在订单点击发货时来更新is_100的状态)
	total_purchase_price = models.FloatField(default=0)  # 总订单采购价格
	# refund_money = models.FloatField(default=-1)     # 订单的退款金额

	class Meta(object):
		db_table = 'mall_order'
		verbose_name = '订单'
		verbose_name_plural = '订单'


class OrderHasProduct(models.Model):
	"""
	<order, product>关联
	"""
	order = models.ForeignKey(Order)
	product_id = models.IntegerField()##商品id（云商通）panda变动频繁以实际下单是信息为准
	product_name = models.CharField(max_length=256)  # 商品名
	product_model_name = models.CharField(max_length=256, default='')  # 商品规格名
	price = models.FloatField()  # 商品单价
	total_price = models.FloatField()  # 订单价格
	number = models.IntegerField(default=1)  # 商品数量
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
	# promotion_id = models.IntegerField(default=0)  # 促销信息id
	# promotion_money = models.FloatField(default=0.0)  # 促销抵扣金额
	# grade_discounted_money = models.FloatField(default=0.0)  # 折扣金额
	purchase_price = models.FloatField(default=0)  # 采购单价
	original_price = models.FloatField(default=0)  # 商品原价 add by bert 请勿随意赋值
	thumbnails_url = models.CharField(max_length=256, default='') # 商品缩略图

	class Meta(object):
		db_table = 'mall_order_has_product'