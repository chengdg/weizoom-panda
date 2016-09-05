# -*- coding: utf-8 -*-
# __author__ = 'charles'

import sys
import os

reload(sys)
sys.setdefaultencoding("utf-8")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "panda.settings")

from django.core.management import execute_from_command_line

from eaglet.utils.resource_client import Resource
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST

from product import models as product_models
import logging
logger = logging.Logger('message')
# from product import models as product_models

execute_from_command_line(sys.argv)

deleted_products = product_models.Product.objects.filter(is_deleted=True)
count = 0
for product in deleted_products:

    relation = product_models.ProductHasRelationWeapp.objects.filter(product_id=product.id).first()
    if relation:
        weapp_product_id = relation.weapp_product_id
        params = {
            'weapp_product_id': weapp_product_id
        }
        resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).delete({
            'resource': 'mall.sync_product',
            'data': params
        })

        if resp and resp.get('code') == 200:
            count += 1
            print 'product: %s is ok!' % product.id
        else:
            print 'product: %s is failed!' % product.id, weapp_product_id
print 'All is OK!'
print 'Count is %s' % count
