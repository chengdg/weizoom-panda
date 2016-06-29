# -*- coding: utf-8 -*-
import os
import sys
import json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)

from django.conf import settings
from django.db.models.aggregates import Sum
from django.db.models.aggregates import Count
from django.contrib.auth.models import User, Group, Permission
from datetime import datetime
from mall.models import *


suppliers = [

['p-测试用户', '测试用户']
['p-北京联合启源科技有限公司','联合启源'],
['p-北京百利勤国际贸易有限公司','百利勤'],
['p-张雪', '张雪']
]

print len(suppliers)
count = 0
for supplier_info in suppliers:
    for s in Supplier.objects.filter(name=supplier_info[1], is_delete=False):
        if Supplier.objects.filter(name=supplier_info[0], owner=s.owner, is_delete=False).count() == 1:
            supplier0 = Supplier.objects.filter(name=supplier_info[0], owner=s.owner,  is_delete=False).first()
            supplier1 = s

            Product.objects.filter(supplier=supplier1.id).update(supplier=supplier0.id)
            Order.objects.filter(supplier=supplier1.id).update(supplier=supplier0.id)
            count += 1

print "count=", count
print "success!"