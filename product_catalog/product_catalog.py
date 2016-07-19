# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from core import resource
from core.jsonresponse import create_response
from core import paginator

from util import string_util
from account import models as account_models
from product import models as product_models
from panda.settings import ZEUS_HOST
from util import db_util
import models as product_catalog_models
import nav
import requests

FIRST_NAV = 'product_catalog'
SECOND_NAV = 'product_catalog'
# COUNT_PER_PAGE = 10

class Fans(resource.Resource):
	app = 'product_catalog'
	resource = 'product_catalogs'

	@login_required
	def get(request):
		"""
		显示商品列表
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV
		})
		return render_to_response('product_catalog/product_catalogs.html', c)

	def api_get(request):
		cur_page = request.GET.get('page', 1)
		catalogs = product_catalog_models.ProductCatalog.objects.all().order_by('-created_at')
		rows = []
		for catalog in catalogs:
			rows.append({
				'id': catalog.id,
				'father_catalog': catalog.father_catalog,
				'catalog_name': catalog.catalog_name,
				'note': catalog.note,
				'created_at': catalog.created_at.strftime("%Y-%m-%d %H:%M:%S"),
				'products_number': 0
			})
		data = {
			'rows': rows
		}
		response = create_response(200)
		response.data = data
		return response.get_response()

	@login_required
	def api_put(request):
		# 新建商品分类
		post = request.POST
		catalog_name = post.get('catalog_name','')
		father_catalog = int(post.get('father_catalog',-1))
		note = post.get('note','')
		try:
			product_catalog_models.ProductCatalog.objects.create(
				catalog_name = catalog_name,
				father_catalog = father_catalog,
				note = note
			)
			response = create_response(200)
		except:
			response = create_response(500)
			response.errMsg = u'新建失败'
			response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	@login_required
	def api_post(request):
		# 编辑商品分类
		post = request.POST
		catalog_id = post.get('catalog_id','')
		catalog_name = post.get('catalog_name','')
		note = post.get('note','')
		try:
			product_catalog_models.ProductCatalog.objects.filter(id=catalog_id).update(
				catalog_name = catalog_name,
				note = note
			)
			response = create_response(200)
		except:
			response = create_response(500)
			response.errMsg = u'编辑失败'
			response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	@login_required
	def api_delete(request):
		catalog_id = request.POST.get('id','')
		try:
			catalog = product_catalog_models.ProductCatalog.objects.get(id=catalog_id)
			catalog.delete()
			response = create_response(200)
			return response.get_response()
		except:
			response = create_response(500)
			response.errMsg = u'删除失败'
			return response.get_response()