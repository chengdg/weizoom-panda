# -*- coding: utf-8 -*-
# __author__ = 'charles'

from django.core.management.base import BaseCommand
from eaglet.utils.resource_client import Resource
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST

from product import models as product_models
from account import models as account_models
from resource.models import *

from datetime import datetime
import xlsxwriter
from core.sendmail import sendmail

class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        同步商品到新的自营平台。

        """
        # product_models.A.objects.filter()

        # user_id = models.IntegerField(default=0)  # 对应自营平台user_id
        # account_id = models.IntegerField(default=0)  # UserProfile id
        # supplier_id = models.IntegerField(default=0)  # 云上通的供货商id
        # store_name = models.CharField(max_length=1024, default='')  # y供货商名称
        file_path = 'PRODUCT_SHELVE_OFF.xlsx'
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        workbook   = xlsxwriter.Workbook(file_path)
        table = workbook.add_worksheet()
        alist = [u"商品名称", u"下架原因"]

        product_ids = product_models.ProductRevokeLogs.objects.all().values('product_id').distinct()
        products = product_models.Product.objects.filter(id__in=product_ids)
        tmp_line = 1
        for product in products:
            name = product.name
            reason = ""
            for log in product_models.ProductRevokeLogs.objects.filter(product_id=product.id):
                reason = reason + log.revoke_reasons


            tmp_line += 1
            tmp_list = [name, reason]

            table.write_row('A{}'.format(tmp_line),tmp_list)

        workbook.close()
        receivers = ['zhangzhiyong@weizoom.com', 'guoyucheng@weizoom.com']
        mode = ''
        if len(args) == 1:
            if args[0] == 'test':
                mode = 'test'
                receivers = ['guoyucheng@weizoom.com']
        title = u'下架商品及原因{}'.format(current_time)
        content = u'您好，下架商品及原因'

        sendmail(receivers, title, content, mode, file_path)