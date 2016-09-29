# -*- coding: utf-8 -*-

__author__ = 'hj'
import os
from django.conf import settings

from panda.celery import task

from util import send_product_message
	
@task(bind=True, time_limit=7200, max_retries=2)
def send_customer_product_messages(self, product_message, product_id):
	result = send_product_message.send_product_message(product_message, None)


