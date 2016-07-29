# -*- coding: utf-8 -*-
# __author__ = 'charles'

from django.core.management.base import BaseCommand
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
import json

from account import models as account_models
from util import send_phone_msg


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        定时任务,给供货商发短信
        """
        accounts = account_models.UserProfile.objects.filter(role=account_models.CUSTOMER,
                                                             is_active=True)
        # print '++++++++++++++++++++++++++++++++++++=', accounts.count()
        content = u'您好，当前您有%s个订单，请及时处理'
        number_message = 0
        account_ids = []
        for account in accounts:
            phone = account.phone

            # print '++++++++++++++++++++++'
            if account.phone:
                supplier_relation = account_models.AccountHasSupplier.objects.filter(user_id=account.user_id).first()
                old_supplier_relation = account_models.AccountHasSupplier.objects.filter(user_id=-account.user_id)
                supplier_ids = []
                if supplier_relation:
                    supplier_ids.append(supplier_relation.supplier_id)
                for relation in old_supplier_relation:
                    supplier_ids.append(relation.supplier_id)
                if not supplier_ids:
                    continue
                params = {
                    'page': 1,
                    'per_count_page': 15,
                    'order_status': 3,
                    'supplier_ids': json.dumps(supplier_ids)
                }
                resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post(
                    {
                        'resource': 'panda.order_list',
                        'data': params
                    }
                )
                # print '=======================', resp
                if resp and resp.get('code') == 200:

                    count = resp.get('data').get('count')
                    account_ids.append([account.user_id, supplier_ids, count])
                    # print '++++++++++++++++++++++++++++++++++++=', phone, count
                    if count > 0:
                        rs = send_phone_msg.send_phone_captcha(phones=str(phone), content=content % count)
                        print content % count
                        if rs:
                            number_message += 1
                            # account_ids.append(account.user_id)
                        # print rs
                        print '供货商%s发送结果是%s' % (str(account.user_id), 'SUCCESS' if rs else 'FAILED')
                        watchdog.info('供货商%s发送结果是%s' % (str(account.user_id), 'SUCCESS' if rs else 'FAILED'))
                    # watchdog.info('供货商%s发送结果是%s' % (account.user_id, 'SUCCESS' if rs else 'FAILED'))
        print '本次一共发送了%s条短信' % number_message
        print '这些帐号ｉｄ是:', account_ids
