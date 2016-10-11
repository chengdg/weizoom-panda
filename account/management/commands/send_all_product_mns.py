# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from product import models as product_models
from resource import models as resource
from util import send_product_message


class Command(BaseCommand):

    def handle(self, **options):
        """
        发送所有商品的mns信息
        """
        products = product_models.Product.objects.filter(is_deleted=False)
        count = 0
        for product in products:
            image_relation = product_models.ProductImage.objects.filter(product_id=product.id).first()
            image_path = ''
            if image_relation:
                image = resource.Image.objects.filter(id=image_relation.image_id).first()
                if image:
                    image_path = image.path

            send_product_message.send_add_product_message(product=product, user_id=product.owner_id,
                                                          image_paths=image_path)
            print 'Product {} was send!'.format(product.id)
            count += 1
        print 'ALL is OK!Fixed products count is {}'.format(count)


