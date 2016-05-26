# -*- coding: utf-8 -*-
import json
import time
import logging
from datetime import datetime, timedelta

from behave import *
import bdd_util

from outline import models as outline_models

__author__ = 'kuki'

def __get_type(type):
	if type:
		type2type_dic = {u"体验客户":1,u"代理商":2,u"运营":3}
		return type2type_dic[type]
	else:
		return 1
def __get_actions(status):
	"""
	根据账号状态
	返回对于操作列表
	"""
	actions_list = [u"编辑"]
	if status == 1:
		actions_list.append(u"关闭")
	elif status == 0:
		actions_list.append(u"开启")
	return actions_list

@when(u"{user}添加账号")
def step_impl(context, user):
	infos = json.loads(context.text)
	for info in infos:
		params = {
            'account_type': __get_type(info.get('account_type', '')),
            'name': info.get('account_name', ''),
			'username': info.get('login_account', ''),
            'password': info.get('password', ''),
            'note': info.get('ramarks', '')
        }
		response = context.client.put('/manager/api/account_create/', params)
		print(response)
		bdd_util.assert_api_call_success(response)

@then(u"{user}能获得账号管理列表")
def step_impl(context, user):
	expected = json.loads(context.text)
	response = context.client.get('/manager/api/account/')
	actual_response = json.loads(response.content)['data']['rows']
	actual = []
	for item in actual_response:
		tmp = {
			"account_name":item['name'],
			"login_account":item['username']
		}
		actions_array = __get_actions(item['status'])
		tmp["actions"] = actions_array
		actual.append(tmp)
	print("expected: {}".format(expected))
	print("actual_data: {}".format(actual))
	bdd_util.assert_list(expected, actual)