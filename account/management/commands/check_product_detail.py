# -*- coding: utf-8 -*-
# __author__ = 'charles'

from django.core.management.base import BaseCommand
from eaglet.utils.resource_client import Resource
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
import json

from account import models as account_models
from product import models as product_models


class Command(BaseCommand):

    def handle(self, *args, **options):
        """

        """
        with open('./supplier.txt', 'wt') as f:
            products = product_models.Product.objects.filter()
            temp_dict = {}
            for product in products:
                relation = product_models.ProductHasRelationWeapp.objects.filter(product_id=product.id).first()
                if relation:
                    weapp_product_id = relation.weapp_product_id
                    temp_dict.update({weapp_product_id: product.remark})
                    print 'weapp_product_id:%s is OK' % weapp_product_id
            # temp_string =
            f.write(json.dumps(temp_dict))
            print 'SUCCESS!'
