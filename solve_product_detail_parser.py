# -*- coding: utf-8 -*-
import sys


reload(sys)
sys.setdefaultencoding("utf-8")
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "panda.settings")

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)

import HTMLParser
from django.core.management.base import BaseCommand

from product import models as product_models

products = product_models.Product.objects.filter(is_deleted=False)
temp_list = []
for product in products:
    remark = product.remark
    if remark.startswith('&lt;'):
        parser = HTMLParser.HTMLParser()
        txt = parser.unescape(remark)

        product.remark = txt
        # if product.id == 1:
        # print txt
        product.save()
        temp_list.append(str(product.id))
        print 'product_id:%s is ok!' % product.id
print ','.join(temp_list)
print 'All is ok!'
