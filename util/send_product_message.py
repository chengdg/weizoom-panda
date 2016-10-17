# -*- coding: utf-8 -*-

from bdem import msgutil

from panda.settings import PRODUCT_TOPIC_NAME
from panda.settings import PRODUCT_MSG_NAME

from product import models
from self_shop import models as self_shop_models
from product_catalog import models as catalog_models
from account.models import UserProfile


def send_add_product_message(product=None, user_id=None, image_paths=None):
	"""
	客户添加商品消息
	"""
	data = organize_product_message_info(product=product, user_id=user_id, image_paths=image_paths)

	msgutil.send_message(PRODUCT_TOPIC_NAME, PRODUCT_MSG_NAME, data)


def send_sync_product_message(product=None, user_id=None, image_paths=None):
	"""
	首次同步商品信息
	"""
	data = organize_product_message_info(product=product, user_id=user_id, image_paths=image_paths)

	msgutil.send_message(PRODUCT_TOPIC_NAME, PRODUCT_MSG_NAME, data)


def send_sync_weapp_account_change(product_id=None):
	"""
	同步不同平台信息(如果取消同步了,也需要同步状态信息)
	"""
	data = {
		'product_id': product_id,
		'show_list': product_show_list(product_id=product_id),
		'push_status': get_product_status(product_id=product_id)
	}
	msgutil.send_message(PRODUCT_TOPIC_NAME, PRODUCT_MSG_NAME, data)


def send_sync_update_product_message(product=None, user_id=None, image_paths=None):
	"""
	运营同步更新商品信息的时候发送消息
	"""
	data = organize_product_message_info(product=product, user_id=user_id, image_paths=image_paths)
	msgutil.send_message(PRODUCT_TOPIC_NAME, PRODUCT_MSG_NAME, data)


def organize_product_message_info(product=None, user_id=None, image_paths=None):
	"""
	组织商品信息
	"""
	second_catagory = catalog_models.ProductCatalog.objects.filter(id=product.catalog_id).last()
	father_catagory = None
	if second_catagory:
		father_catagory = catalog_models.ProductCatalog.objects.filter(id=second_catagory.father_id).last()
	# 商品规格信息
	if not product.has_product_model:
		price_info = 'standard %s' % str(product.product_price)
		product_price = str(product.product_price)
	else:
		# 多规格
		price_info = []
		model_infos = models.ProductModel.objects.filter(product_id=product.id,
														 is_deleted=False,
														 )
		for info in model_infos:
			temp_price = info.price
			names = info.name.split('_')
			model_property_value_ids = [name.split(':')[-1] for name in names]
			model_property_value = models.ProductModelPropertyValue.objects.filter(id__in=model_property_value_ids)
			model_name = ' '.join([value.name for value in model_property_value])
			price_info.append(model_name + ' ' + str(temp_price))
		price_info = ';'.join(price_info)

		model_prices = sorted([model_info.price for model_info in model_infos])
		product_price = '0'
		if model_prices:
			if len(model_prices) > 1:
				product_price = str(model_prices[0]) + '~' + str(model_prices[-1])
			else:
				product_price = str(model_prices[0])
		# print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.'
		# print price_info
		# print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.'
	push_status = get_product_status(product_id=product.id)
	# 在哪个平台显示该商品
	show_list = product_show_list(product.id)
	# 构造参数
	product_message = {
		'product_id': product.id,
		'product_name': product.product_name,
		'customer_name': UserProfile.objects.filter(user_id=user_id)[0].company_name,
		'product_image': image_paths,
		'category': '' if not second_catagory or not father_catagory
						else '-'.join([father_catagory.name, second_catagory.name]),
		'price': product_price,
		'price_info': price_info,  # 规格/价格
		'push_status': push_status,
		# 'first_sale_time': '',  # 首次上架时间
		'show_list': show_list,
		# 'sales_revenue': '0',  # 累计销量
		# 'buyer_count': '0',  # 累计购买用户数量
		# 'order_area': "0",  # 商品销售区域覆盖数量
		# 'evaluation': '',
		# 'evaluation_list': []
	}
	return product_message


def product_show_list(product_id):
	"""
	商品在哪个平台显示(返回平台名称列表)
	"""

	self_user_names = [t.self_user_name
					   for t in models.ProductSyncWeappAccount.objects.filter(product_id=product_id)]
	if self_user_names:
		self_shop_names = [self_shop.self_shop_name
						   for self_shop in
						   self_shop_models.SelfShops.objects.filter(weapp_user_id__in=self_user_names)]

		show_list = u'、'.join(self_shop_names)
		return show_list
	else:
		return u''


def get_product_status(product_id=None):
	"""
	获取商品状态
	"""
	push_status = '待入库'
	product_relation = models.ProductHasRelationWeapp.objects.filter(product_id=product_id).last()
	account_count = models.ProductSyncWeappAccount.objects.filter(product_id=product_id)
	product_info = models.Product.objects.get(id=product_id)
	if product_relation:
		if account_count == 0:
			push_status = '已入库,已停售'
		else:
			push_status = '已入库,已同步'
	else:
		if product_info.is_refused: #未同步状态下的驳回算作入库驳回
			push_status = '入库驳回'
	return push_status
