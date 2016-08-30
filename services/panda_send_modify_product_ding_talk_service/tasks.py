# -*- coding: utf-8 -*-

__author__ = 'hj'
import os
from django.conf import settings

from panda.celery import task

from util import ding_util
uuid = 199597313

@task(bind=True, time_limit=7200, max_retries=2)
def send_modify_product_ding_talk(self, message, product_id):
	result = ding_util.send_to_ding(message, uuid)

