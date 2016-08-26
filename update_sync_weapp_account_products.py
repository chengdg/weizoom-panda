# -*- coding: utf-8 -*-
import sys


reload(sys)
sys.setdefaultencoding("utf-8")
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "panda.settings")

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)



from django.core.management.base import BaseCommand
from eaglet.utils.resource_client import Resource
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST

from product import models as product_models
from account import models as account_models
from resource.models import *

relations = product_models.ProductSyncWeappAccount.objects.all().values('product_id').distinct()
bulk_create = []
accounts = product_models.SelfUsernameWeappAccount.objects.all()
account_count = accounts.count()
all_user_names = [account.self_user_name for account in accounts]
bulk_create = []
for relation in relations:
	product_id = relation.get('product_id')
	product_accounts = product_models.ProductSyncWeappAccount.objects.filter(product_id=product_id)
	product_users = [product_account.self_user_name for product_account in product_accounts]
	if account_count != len(product_users):
		# 需要同步
		need_insert_user_names = list(set(all_user_names) - set(product_users))
		temp_bulk = [product_models.ProductSyncWeappAccount(product_id=product_id,
															self_user_name=username)
					 for username in need_insert_user_names]
		bulk_create += temp_bulk
		print product_id, need_insert_user_names, 'need insert!'
product_models.ProductSyncWeappAccount.objects.bulk_create(bulk_create)
print 'All count is %s' % len(bulk_create)
print 'SUCCESS'
