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
from product_list import getProductData
from product import models as product_models
from account import models as account_models

SELF_SHOP2TEXT = {
    'weizoom_jia': u'微众家',
    'weizoom_mama': u'微众妈妈',
    'weizoom_xuesheng': u'微众学生',
    'weizoom_baifumei': u'微众白富美',
    'weizoom_shop': u'微众商城',
    'weizoom_club': u'微众俱乐部',
    'weizoom_life': u'微众Life',
    'weizoom_yjr': u'微众一家人'
}

class CustomerExported(resource.Resource):
	app = 'product'
	resource = 'product_exported'

	def get(request):
		is_export = True
		product_list = getProductData(request,is_export)
		titles = [
			u'id', u'编号', u'一级分类', u'二级分类', u'商品名称', u'促销标题', u'商品价格(元)', u'结算价(元)', u'限时结算价(元)', u'有效期'
			, u'商品重量(Kg)', u'商品主图', u'商品轮播图', u'商品描述'
		]
		product_table = []
		product_table.append(titles)
		for product in product_list:
			product_name = product['product_name']
			info = [
				product['id'],
				'',
				'',
				'',
				product['product_name'],
				product['promotion_title'],
				product['product_price'],
				product['clear_price'],
				product['limit_clear_price'],
				product['has_limit_time'],
				product['product_weight'],
				product['image_path'],
				u'，'.join(product['image_paths']),
				product['remark']
			]
			product_table.append(info)
		filename = u'商品统计列表'
		return ExcelResponse(product_table,output_name=filename.encode('utf8'),force_csv=False)