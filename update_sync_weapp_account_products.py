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
for relation in relations:
	product_id = relation.get('product_id')
	count = product_models.ProductSyncWeappAccount.objects.filter(self_user_name__in=['weizoom_fulilaile'],
																  product_id=product_id).count()
	print 'product_id:%s count :%s' % (product_id, count)
	if count == 0:
		t_1 = product_models.ProductSyncWeappAccount(product_id=product_id,
													 self_user_name='weizoom_fulilaile')

		bulk_create.append(t_1)
		print 'product: %s is ok' % product_id
product_models.ProductSyncWeappAccount.objects.bulk_create(bulk_create)
print 'ALL is OK! COUNT is %s' % len(bulk_create)

print('start...')
