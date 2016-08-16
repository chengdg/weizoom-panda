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
            # count = product_models.ProductSyncWeappAccount.objects.filter(self_user_name__in=['weizoom_zhonghai',
            #                                                          'weizoom_juweihui'],
            #                                                               product_id=product_id).count()
            # print 'product_id:%s count :%s' % (product_id, count)
            # if count == 0:
            t_1 = product_models.ProductSyncWeappAccount(product_id=product_id,
                                                   self_user_name='weizoom_jinmeihui')

            t2 = product_models.ProductSyncWeappAccount(product_id=product_id,
                                                   self_user_name='weizoom_pengyouquan')
            t3 = product_models.ProductSyncWeappAccount(product_id=product_id,
                                                         self_user_name='weizoom_chh')

            t4 = product_models.ProductSyncWeappAccount(product_id=product_id,
                                                        self_user_name='weizoom_shxd')
            t5 = product_models.ProductSyncWeappAccount(product_id=product_id,
                                                         self_user_name='weizoom_wzbld')

            t6 = product_models.ProductSyncWeappAccount(product_id=product_id,
                                                        self_user_name='weizoom_zoomjulebu')
            bulk_create.append(t_1)
            bulk_create.append(t2)
            bulk_create.append(t3)
            bulk_create.append(t4)
            bulk_create.append(t5)
            bulk_create.append(t6)
            print 'product: %s is ok' % product_id
        product_models.ProductSyncWeappAccount.objects.bulk_create(bulk_create)
        print 'ALL is OK! COUNT is %s' % len(bulk_create)


