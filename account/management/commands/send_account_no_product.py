# -*- coding: utf-8 -*-
#__auth__='justiing'
import logging
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import Q,F

#邮件部分
from core.sendmail import sendmail


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
from account.models import UserProfile
import xlsxwriter

from datetime import datetime,timedelta,date
DATE_FORMAT="%Y-%m-%d"


class Command(BaseCommand):
	help = "send product sales email"
	args = ''
	
	def handle(self,*args, **options):
			print args


			file_path = 'account_no_product_list.xlsx'
			workbook   = xlsxwriter.Workbook(file_path)
			table = workbook.add_worksheet()
			alist = [u'帐号名称',u'公司名称',u"联系人", u"手机号"]
			
			table.write_row('A1',alist)
			accounts = UserProfile.objects.filter(is_active=True, role=1, product_count=0).order_by('created_at')
			tmp_line = 1
			for account in accounts:
				tmp_line += 1
				tmp_list = [account.name, account.company_name, account.contacter, account.phone]


				table.write_row('A{}'.format(tmp_line),tmp_list)

			workbook.close()
			receivers = ['guoyucheng@weizoom.com', 'wangzhen01@weizoom.com','gaoyang@weizoom.com','chenjuan@weizoom.com']
			mode = ''
			if len(args) == 1:
				if args[0] == 'test':
					mode = 'test'
					receivers = ['guoyucheng@weizoom.com']
			title = u'未添加商品帐号{}'.format(datetime.now())
			content = u'您好，未添加商品帐号'

			sendmail(receivers, title, content, mode, file_path)

