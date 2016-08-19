# -*- coding: utf-8 -*-
import sys


reload(sys)
sys.setdefaultencoding("utf-8")
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "panda.settings")

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)

from django.core.management.base import BaseCommand
import xlwt
from eaglet.utils.resource_client import Resource
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
from product import models as product_models
from account import models as account_models

products = product_models.Product.objects.filter(is_deleted=False)
temp_count = 0
temp_list = []
product_list = []
accounts = account_models.UserProfile.objects.filter(role=1,
                                                     is_active=True)
owner_to_company_name = {}
for account in accounts:
    owner_to_company_name.update({account.user_id: account.name})
file_s = open('temp.txt', 'w')
row_number = 0
workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('My Worksheet')
for product in products:
    temp_count += 1
    temp_list.append(product.id)
    product_list.append(product)
    # print temp_count, '>>>>>>>>>>>>>>>>>>>>>.'
    if temp_count % 20 == 0 or temp_count == products.count():
        relations = product_models.ProductHasRelationWeapp.objects.filter(product_id__in=temp_list)
        weapp_product_ids = [relation.weapp_product_id for relation in relations if relation.weapp_product_id]
        weapp_product_id_to_product_id = dict()
        for relation in relations:
            weapp_product_id_to_product_id.update({relation.product_id: relation.weapp_product_id})
        params = {
            'product_ids': '_'.join(weapp_product_ids)
        }
        resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).get({
            'resource': 'panda.product_pool_status',
            'data': params
        })
        if resp and resp.get('code') == 200:
            data = resp.get('data').get('product_pool')
            # print product_list
            for temp_product in product_list:
                shop_info = data.get(weapp_product_id_to_product_id.get(temp_product.id))
                # print shop_info
                info_str = []
                if not shop_info:
                    continue
                for info in shop_info:

                    store_name = info.get(u'store_name')
                    status = info.get(u'status')
                    # print store_name, status, '++++++++++++++++++++++++++++++++++++++', \
                    #     weapp_product_id_to_product_id.get(temp_product.id)
                    if store_name:
                        # status = info.get('status', '')
                        # print '--------------------------------'
                        info_str.append(store_name + '-' + status)

                string = '%s	%s	%s	\n' % (temp_product.product_name,
                                             owner_to_company_name.get(product.owner_id),
                                             ','.join(info_str))
                file_s.write(string)
                worksheet.write(row_number, 0, label=temp_product.product_name)
                worksheet.write(row_number, 1, label=owner_to_company_name.get(product.owner_id))
                worksheet.write(row_number, 2, label=','.join(info_str))

                row_number += 1

                # print string, '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
        temp_list = []
        product_list = []

workbook.save('Excel_Workbook.xls')
