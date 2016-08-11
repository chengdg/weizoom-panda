# -*- coding: utf-8 -*-
# __author__ = 'charles'

from django.core.management.base import BaseCommand
from eaglet.utils.resource_client import Resource
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST

from product import models as product_models
from account import models as account_models
from resource.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        同步商品到新的自营平台。

        """
        # product_models.A.objects.filter()

        # user_id = models.IntegerField(default=0)  # 对应自营平台user_id
        # account_id = models.IntegerField(default=0)  # UserProfile id
        # supplier_id = models.IntegerField(default=0)  # 云上通的供货商id
        # store_name = models.CharField(max_length=1024, default='')  # y供货商名称
        relations = product_models.ProductSyncWeappAccount.objects.all().values('product_id').distinct()
        bulk_create = []
        for relation in relations:
            product_id = relation.get('product_id')
            t_1 = product_models.ProductSyncWeappAccount(product_id=product_id,
                                                   self_user_name='weizoom_zhonghai')

            t2 = product_models.ProductSyncWeappAccount(product_id=product_id,
                                                   self_user_name='weizoom_juweihui')

            bulk_create.append(t_1)
            # bulk_create.append(t2)
            print 'product: %s is ok' % product_id
        product_models.ProductSyncWeappAccount.objects.bulk_create(bulk_create)
        print 'ALL is OK! COUNT is %s' % len(bulk_create)


