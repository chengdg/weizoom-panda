# -*- coding: utf-8 -*-
__author__ = 'lihanyi'

import json
import time
import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.exceptionutil import unicode_full_stack
from core import resource
from core.jsonresponse import create_response
from core import paginator
from util import db_util
import nav
import requests
from excel_response import ExcelResponse
from manager_account import ManagerAccount


class ExportAccounts(resource.Resource):
	app = 'manager'
	resource = 'account_export'

	@login_required
	def get(request):
		accounts = ManagerAccount.api_get(request)
		titles = [
			u'账号id', u'对应user_id', u'账号类型', u'账号名称', u'登录账号', u'公司名称',
			u'联系人', u'手机号', u'采购方式', u'备注', u"经营类目", u"创建时间"
		]
		table = []
		table.append(titles)
		for account in accounts:
			table.append([
				account['id'],
				account['user_id'],
				account['role'],
				account['name'],
				account['username'],
				account['company_name'],
				account['contacter'],
				account['phone'],
				account['purchase_method'],
				account['note'],
				account['companyType'],
				account['createdAt']
			])
		return ExcelResponse(table, output_name=u'账号管理文件'.encode('utf8'), force_csv=False)