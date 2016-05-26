# -*- coding: utf-8 -*-
import logging

from product import models as product_models

def clean():
	logging.info('clean database for product app')
	product_models.Product.objects.all().delete()
	product_models.ProductImage.objects.all().delete()
