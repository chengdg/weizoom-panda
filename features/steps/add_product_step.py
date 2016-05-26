# -*- coding: utf-8 -*-
import json
import time
import logging
from datetime import datetime, timedelta

from behave import *
import bdd_util

from outline import models as outline_models

@when(u"{user}添加商品")
def step_impl(context, user):
	context.products = json.loads(context.text)
	for product in context.products:
		pass