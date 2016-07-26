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
from core.exceptionutil import unicode_full_stack
from core import paginator
from util import db_util
from util import string_util

from resource import models as resource_models
from account.models import *
from product.product_has_model import get_product_model_property_values
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
		second_level_id = request.GET.get('second_level_id', 0)
		jsons = {'items':[]}
		user_profile = UserProfile.objects.get(user_id=request.user.id)
		role = user_profile.role
		purchase_method = user_profile.purchase_method #采购方式
		points = user_profile.points #零售价返点
		product_has_model = 0
		if product_id:
			if role == YUN_YING:
				product = models.Product.objects.get(id=product_id)
				product_models = models.ProductModel.objects.filter(product_id=product_id)
				product_has_model = 1
			else:
				model_properties = models.ProductModelProperty.objects.filter(owner=request.user)
				property_ids = [model_propertie.id for model_propertie in model_properties]
				property_values = models.ProductModelPropertyValue.objects.filter(property_id__in=property_ids)
				product_has_model = len(property_values)
				product = models.Product.objects.get(owner=request.user, id=product_id)
				product_models = models.ProductModel.objects.filter(product_id=product_id,owner=request.user)
			limit_clear_price = ''
			if product.limit_clear_price and product.limit_clear_price != -1:
				limit_clear_price = product.limit_clear_price

			# product_models = models.ProductModel.objects.filter(product_id=product_id,owner=request.user)
			product_model_ids = [product_model.id for product_model in product_models]
			property_values = models.ProductModelHasPropertyValue.objects.filter(model_id__in=product_model_ids)

			value_ids = set([str(property_value.property_value_id) for property_value in property_values])
			product_model_property_values = models.ProductModelPropertyValue.objects.filter(id__in=value_ids)
			model_values = get_product_model_property_values(product_model_property_values)
			
			product_data = {
				'id': product.id,
				'product_name': product.product_name,
				'promotion_title': product.promotion_title,
				'product_price': '%s' % product.product_price if product.product_price>0 else '%s' % product.clear_price,
				'clear_price': '%s' % product.clear_price,
				'product_weight': '%s'% product.product_weight,
				'product_store': product.product_store,
				'has_limit_time': '%s' %(1 if product.has_limit_time else 0),
				'valid_time_from': '' if not product.valid_time_from else product.valid_time_from.strftime("%Y-%m-%d %H:%M"),
				'valid_time_to': '' if not product.valid_time_to else product.valid_time_to.strftime("%Y-%m-%d %H:%M"),
				'limit_clear_price': '%s' % limit_clear_price,
				'remark': string_util.raw_html(product.remark),
				'has_product_model': '%s' %(1 if product.has_product_model else 0),
				'model_values': json.dumps(model_values),
				'images': [],
				'value_ids': ','.join(value_ids)
			}

			for product_model in product_models:
				model_Id = product_model.name
				product_data['product_price_'+model_Id] = '%s' %product_model.price
				product_data['limit_clear_price_'+model_Id] = '%s' %product_model.limit_clear_price
				product_data['clear_price_'+model_Id] = '%s' %product_model.market_price
				product_data['product_weight_'+model_Id] = '%s' %product_model.weight
				product_data['product_store_'+model_Id] = '%s' %product_model.stocks
				product_data['product_code_'+model_Id] = '%s' %product_model.user_code
				product_data['valid_time_from_'+model_Id] = '%s' %product_model.valid_time_from.strftime("%Y-%m-%d %H:%M") if product_model.valid_time_from else ''
				product_data['valid_time_to_'+model_Id] = '%s' %product_model.valid_time_to.strftime("%Y-%m-%d %H:%M") if product_model.valid_time_to else ''

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
			model_properties = models.ProductModelProperty.objects.filter(owner=request.user)
			property_ids = [model_propertie.id for model_propertie in model_properties]
			property_values = models.ProductModelPropertyValue.objects.filter(property_id__in=property_ids)
			product_has_model = len(property_values)
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
			'jsons': jsons,
			'second_level_id': second_level_id,
			'role': role,
			'points': points,
			'purchase_method': purchase_method,
			'product_has_model': product_has_model
		})
		return render_to_response('product/new_product.html', c)

	def api_put(request):
		post = request.POST
		product_name = post.get('product_name','')
		promotion_title = post.get('promotion_title','')
		product_price = post.get('product_price',-1)
		clear_price = post.get('clear_price',0)
		product_weight = post.get('product_weight',0)
		product_store = int(post.get('product_store',-1))
		has_limit_time = int(post.get('has_limit_time',0))
		limit_clear_price = post.get('limit_clear_price',-1)
		valid_time_from = post.get('valid_time_from','')
		valid_time_to = post.get('valid_time_to','')
		remark = post.get('remark','')
		images = post.get('images','')
		has_product_model = int(post.get('has_product_model',0))
		second_level_id = int(post.get('second_level_id',0))
		model_values = post.get('model_values','')
		if not product_price:
			product_price = -1
		if not limit_clear_price:
			limit_clear_price = -1
		try:
			if has_limit_time == 1:
				product = models.Product.objects.create(
					owner = request.user, 
					product_name = product_name, 
					promotion_title = promotion_title, 
					product_price = product_price,
					clear_price = clear_price,
					product_weight = product_weight,
					product_store = product_store,
					has_limit_time = has_limit_time,
					limit_clear_price = limit_clear_price,
					valid_time_from = valid_time_from,
					valid_time_to = valid_time_to,
					has_product_model = has_product_model,
					catalog_id = second_level_id,
					remark = remark
				)
			else:
				product = models.Product.objects.create(
					owner = request.user, 
					product_name = product_name, 
					promotion_title = promotion_title, 
					product_price = product_price,
					clear_price = clear_price,
					product_weight = product_weight,
					product_store = product_store,
					has_limit_time = has_limit_time,
					limit_clear_price = limit_clear_price,
					has_product_model = has_product_model,
					catalog_id = second_level_id,
					remark = remark
				)

			#获取商品图片
			if images:
				product_images = json.loads(request.POST['images'])
				for product_image in product_images:
					models.ProductImage.objects.create(product=product, image_id=product_image['id'])

			if model_values:
				model_values = json.loads(model_values)
				for model_value in model_values:
					model_Id = model_value.get('modelId',0)
					propertyValues = model_value.get('propertyValues',[])
					price = model_value.get('product_price_'+model_Id,0)#售价
					limit_clear_price = model_value.get('limit_clear_price_'+model_Id,0)#限时结算价
					market_price = model_value.get('clear_price_'+model_Id,0)#结算价
					weight = model_value.get('product_weight_'+model_Id,0)
					stocks = model_value.get('product_store_'+model_Id,0)
					user_code = model_value.get('product_code_'+model_Id,0)
					valid_from = model_value.get('valid_time_from_'+model_Id,None)
					valid_to = model_value.get('valid_time_to_'+model_Id,None)
					product_model = models.ProductModel.objects.create(
						owner = request.user,
						product = product,
						name = model_Id,
						price = price,
						market_price = market_price,
						limit_clear_price = limit_clear_price,
						weight = weight,
						stocks = stocks,
						user_code = user_code,
						valid_time_from = valid_from,
						valid_time_to =valid_to
					)
					if propertyValues:
						list_propery_create = []
						for property_value in propertyValues:
							list_propery_create.append(models.ProductModelHasPropertyValue(
								model = product_model,
								property_id = property_value['propertyId'],
								property_value_id = property_value['id']
							))
						models.ProductModelHasPropertyValue.objects.bulk_create(list_propery_create)
			response = create_response(200)
		except:
			response = create_response(500)
			response.innerErrMsg = unicode_full_stack()
		return response.get_response()

	@login_required
	def api_post(request):
		#更新商品
		post = request.POST
		product_name = post.get('product_name','')
		promotion_title = post.get('promotion_title','')
		product_price = post.get('product_price',-1)
		clear_price = post.get('clear_price',0)
		product_weight = post.get('product_weight',0)
		has_limit_time = int(post.get('has_limit_time',0))
		limit_clear_price = post.get('limit_clear_price',-1)
		valid_time_from = post.get('valid_time_from',None)
		valid_time_to = post.get('valid_time_to',None)
		product_store = post.get('product_store',0)
		product_store_type = int(post.get('product_store_type',-1))
		has_product_model = int(post.get('has_product_model',0))
		model_values = post.get('model_values','')
		# if product_store_type == -1:
		# 	product_store = -1
		if not limit_clear_price:
			limit_clear_price = -1
		if not product_price:
			product_price = -1
		remark = post.get('remark','')
		images = post.get('images','')
		if has_limit_time ==1:
			models.Product.objects.filter(owner=request.user, id=request.POST['id']).update(
				owner = request.user, 
				product_name = product_name, 
				promotion_title = promotion_title, 
				product_price = product_price,
				clear_price = clear_price,
				product_weight = product_weight,
				product_store = product_store,
				has_limit_time = has_limit_time,
				limit_clear_price = limit_clear_price,
				valid_time_from = valid_time_from,
				valid_time_to = valid_time_to,
				has_product_model= has_product_model,
				remark = remark
			)
		else:
			models.Product.objects.filter(owner=request.user, id=request.POST['id']).update(
				owner = request.user, 
				product_name = product_name, 
				promotion_title = promotion_title, 
				product_price = product_price,
				clear_price = clear_price,
				product_weight = product_weight,
				product_store = product_store,
				has_limit_time = has_limit_time,
				limit_clear_price = limit_clear_price,
				valid_time_from = None,
				valid_time_to = None,
				has_product_model= has_product_model,
				remark = remark
			)

		#删除、重建商品图片
		if images:
			product = models.Product.objects.get(owner=request.user, id=request.POST['id'])
			models.ProductImage.objects.filter(product_id=product.id).delete()
			product_images = json.loads(request.POST['images'])
			for product_image in product_images:
				models.ProductImage.objects.create(product=product, image_id=product_image['id'])

		if model_values:
			product_models = models.ProductModel.objects.filter(product_id=request.POST['id'])
			model_ids = [product_model.id for product_model in product_models]
			models.ProductModelHasPropertyValue.objects.filter(model_id__in=model_ids).delete()
			product_models.delete()
			model_values = json.loads(model_values)
			for model_value in model_values:
				model_Id = model_value.get('modelId',0)
				propertyValues = model_value.get('propertyValues',[])
				price = model_value.get('product_price_'+model_Id,0)
				limit_clear_price = model_value.get('limit_clear_price_'+model_Id,0)
				market_price = model_value.get('clear_price_'+model_Id,0)
				weight = model_value.get('product_weight_'+model_Id,0)
				stocks = model_value.get('product_store_'+model_Id,0)
				user_code = model_value.get('product_code_'+model_Id,0)
				valid_from = model_value.get('valid_time_from_'+model_Id,None)
				valid_to = model_value.get('valid_time_to_'+model_Id,None)
				product_model = models.ProductModel.objects.create(
					owner = request.user,
					product_id = int(request.POST['id']),
					name = model_Id,
					price = price,
					market_price = market_price,
					limit_clear_price = limit_clear_price,
					weight = weight,
					stocks = stocks,
					user_code = user_code,
					valid_time_from= valid_from,
					valid_time_to = valid_to
				)
				if propertyValues:
					list_propery_create = []
					for property_value in propertyValues:
						list_propery_create.append(models.ProductModelHasPropertyValue(
							model = product_model,
							property_id = property_value['propertyId'],
							property_value_id = property_value['id']
						))
					models.ProductModelHasPropertyValue.objects.bulk_create(list_propery_create)

		response = create_response(200)
		return response.get_response()

	def api_delete(request):
		user_has_products = len(models.Product.objects.filter(owner_id=request.user.id))
		products = models.Product.objects.filter(owner=request.user, id=request.POST['id'])
		product_ids = [product.id for product in products]
		products.delete()
		models.ProductHasRelationWeapp.objects.filter(product_id__in=product_ids).delete()
		response = create_response(200)
		response.data.user_has_products = user_has_products
		return response.get_response()

