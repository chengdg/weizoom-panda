# -*- coding: utf-8 -*-
# __author__ = 'charles'

import sys


reload(sys)
sys.setdefaultencoding("utf-8")
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "panda.settings")

from django.core.management import execute_from_command_line


from django.core.management.base import BaseCommand
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
import json
import xlrd

from product import models as product_models
from product_catalog import models as catalog_models
import logging
logger = logging.Logger('message')

execute_from_command_line(sys.argv)

file_name_dir = '%s' % './new_product_catalog_hate.xls'
data = xlrd.open_workbook(file_name_dir)
table = data.sheet_by_index(0)
# 行数
nrows = table.nrows
can_not_find_products = []
can_not_find_catalog = []
catalog_not_sync = []
# catalogs = catalog_models.ProductCatalog.objects.filter(level=2)
# catalog_name_2_id = dict([(catalog.name, catalog.id) for catalog in catalogs])
# products = product_models.Product.objects.filter(is_deleted=False)
# product_name_2_id = dict([(product.product_name, product.id) for product in products])
# product_name_2_catalog_id = dict([(product.product_name, product.catalog_id) for product in products])
# print product_name_2_catalog_id
# print product_name_2_id
# print catalog_name_2_id
for product in product_models.Product.objects.filter(is_deleted=False):

    product_id = product.id
    # product = product_models.Product.objects.filter(product_name=product_name).first()
    # print '%s' % product_name
    catalog_id = product.catalog_id
    # print '====================================================================='
    # print catalog_id, product_id
    # print '====================================================================='

    if not catalog_id:
        continue
    # 更新商品的类目

    catalog_relation = catalog_models.ProductCatalogRelation.objects.filter(id=catalog_id).first()

    product_relation = product_models.ProductHasRelationWeapp.objects.filter(product_id=product_id).first()
    if not catalog_relation or not product_relation:
        continue
    # 同步到we app
    catalog_params = {'classification_id': catalog_relation.weapp_catalog_id,
                      'product_id': product_relation.weapp_product_id}
    resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post({
        'resource': 'mall.classification_product',
        'data': catalog_params
    })

    if not resp or resp.get('code') == 200:
        watchdog.info({'errorMsg': 'Panda product: %s sync catalog Success!' % product.id})
        print '====================================================================='
    else:
        # catalog_params = {'classification_id': weapp_catalog_id,
        # 				  'product_id': relation.weapp_product_id}
        resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put({
            'resource': 'mall.classification_product',
            'data': catalog_params
        })
        if not resp or resp.get('code') != 200:
            watchdog.error({'errorMsg': 'Panda product: %s sync catalog failed!' % product.id})
print 'ALL is Ok'

