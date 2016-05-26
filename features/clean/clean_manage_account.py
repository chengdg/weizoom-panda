# -*- coding: utf-8 -*-
import logging
from account import models as account_models
from django.contrib.auth.models import User

def clean():
	logging.info('clean database for account app')
	#清空用户信息
	user_ids = [u.user_id for u in account_models.UserProfile.objects.filter(manager_id__gt=0)]
	account_models.UserProfile.objects.filter(manager_id__gt=0).all().delete()
	User.objects.filter(id__in=user_ids).delete()