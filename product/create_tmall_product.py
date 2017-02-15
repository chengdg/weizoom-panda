# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth

from core import resource
from core.jsonresponse import create_response
from core import paginator
from eaglet.utils.resource_client import Resource

from util import db_util
from resource import models as resource_models
from product_catalog import models as catalog_models
from account.models import *
from util import string_util
from panda.settings import ZEUS_HOST, ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
from product.sales_from_weapp import sales_from_weapp
import nav
import models
import requests
from util import sync_util
from weapp_relation import get_weapp_model_properties


class TmallProduct(resource.Resource):
	app = 'product'
	resource = 'tmall_product'

	def api_put(request):
		
		post = request.POST
		# 商品id
		# 商品名称
		# 商品图片
		# 商品的价格
		# 商品详情
		# 商品的remark
		tmall_id = post.get('tmall_id')
		name = post.get('name')
		images = post.get('images', '[]')
		price = post.get('price')
		detail = post.get('detail')
		remark = post.get('remark')
		user = User.objects.filter(username='tmall_weizoom').first()
		
		# 处理图片
		images = json.loads(images)
		image_model_ids = []
		for image in images:
			image_model = resource_models.Image.objects.create(user=user,
												 			   path=image)
			image_model_ids.append(image_model.id)
		
		product = models.Product.objects.create(
			owner=user,
			product_name=name,
			promotion_title='',
			product_price=price,
			clear_price=price,
			# product_weight=product_weight,
			product_store=-1,
			# has_limit_time=has_limit_time,
			# limit_clear_price=limit_clear_price,
			# has_product_model=false,
			# catalog_id=second_level_id,
			remark=detail,
			# limit_zone_type=limit_zone_type,
			# limit_zone=limit_zone_id,
			# has_same_postage=has_same_postage,
			# postage_money=postage_money,
			# postage_id=postage_id
		)
		
		for image_model_id in image_model_ids:
			models.ProductImage.objects.create(product=product, image_id=image_model_id)

		models.TmallProductInfo.objects.create(
			tmall_id=tmall_id,
			product_id=product.id,
			remark=remark
		)
		
		response = create_response(200)
		return response.get_response()

	def api_get(request):
		"""
		临时加接口返回这些天猫id是否已经添加过了
		"""
		tmall_ids = request.GET.get('tmall_ids')
		print '======================', type(tmall_ids)
		tmall_info = models.TmallProductInfo.objects.filter(tmall_id__in=json.loads(tmall_ids))
		# 暂时就返回这个吧
		tmall_info_ids = [db_model.tmall_id for db_model in tmall_info]
		data = {
			'ids': tmall_info_ids,
		}
		
		response = create_response(200)
		response.data = data
		return response.get_response()
		
		

