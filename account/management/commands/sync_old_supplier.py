# -*- coding: utf-8 -*-
# __author__ = 'charles'

from django.core.management.base import BaseCommand
from eaglet.utils.resource_client import Resource
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST

from account import models as account_models


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        同步旧的没有同步过得供应商
        """
        # product_models.A.objects.filter()

        # user_id = models.IntegerField(default=0)  # 对应自营平台user_id
        # account_id = models.IntegerField(default=0)  # UserProfile id
        # supplier_id = models.IntegerField(default=0)  # 云上通的供货商id
        # store_name = models.CharField(max_length=1024, default='')  # y供货商名称
        accounts = account_models.UserProfile.objects.filter(is_active=True,
                                                             role=account_models.CUSTOMER)
        for account in accounts:
            user_id = account.user_id
            account_id = account.id
            params = {
                'name': account.name,
                'remark': '',
                'responsible_person': u'8000FT',
                'supplier_tel': '13112345678',
                'supplier_address': u'中国 北京'
            }
            resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put(
                {
                    'resource': 'mall.supplier',
                    'data': params
                }
            )

            if resp:
                if resp.get('code') == 200:
                    account_models.AccountHasSupplier.objects.filter(user_id=user_id,
                                                                     account_id=account_id)\
                        .update(user_id=-user_id,
                                account_id=-account_id)
                    # 创建新数据
                    account_models.AccountHasSupplier.objects.create(
                        user_id=user_id,
                        account_id=account_id,
                        # store_name = account_zypt_info['store_name'].encode('utf8'),
                        supplier_id=int(resp.get('data').get('id'))
                    )
                else:
                    print 'user_id: %s , account_id: %s is failed!' % (user_id, account_id)
            else:
                print 'user_id: %s , account_id: %s is failed!' % (user_id, account_id)

