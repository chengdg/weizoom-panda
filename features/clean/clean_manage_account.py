# -*- coding: utf-8 -*-
import logging
from account import models as account_models

def clean():
	logging.info('clean database for account app')
	#清空用户信息
	account_models.UserProfile.objects.filter(manager_id__gt=0).all().delete()
