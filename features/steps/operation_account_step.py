# -*- coding: utf-8 -*-
__author__ = 'hj'
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

@then(u"{user}能获得所有商品列表")
def step_impl(context, user):
	expected = json.loads(context.text)
	response = context.client.get('/product/api/product_relation/')
	actual_response = json.loads(response.content)['data']['rows']
	actual = []
	for item in actual_response:
		tmp = {
			"name":item['product_name'],
			"sales":item['total_sales'],
			"account_name":item['customer_name'],
			"weapp_id": [{}]
		}
		actual.append(tmp)
	print("expected: {}".format(expected))
	print("actual_data: {}".format(actual))
	bdd_util.assert_list(expected, actual)