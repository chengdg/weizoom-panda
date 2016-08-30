# -*- coding: utf-8 -*-

__author__ = 'bert'
import os
from django.conf import settings

from panda.celery import task

from util import ding_util
uuid = 199597313

@task(bind=True, time_limit=7200, max_retries=2)
def send_sync_product_ding_talk(self, product_id):
	result = ding_util.send_to_ding("我在测试商品修改通知 不要怕",uuid)

