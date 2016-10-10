# -*- coding: utf-8 -*-
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from core import resource
from excel_response import ExcelResponse
from product_relation import getProductRelationData
from product import models as product_models
from account import models as account_models

class YunyingProductExported(resource.Resource):
	app = 'product'
	resource = 'yunying_product_exported'

	def get(request):
		is_export = True
		purchase_method = account_models.UserProfile.objects.get(user_id=request.user.id).purchase_method
		product_list = getProductRelationData(request,is_export)
		titles = [
			u'编号', u'商品名称', u'一级分类', u'二级分类', u'供货商', u'当月销售数量', u'当月销售金额'
			, u'累计销售数量', u'累计销售金额', u'客户来源', u'商品状态', u'停售原因'
		]
		product_table = []
		product_table.append(titles)
		for product in product_list:
			revoke_reasons = ''
			if product['product_status_value'] == 2:
				revoke_reasons = product['revoke_reasons']

			info = [
				'',
				product['product_name'],
				product['first_level_name'],
				product['second_level_name'],
				product['customer_name'],
				'-',
				'-',
				product['total_sales'],
				'-',
				product['customer_from_text'],
				product['product_status'],
				revoke_reasons
			]
			product_table.append(info)
		filename = u'商品统计列表'
		return ExcelResponse(product_table,output_name=filename.encode('utf8'),force_csv=False)