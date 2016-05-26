# -*- coding: utf-8 -*-
import json
import time
import logging
from datetime import datetime, timedelta

from behave import *
import bdd_util

from product import models as product_models

PRODUCT_STORE_TEXT2VALUE={
	u'无限': -1,
	u'有限': 0
}

@when(u"{user}添加商品")
def step_impl(context, user):
	products = json.loads(context.text)
	for product in products:
		stock_value = PRODUCT_STORE_TEXT2VALUE[product['stock_type']]
		product_info = {
			'product_name': product['name'],
			'promotion_title': product['promotion_name'],
			'product_price': product['price'],
			'clear_price': product['settlement_price'],
			'product_weight': product['weight'],
			'product_store': stock_value,
			'remark': product['introduction']
		}
		response = context.client.put('/product/api/new_product/', product_info)
		bdd_util.assert_api_call_success(response)

@then(u"{user}能获得商品列表")
def step_impl(context, user):
	expected = json.loads(context.text)
	response = context.client.get('/product/api/product_list/')
	actual_response = json.loads(response.content)['data']['rows']
	actual = []
	for item in actual_response:
		tmp = {
			"name":item['product_name'],
			"sales":item['sales'],
			"status":item['status']
		}
		tmp["actions"] = [u"编辑",u"彻底删除"]
		actual.append(tmp)
	print("expected: {}".format(expected))
	print("actual_data: {}".format(actual))
	bdd_util.assert_list(expected, actual)

@when(u"{user}删除商品'{product_name}'")
def step_impl(context, user, product_name):
	user_id = bdd_util.get_user_id_for(user)
	product = product_models.Product.objects.get(owner_id=user_id, product_name=product_name)
	response = context.client.delete('/product/api/new_product/', {'id': product.id})
	bdd_util.assert_api_call_success(response)