# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack
from eaglet.core import watchdog

from account.models import *
from eaglet.utils.resource_client import Resource
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
from resource.models import Image
import models
from weapp_relation import get_weapp_model_properties, sync_product_label, get_products_limit_info
from account import models as account_models
from product_catalog import models as catalog_models
from label import models as label_models


class SyncProduct(resource.Resource):
	app = 'product'
	resource = 'sync_product'

	@login_required
	def api_post(request):
		product_id = request.POST.get('product_id', 0)
		# print product_id.split(','),"======="
		response = create_response(200)
		data = {}
		try:
			product_ids = product_id.split(',')
			products = models.Product.objects.filter(id__in=product_ids)
			limit_zone_infos = get_products_limit_info(products=products)
			for product in products:
				# 供货商中间关系
				account_has_supplier = account_models.AccountHasSupplier.objects.filter(user_id=product.owner_id).first()
				if not account_has_supplier:
					data['code'] = 500
					response.data = data
					return response.get_response()
				images = get_product_images(product=product)

				# 获取是单品还是多规格
				model_type = 'single' if not product.has_product_model else 'custom'
				weapp_models_info = []
				if product.has_product_model:
					# 多规格,获取规格信息
					weapp_models_info = get_weapp_model_properties(product=product)
				params = organize_params(product=product, supplier_id=account_has_supplier.supplier_id, images=images,
										 model_type=model_type, weapp_models_info=weapp_models_info,
										 limit_zone_infos=limit_zone_infos)

				relation = models.ProductHasRelationWeapp.objects.filter(product_id=product.id).first()
				if not relation:
					sync_add_product(params, product, user_id=request.user.id)
				else:
					params.update({'product_id': relation.weapp_product_id})
					sync_update_product(params, product)
				models.Product.objects.filter(id=product.id).update(
					is_update=False
				)

			data['code'] = 200
			data['count'] = len(product_ids)
		except:
			msg = unicode_full_stack()
			watchdog.error('{}'.format(msg))
			data['code'] = 500
		response.data = data
		return response.get_response()


def get_product_images(product=None):
	"""
	获取该商品的图片
	"""
	product_images = models.ProductImage.objects.filter(product_id=product.id)
	image_ids = [product_image.image_id for product_image in product_images]
	images = Image.objects.filter(id__in=image_ids)
	return [{'order': 1, 'url': image.path} for image in images]


def organize_params(product=None, supplier_id=None, images=None,model_type=None, weapp_models_info=None,
					limit_zone_infos=None):
	if product.limit_zone_type == models.NO_LIMIT:
		limit_zone_type = 'no_limit'
	elif product.limit_zone_type == models.FORBIDDEN_SALE_LIMIT:
		limit_zone_type = 'forbidden'
	else:
		limit_zone_type = 'only'
	# 组织参数

	params = {
		'supplier': supplier_id,
		'name': product.product_name,
		'promotion_title': product.promotion_title if product.promotion_title else '',
		'purchase_price': float(product.clear_price),
		'price': float(product.product_price),
		'weight': product.product_weight,
		'stock_type': 'unbound' if product.product_store == -1 else product.product_store,
		'swipe_images': json.dumps(images),
		'product_id': product.id,
		'model_type': model_type,
		'model_info': json.dumps(weapp_models_info),
		'stocks': product.product_store if product.product_store > 0 else 0,
		'detail': product.remark,
		'limit_zone_type': limit_zone_type,
		'limit_zone': limit_zone_infos.get(product.limit_zone)
	}

	return params


def sync_add_product(params, product, weapp_catalog_id=None, user_id=None):
	"""
	同步新增加商品
	"""
	if product.catalog_id:
		weapp_catalog_id = catalog_models.ProductCatalogRelation.objects\
			.filter(catalog_id=product.catalog_id).first().weapp_catalog_id
	resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put({
		'resource': 'mall.sync_product',
		'data': params
	})
	# 同步到商品中间关系表
	if resp:
		if resp.get('code') == 200 and resp.get('data').get('product'):
			weapp_product_id = resp.get('data').get('product').get('id')
			models.ProductHasRelationWeapp.objects.create(
				product_id=product.id,
				weapp_product_id=weapp_product_id,
				self_user_name=user_id
			)
			# 同步类目
			if weapp_catalog_id:
				catalog_params = {'classification_id': weapp_catalog_id, 'product_id': weapp_product_id}
				resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put({
					'resource': 'mall.classification_product',
					'data': catalog_params
				})
				if not resp or resp.get('code') != 200:
					watchdog.error({'errorMsg': 'Panda product: %s sync catalog failed!' % product.id})
			# 同步标签
			sync_product_label(weapp_product_id=weapp_product_id, product=product)


def sync_update_product(params, product, weapp_catalog_id=None):
	"""
	同步更新商品
	"""
	if product.catalog_id:
		weapp_catalog_id = catalog_models.ProductCatalogRelation.objects\
			.filter(catalog_id=product.catalog_id).first().weapp_catalog_id
	resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post({
		'resource': 'mall.sync_product',
		'data': params
	})
	# 同步到商品中间关系表
	if resp:
		if resp.get('code') == 200:
			# weapp_product_id = resp.get('data').get('product').get('id')
			# print '++++++++++++++++++++++++++++++++++++++++++213'
			# 同步类目
			if weapp_catalog_id:
				catalog_params = {'classification_id': weapp_catalog_id, 'product_id': params.get('product_id')}
				resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post({
					'resource': 'mall.classification_product',
					'data': catalog_params
				})
				if not resp or resp.get('code') == 200:
					watchdog.error({'errorMsg': 'Panda product: %s sync catalog Success!' % product.id})
					print '====================================================================='
				else:
					# catalog_params = {'classification_id': weapp_catalog_id,
					# 				  'product_id': relation.weapp_product_id}
					resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put({
						'resource': 'mall.classification_product',
						'data': catalog_params
					})
					if not resp or resp.get('code') != 200:
						watchdog.error({'errorMsg': 'Panda product: %s sync catalog failed!' % product.id})
			# 更新商品标签
			# 判断商品需不需要同步标签
			sync_product_label(weapp_product_id=params.get('product_id'), product=product, method='POST')
