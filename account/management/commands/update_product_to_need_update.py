# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from eaglet.utils.resource_client import Resource
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST

from self_shop import models as self_shop_models
from account import models as account_models
from product import models as product_models


class Command(BaseCommand):

    def handle(self, **options):
        """
        把指定商品id的数据更新成需要同步更新的状态
        """
        product_ids = [4317 ,5144 ,5146 ,5168 ,5171 ,5172 ,5173 ,5174 ,5179 ,5180 ,5181 ,5184 ,5185 ,5214 ,5215 ,
                       5216 ,5217 ,5219 ,5220 ,5221 ,5223 ,5227 ,5229 ,5235 ,5239 ,5241 ,5243 ,5244 ,5246 ,5248 ,
                       5249 ,5250 ,5251 ,5394 ,5398 ,5464 ,5465 ,5466 ,5467 ,5468 ,5470 ,5472 ,5477 ,5488 ,5494 ,]
        product_models.Product.objects.filter(id__in=product_ids).update(is_update=True)
        bulk_create = []
        for product_id in product_ids:
            bulk_create.append(product_models.OldProduct(product_id=product_id))
        product_models.OldProduct.objects.bulk_create(bulk_create)
        print 'ALL is OK'
