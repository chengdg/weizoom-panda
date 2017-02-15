# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from eaglet.utils.resource_client import Resource
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST

from self_shop import models as self_shop_models
from account import models as account_models
import datetime


class Command(BaseCommand):

    def handle(self, **options):
        """
        创建一个天猫商城供货商
        """
        user = account_models.User.objects.create_user('tmall_weizoom', 'tmall_weizoom@weizoom.com', "test")
        account_models.UserProfile.objects.filter(user_id=user).update(
            purchase_method=1,
            valid_time_from=datetime.datetime.now(),
            valid_time_to='2099-01-01',
            is_active=True,
            status=1,
            corpid='tmall_weizoom',
            name='天猫商城'
            
            
        )
        print '==================is OK========================'
        
        