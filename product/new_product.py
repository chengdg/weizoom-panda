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
import nav
import models
from resource import models as resource_models
from util import string_util

FIRST_NAV = 'product'
SECOND_NAV = 'product-list'

class NewProduct(resource.Resource):
	app = 'product'
	resource = 'new_product'

	@login_required
	def get(request):
		"""
		显示商品创建页面
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV
		})
		return render_to_response('product/new_product.html', c)

	@login_required
	def api_put(request):
		post = request.POST
		product_name = post.get('product_name','')
		promotion_title = post.get('promotion_title','')
		product_price = post.get('product_price','')
		clear_price = post.get('clear_price','')
		product_weight = post.get('product_weight','')
		product_store = post.get('product_store','')
		remark = post.get('remark','')

		product = models.Product.objects.create(
			owner = request.user, 
			product_name = product_name, 
			promotion_title = promotion_title, 
			product_price = product_price,
			clear_price = clear_price,
			product_weight = product_weight,
			remark = remark
		)

		#获取商品图片
		product_images = json.loads(request.POST['images'])
		for product_image in product_images:
			models.ProductImage.objects.create(product=product, image_id=product_image['id'])

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_delete(request):
		models.Product.objects.filter(owner=request.user, id=request.POST['id']).delete()

		response = create_response(200)
		return response.get_response()

