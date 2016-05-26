# -*- coding: utf-8 -*-
import json
import time
import logging
from datetime import datetime, timedelta

from behave import *
from features import bdd_util

from outline import models as outline_models

__author__ = 'kuki'

def __get_type(type):
	if type:
		type2type_dic = {u"体验客户":1,u"代理商":2,u"运营":3}
		return type2type_dic[type]
	else:
		return 1

@when(u"{user}添加账号")
def step_impl(context, user):
	infos = json.loads(context.text)
	# owner_id = bdd_util.get_user_id_for(user)
	for info in infos:
		params = {
            'account_type': __get_type(info.get('account_type', '')),
            'name': info.get('account_name', ''),
			'username': info.get('login_account', ''),
            'password': info.get('password', ''),
            'note': info.get('ramarks', '')
        }
		print('params!!!!!!!!!')
		print(params)
		response = context.client.put('/manager/api/account_create/', params)
		bdd_util.assert_api_call_success(response)