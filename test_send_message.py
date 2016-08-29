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
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
import json
products = product_models.Product.objects.filter(is_deleted=False)
temp_list = []
supplier_ids = [3752,481,677,676]
params = {
    'page': 1,
    'per_count_page': 1000,
    'order_status': 3,
    'supplier_ids': json.dumps(supplier_ids)
}
resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post(
    {
        'resource': 'panda.order_list',
        'data': params
    }
)
if resp and resp.get('code') == 200:
    count = resp.get('data').get('count')
    print '++++++++++++++++++++++++++++++++++%s' % count
