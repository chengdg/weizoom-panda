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
from product_catalog import models as catalog_models


products = product_models.Product.objects.exclude(is_deleted=True,
                                                  catalog_id=0)

catalogs = catalog_models.ProductCatalogRelation.objects.all()
# 所有分类关系(panda分类id: weapp分类id)
catalog_2_weapp_catalog = dict([(catalog.catalog_id, catalog.weapp_catalog_id) for catalog in catalogs])
temp_list = []
for product in products:
    relation = product_models.ProductHasRelationWeapp.objects.filter(product_id=product.id).first()
    if relation:
        # 对应云上通的商品id
        weapp_product_id = relation.weapp_product_id
        # 对应云上通的分类id
        weapp_catalog_id = catalog_2_weapp_catalog.get(product.catalog_id)
        if weapp_catalog_id:
            # temp_dict.update({})
            temp_list.append((weapp_product_id, weapp_catalog_id))
import json
# print temp_list
temp_file = open('./temp_file.txt', 'wt')
temp_file.write(json.dumps(temp_list))
print 'OK!'
