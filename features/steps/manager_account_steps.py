# -*- coding: utf-8 -*-
import json
import time
import logging
from datetime import datetime, timedelta

from behave import *
from features import bdd_util

from outline import models as outline_models

__author__ = 'kuki'

# @when(u"{user}添加商品")
def step_impl(context, user):
	infos = json.loads(context.text)
	# owner_id = bdd_util.get_user_id_for(user)
	for info in infos:
		params = {
            'account_type': info.get('name', ''),
            'detail': info.get('detail', ''),
            'share_pic': info.get('share_pic', ''),
            'remark': info.get('remark', '')
        }