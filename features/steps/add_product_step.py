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
	context.products = json.loads(context.text)
	for product in context.products:
		stock_value = PRODUCT_STORE_TEXT2VALUE[product['stock_type']]
		product_info = {
			'product_name': product['name'],
			'promotion_title': product['promotion_name'],
			'product_price': product['price'],
			'clear_price': product['settlement_price'],
			'product_weight': product['weight'],
			'product_store': stock_value,
			'remark': product['introduction'],
		}
		response = context.client.put('/product/api/new_product/', product_info)
		bdd_util.assert_api_call_success(response)