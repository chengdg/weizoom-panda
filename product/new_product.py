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
from util import string_util

from resource import models as resource_models
from account.models import *
import nav
import models

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
		#获取业务数据
		product_id = request.GET.get('id', None)
		jsons = {'items':[]}
		role = UserProfile.objects.get(user_id=request.user.id).role
		user_has_products = len(models.Product.objects.filter(owner_id=request.user.id))
		if product_id:
			if role == YUN_YING:
				product = models.Product.objects.get(id=product_id)
			else:
				product = models.Product.objects.get(owner=request.user, id=product_id)
			product_data = {
				'id': product.id,
				'product_name': product.product_name,
				'promotion_title': product.promotion_title,
				'product_price': '%s' % product.product_price,
				'clear_price': '%s' % product.clear_price,
				'product_weight': product.product_weight,
				'product_store': product.product_store,
				'remark': string_util.raw_html(product.remark),
				'images': [],
			}
	
			#获取商品图片
			product_image_ids = [product_image.image_id for product_image in models.ProductImage.objects.filter(product_id=product_id)]
			for image in resource_models.Image.objects.filter(id__in=product_image_ids):
				product_data['images'].append({
					'id': image.id,
					'path': image.path
				})

			jsons['items'].append(('product', json.dumps(product_data)))
		else:
			jsons['items'].append(('product', json.dumps(None)))

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
			'jsons': jsons,
			'user_has_products': user_has_products,
			'role': role
		})
		return render_to_response('product/new_product.html', c)

	def api_put(request):
		post = request.POST
		product_name = post.get('product_name','')
		promotion_title = post.get('promotion_title','')
		product_price = post.get('product_price',0)
		clear_price = post.get('clear_price',0)
		product_weight = post.get('product_weight',0)
		product_store = int(post.get('product_store',-1))
		remark = post.get('remark','')
		images = post.get('images','')
		product = models.Product.objects.create(
			owner = request.user, 
			product_name = product_name, 
			promotion_title = promotion_title, 
			product_price = product_price,
			clear_price = clear_price,
			product_weight = product_weight,
			product_store = product_store,
			remark = remark
		)

		#获取商品图片
		if images:
			product_images = json.loads(request.POST['images'])
			for product_image in product_images:
				models.ProductImage.objects.create(product=product, image_id=product_image['id'])

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		#更新商品
		post = request.POST
		product_name = post.get('product_name','')
		promotion_title = post.get('promotion_title','')
		product_price = post.get('product_price',0)
		clear_price = post.get('clear_price',0)
		product_weight = post.get('product_weight',0)
		product_store = post.get('product_store',0)
		product_store_type = int(post.get('product_store_type',-1))
		if product_store_type == -1:
			product_store = -1
		remark = post.get('remark','')
		images = post.get('images','')
		models.Product.objects.filter(owner=request.user, id=request.POST['id']).update(
			owner = request.user, 
			product_name = product_name, 
			promotion_title = promotion_title, 
			product_price = product_price,
			clear_price = clear_price,
			product_weight = product_weight,
			product_store = product_store,
			remark = remark
		)

		#删除、重建商品图片
		if images:
			product = models.Product.objects.get(owner=request.user, id=request.POST['id'])
			models.ProductImage.objects.filter(product_id=product.id).delete()
			product_images = json.loads(request.POST['images'])
			for product_image in product_images:
				models.ProductImage.objects.create(product=product, image_id=product_image['id'])

		response = create_response(200)
		return response.get_response()

	def api_delete(request):
		models.Product.objects.filter(owner=request.user, id=request.POST['id']).delete()

		response = create_response(200)
		return response.get_response()

