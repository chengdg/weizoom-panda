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
		weapp = []
		if item['relations']:
			relations = json.loads(item['relations'])
			for relation in relations:
				weapp_relation = {}
				weapp_name = relation['self_first_name']
				weapp_id = '%s'%relation['weapp_product_id']
				weapp_relation[weapp_name] = weapp_id
				weapp.append(weapp_relation)

		tmp = {
			"name":item['product_name'],
			"sales":item['total_sales'],
			"account_name":item['customer_name'],
			"weapp_id": weapp
		}
		actual.append(tmp)
	print("expected: {}".format(expected))
	print("actual_data: {}".format(actual))
	bdd_util.assert_list(expected, actual)

@When(u"{user}绑定商品关联的云商通商品")
def step_impl(context, user):
	products = json.loads(context.text)
	for product in products:
		weapps = product['weapp_id']
		if weapps:
			product_name = product['name']
			product = product_models.Product.objects.get(product_name=product_name)
			product_info = {
				'product_id': product.id,
				'weapps': json.dumps(weapps)
			}
			response = context.client.put('/product/api/relation_step/', product_info)
			bdd_util.assert_api_call_success(response)

@When(u"{user}修改商品关联的云商通商品")
def step_impl(context, user):
	products = json.loads(context.text)
	for product in products:
		weapps = product['weapp_id']
		product_name = product['name']
		product = product_models.Product.objects.get(product_name=product_name)
		if len(weapps)>0:
			product_info = {
				'product_id': product.id,
				'weapps': json.dumps(weapps)
			}
			response = context.client.put('/product/api/relation_step/', product_info)
			bdd_util.assert_api_call_success(response)
		else:
			product_info = {
				'product_id': product.id,
				'weapps': ''
			}
			response = context.client.put('/product/api/relation_step/', product_info)
			bdd_util.assert_api_call_success(response)