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
        with open('./json.txt', 'wt') as f:
            new_relations = product_models.ProductHasRelationWeapp.objects.filter(product_id__gt=0)
            temp_dict = {}
            for new_relation in new_relations:
                panda_product_id = new_relation.product_id
                new_weapp_product_id = new_relation.weapp_product_id
                old_relations = product_models.ProductHasRelationWeapp.objects.filter(product_id=-panda_product_id)
                old_weapp_product_ids = [old_relation.weapp_product_id for old_relation in old_relations]
                temp_dict.update({new_weapp_product_id: old_weapp_product_ids})
            temp_string = json.dumps(temp_dict)
            print type(temp_string)
            f.write(temp_string)
