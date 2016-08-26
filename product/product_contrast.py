# -*- coding: utf-8 -*-
import json
import time
import HTMLParser

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
from eaglet.utils.resource_client import Resource

from account.models import *
from resource import models as resource_models
from product_catalog import models as catalog_models
from product.product_has_model import get_product_model_property_values
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
from weapp_relation import get_weapp_model_properties
import nav
import models

FIRST_NAV = 'product'
SECOND_NAV = 'product-update-list'

class ProductContrast(resource.Resource):
	app = 'product'
	resource = 'product_contrast'

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
			product = models.Product.objects.get(id=product_id)
			product_models = models.ProductModel.objects.filter(product_id=product_id, is_deleted=False)
			product_has_model = 1
			limit_clear_price = ''
			if product.limit_clear_price and product.limit_clear_price != -1:
				limit_clear_price = product.limit_clear_price

			# product_models = models.ProductModel.objects.filter(product_id=product_id,owner=request.user)
			product_model_ids = [product_model.id for product_model in product_models]
			property_values = models.ProductModelHasPropertyValue.objects.filter(model_id__in=product_model_ids)
			
			#获取规格值
			value_ids = set([str(property_value.property_value_id) for property_value in property_values])
			product_model_property_values = models.ProductModelPropertyValue.objects.filter(id__in=value_ids)
			model_values = get_product_model_property_values(product_model_property_values)
			
			#获取商品分类
			product_catalog = catalog_models.ProductCatalog.objects.filter(id=product.catalog_id)
			first_level_name = ''
			second_level_name = ''
			if product_catalog:
				second_level_name = product_catalog[0].name
				first_level_name = catalog_models.ProductCatalog.objects.get(id=product_catalog[0].father_id).name

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
				'catalog_name': '' if not first_level_name else ('%s--%s') %(first_level_name,second_level_name),
				'second_catalog_id': product.catalog_id,
				'value_ids': ','.join(value_ids)
			}
			#组织多规格数据
			for product_model in product_models:
				model_Id = product_model.name
				product_data['product_price_'+model_Id] = '%s' %('%.2f'%product_model.price)
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


			#修改的商品旧数据
			old_product = models.OldProduct.objects.get(product_id=product_id)

			old_product_model_ids = old_product.product_model_ids.split(',')
			old_property_values = models.ProductModelHasPropertyValue.objects.filter(model_id__in=old_product_model_ids, is_deleted=True)
			
			#获取规格值
			old_value_ids = set([str(property_value.property_value_id) for property_value in old_property_values])
			old_product_model_property_values = models.ProductModelPropertyValue.objects.filter(id__in=old_value_ids)
			old_model_values = get_product_model_property_values(old_product_model_property_values)
			print old_model_values,"=======+++++========"
			#获取商品分类
			old_product_catalog = catalog_models.ProductCatalog.objects.filter(id=old_product.catalog_id)
			old_first_level_name = ''
			old_second_level_name = ''
			if old_product_catalog:
				old_second_level_name = old_product_catalog[0].name
				old_first_level_name = catalog_models.ProductCatalog.objects.get(id=old_product_catalog[0].father_id).name

			old_product_data = {
				'old_product_name' : old_product.product_name,
				'old_promotion_title' : old_product.promotion_title,
				'old_product_price' : '%s' % old_product.product_price,
				'old_clear_price' : '%s' % old_product.clear_price,
				'old_product_weight' : old_product.product_weight,
				'old_product_store' : old_product.product_store,
				'old_remark' : '' if not old_product.remark else string_util.raw_html(old_product.remark),
				'old_has_product_model' : '%s' %(1 if old_product.has_product_model else 0),
				'old_models' : json.dumps(old_model_values),
				'old_images' : [] if not old_product.images else json.loads(old_product.images),
				'old_catalog_name' : '' if not old_first_level_name else ('%s--%s') %(old_first_level_name,old_second_level_name),
				'old_second_catalog_id' : old_product.catalog_id,
				'old_value_ids': ','.join(old_value_ids)
			}

			#组织多规格数据
			for product_model in models.ProductModel.objects.filter(id__in=old_product_model_ids):
				model_Id = product_model.name
				old_product_data['old_product_price_'+model_Id] = '%s' %('%.2f'%product_model.price)
				old_product_data['old_limit_clear_price_'+model_Id] = '%s' %product_model.limit_clear_price
				old_product_data['old_clear_price_'+model_Id] = '%s' %product_model.market_price
				old_product_data['old_product_weight_'+model_Id] = '%s' %product_model.weight
				old_product_data['old_product_store_'+model_Id] = '%s' %product_model.stocks
				old_product_data['old_product_code_'+model_Id] = '%s' %product_model.user_code
				old_product_data['old_valid_time_from_'+model_Id] = '%s' %product_model.valid_time_from.strftime("%Y-%m-%d %H:%M") if product_model.valid_time_from else ''
				old_product_data['old_valid_time_to_'+model_Id] = '%s' %product_model.valid_time_to.strftime("%Y-%m-%d %H:%M") if product_model.valid_time_to else ''
			product_data.update(old_product_data)
			# product_data['old_product_name'] = old_product.product_name,
			# product_data['old_promotion_title'] = old_product.promotion_title,
			# product_data['old_product_price'] = '%s' % old_product.product_price if old_product.product_price>0 else '%s' % old_product.clear_price,
			# product_data['old_clear_price'] = '%s' % old_product.clear_price,
			# product_data['old_product_weight'] = '%s'% old_product.product_weight,
			# product_data['old_product_store'] = old_product.product_store,
			# product_data['old_remark'] = string_util.raw_html(old_product.remark),
			# product_data['old_has_product_model'] = '%s' %(1 if old_product.has_product_model else 0),
			# product_data['old_model_values'] = json.dumps(model_values),
			# product_data['old_images'] = [],
			# product_data['old_catalog_name'] = '' if not first_level_name else ('%s--%s') %(first_level_name,second_level_name),
			# product_data['old_old_second_catalog_id'] = old_product.catalog_id,
			# 'old_value_ids': ','.join(value_ids)

			jsons['items'].append(('product', json.dumps(product_data)))
		else:
			jsons['items'].append(('product', json.dumps(None)))
			model_properties = models.ProductModelProperty.objects.filter(owner=request.user)
			property_ids = [model_propertie.id for model_propertie in model_properties]
			property_values = models.ProductModelPropertyValue.objects.filter(property_id__in=property_ids)
			product_has_model = len(property_values)

			product_catalog = catalog_models.ProductCatalog.objects.filter(id=second_level_id)
			first_level_name = ''
			second_level_name = ''
			if product_catalog:
				second_level_name = product_catalog[0].name
				first_level_name = catalog_models.ProductCatalog.objects.get(id=product_catalog[0].father_id).name

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(request),
			'second_nav_name': SECOND_NAV,
			'jsons': jsons,
			'second_level_id': second_level_id,
			'role': role,
			'points': points,
			'purchase_method': purchase_method,
			'product_has_model': product_has_model,
			'catalog_name': '' if not first_level_name else ('%s--%s') %(first_level_name,second_level_name)
		})
		return render_to_response('product/product_contrast.html', c)