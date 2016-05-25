# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from core import paginator
from util import db_util
from resource import models as resource_models
from util import string_util
import nav
import models

FIRST_NAV = 'product'
SECOND_NAV = 'product-list'

class ProductList(resource.Resource):
	app = 'product'
	resource = 'product_list'

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
		
		return render_to_response('product/product_list.html', c)

	def api_get(request):
		products = models.Product.objects.filter(owner=request.user)
		product_images = models.ProductImage.objects.all()
		#组装数据
		rows = []

		#获取商品图片
		product_id2image_id = {}
		image_id2images = {}

		# product_image_ids = [product_image.image_id for product_image in models.ProductImage.objects.filter(product_id=product_id)]
		for product in product_images:
			product_id2image_id[product.product_id] = product.image_id
		for image in resource_models.Image.objects.all():
			image_id2images[image.id] = json.dumps([{
				'id':image.id,
				'path': image.path
			}])

		for product in products:
			# image_id = product_id2image_id[product.id]
			# images = image_id2images[image_id]
			rows.append({
				'id': product.id,
				'promotion_title': product.promotion_title,
				'product_price': '%.2f' %product.product_price,
				'product_name': product.product_name,
				# 'images': images,
				'status': u'已上架',
				'sales': '100',
				'created_at': product.created_at.strftime('%Y-%m-%d %H:%M:%S'),
			})
		data = {
			'rows': rows,
			# 'pagination_info': pageinfo.to_dict()
		}

		#构造response
		response = create_response(200)
		response.data = data

		return response.get_response()
