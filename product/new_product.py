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
from eaglet.core.exceptionutil import unicode_full_stack
from util import watchdog

from account.models import *
from resource import models as resource_models
from product_catalog import models as catalog_models
from product.product_has_model import get_product_model_property_values
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
from weapp_relation import get_weapp_model_properties
from services.panda_send_modify_product_ding_talk_service.tasks import send_modify_product_ding_talk
import nav
import models
from product_limit_zone import models as limit_zone_models

FIRST_NAV = 'product'
SECOND_NAV = 'product-list'

SELF_SHOP2TEXT = {
	'weizoom_jia': u'微众家',
	'weizoom_mama': u'微众妈妈',
	'weizoom_xuesheng': u'微众学生',
	'weizoom_baifumei': u'微众白富美',
	'weizoom_shop': u'微众商城',
	'weizoom_club': u'微众俱乐部',
	'weizoom_life': u'微众Life',
	'weizoom_yjr': u'微众一家人',
	'weizoom_fulilaile': u'惠惠来啦',
	'weizoom_juweihui': u'居委汇',
	'weizoom_zhonghai': u'微众中海',
	'weizoom_zoomjulebu': u'微众club',
	'weizoom_chh': u'微众吃货',
	'weizoom_pengyouquan': u'微众圈',
	'weizoom_shxd': u'少先队',
	'weizoom_jinmeihui': u'津美汇',
	'weizoom_wzbld': u'微众便利店',
	'weizoom_jiaren': u'微众佳人',
	'weizoom_xiaoyuan': u'微众良乡商城',
	'weizoom_jy': u'微众精英',
	'devceshi': u'开发测试',
	'caiwuceshi': u'财务测试'
}

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
		# 获取所有的限制
		limit_zones = limit_zone_models.ProductLimitZoneTemplate.objects.filter(is_deleted=False,
																				owner_id=request.user.id)
		limit_zone_info = [dict(text=limit_zone.name,
								value=limit_zone.id) for limit_zone in limit_zones]
		if product_id:
			if role == YUN_YING:
				product = models.Product.objects.get(id=product_id)
				product_models = models.ProductModel.objects.filter(product_id=product_id, is_deleted=False)
				product_has_model = 1
			else:
				model_properties = models.ProductModelProperty.objects.filter(owner=request.user)
				property_ids = [model_propertie.id for model_propertie in model_properties]
				property_values = models.ProductModelPropertyValue.objects.filter(property_id__in=property_ids)
				product_has_model = len(property_values)
				product = models.Product.objects.get(owner=request.user, id=product_id)
				product_models = models.ProductModel.objects.filter(product_id=product_id, owner=request.user, is_deleted=False)
			limit_clear_price = ''
			if product.limit_clear_price and product.limit_clear_price != -1:
				limit_clear_price = product.limit_clear_price

			# product_models = models.ProductModel.objects.filter(product_id=product_id,owner=request.user)
			product_model_ids = [product_model.id for product_model in product_models]
			property_values = models.ProductModelHasPropertyValue.objects.filter(model_id__in=product_model_ids, is_deleted=False)
			
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
				'old_second_catalog_id': product.catalog_id,
				'value_ids': ','.join(value_ids),
				'limit_zone_type': product.limit_zone_type,
				'limit_zone_id': product.limit_zone,

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
		limit_zone_info.append(
			{'text': '请选择区域',
			 'value': 0}
		)
		jsons['items'].append(('limit_zone_info', json.dumps(limit_zone_info)))
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(request),
			'second_nav_name': SECOND_NAV if role==CUSTOMER else 'product-relation-list',#为了兼容运营查看商品详情页
			'jsons': jsons,
			'second_level_id': second_level_id,
			'role': role,
			'points': points,
			'purchase_method': purchase_method,
			'product_has_model': product_has_model,
			'catalog_name': '' if not first_level_name else ('%s--%s') %(first_level_name,second_level_name)
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
		# valid_time_from = post.get('valid_time_from','')
		# valid_time_to = post.get('valid_time_to','')
		remark = post.get('remark','')
		images = post.get('images','')
		has_product_model = int(post.get('has_product_model',0))
		second_level_id = int(post.get('second_level_id',0))
		model_values = post.get('model_values','')
		limit_zone_type = post.get('limit_zone_type', 0)
		limit_zone_id = post.get('limit_zone_id', 0)

		parser = HTMLParser.HTMLParser()
		if remark:
			remark = parser.unescape(remark)
		if not product_price:
			product_price = -1
		if not limit_clear_price:
			limit_clear_price = -1
		try:

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
				remark = remark,
				limit_zone_type=limit_zone_type,
				limit_zone=limit_zone_id,
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

			try:
				UserProfile.objects.filter(user=request.user).update(product_count=F('product_count') + 1)
			except :
				message = u"修改帐号商品数异常：{}".format(unicode_full_stack())
				watchdog.watchdog_error(message)
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
		second_level_id = int(post.get('second_level_id',0))
		limit_zone_type = post.get('limit_zone_type', 0)
		limit_zone_id = post.get('limit_zone_id', 0)
		print '======================================='
		print post
		print limit_zone_id, limit_zone_type
		print '======================================='
		# if product_store_type == -1:
		# 	product_store = -1
		if not limit_clear_price:
			limit_clear_price = -1
		if not product_price:
			product_price = -1
		remark = post.get('remark','')
		images = post.get('images','')
		parser = HTMLParser.HTMLParser()
		if remark:
			remark = parser.unescape(remark)

		modify_contents = []
		catalog_id = models.Product.objects.get(owner=request.user, id=request.POST['id']).catalog_id
		product_sync_weapp_accounts = models.ProductSyncWeappAccount.objects.filter(product_id=request.POST['id'])
		#判断商品是否同步
		if product_sync_weapp_accounts:
			product = models.Product.objects.get(owner=request.user, id=request.POST['id'])
			old_product_name = product.product_name
			old_promotion_title = product.promotion_title
			old_product_price = '%.2f' %product.product_price
			old_clear_price = '%.2f' %product.clear_price
			old_product_weight = str(product.product_weight)
			old_product_store = int(product.product_store)
			old_remark = product.remark
			old_has_product_model = product.has_product_model
			old_catalog_id = int(product.catalog_id)

			# models.OldProduct.objects.filter(product_id = product.id).delete()
			models.OldProduct.objects.create(product_id = product.id)
			#获取图片
			image_ids = [product_img.image_id for product_img in models.ProductImage.objects.filter(product_id=product.id)]
			old_images = []
			new_images = json.loads(request.POST['images'])
			for image in resource_models.Image.objects.filter(id__in=image_ids):
				old_images.append({
					'id': image.id,
					'path': image.path
				})

			#获取规格值
			old_product_models = models.ProductModel.objects.filter(product_id=product.id, is_deleted=False)
			old_product_model_ids = [str(old_product_model.id) for old_product_model in old_product_models]
			#保存修改之前的数据
			last_old_products = models.OldProduct.objects.filter(product_id=product.id).order_by('-id')[0]
			old_products = models.OldProduct.objects.filter(id=last_old_products.id)
			if old_images != new_images:
				old_products.update(
					images = json.dumps(old_images)
				)
				modify_contents.append(u'商品图片')
			if old_product_name != product_name:
				old_products.update(
					product_name = old_product_name
				)
				modify_contents.append(u'商品名称')
			if old_promotion_title != promotion_title:
				old_products.update(
					promotion_title = old_promotion_title
				)
				modify_contents.append(u'促销标题')
			if has_product_model == 0:
				if product_price and (old_product_price != product_price):
					old_products.update(
						product_price = old_product_price
					)
					modify_contents.append(u'商品售价')
				if clear_price and (old_clear_price != clear_price):
					old_products.update(
						clear_price = old_clear_price
					)
					modify_contents.append(u'结算价')
				if product_weight and (old_product_weight != product_weight):
					old_products.update(
						product_weight = old_product_weight
					)
					modify_contents.append(u'商品重量')
				if product_store and (old_product_store != int(product_store)):
					old_products.update(
						product_store = old_product_store
					)
					if int(product_store)>int(old_product_store):
						modify_contents.append(u'库存数量(增加)')
					else:
						modify_contents.append(u'库存数量(减少)')
			if old_remark != remark:
				old_products.update(
					remark = old_remark
				)
				modify_contents.append(u'商品描述')
			if old_has_product_model != has_product_model:
				old_products.update(
					has_product_model = old_has_product_model
				)
			if old_catalog_id != second_level_id:
				old_products.update(
					catalog_id = old_catalog_id
				)
				modify_contents.append(u'商品类目')

		source_product = models.Product.objects.filter(owner=request.user, id=request.POST['id']).first()

		models.Product.objects.filter(owner=request.user, id=request.POST['id']).update(
			owner = request.user,
			product_name = product_name,
			promotion_title = promotion_title,
			has_limit_time = has_limit_time,
			limit_clear_price = limit_clear_price,
			valid_time_from = None,
			valid_time_to = None,
			has_product_model= has_product_model,
			catalog_id = second_level_id,
			remark = remark,
			limit_zone=limit_zone_id,
			limit_zone_type=limit_zone_type
		)

		if has_product_model == 0:
			models.Product.objects.filter(owner=request.user, id=request.POST['id']).update(
				product_price = product_price,
				clear_price = clear_price,
				product_weight = product_weight,
				product_store = product_store
			)

		if product_sync_weapp_accounts:
			models.Product.objects.filter(owner=request.user, id=request.POST['id']).update(
				is_update = True,
				is_refused = False
			)

		if int(catalog_id) != second_level_id:
			models.ProductHasLabel.objects.filter(product_id=request.POST['id']).delete()
		#删除、重建商品图片
		if images:
			product = models.Product.objects.get(owner=request.user, id=request.POST['id'])
			models.ProductImage.objects.filter(product_id=product.id).delete()
			product_images = json.loads(request.POST['images'])
			for product_image in product_images:
				models.ProductImage.objects.create(product=product, image_id=product_image['id'])
		old_properties = []
		new_properties = []
		new_product_model_ids = []
		if model_values:
			product_models = models.ProductModel.objects.filter(product_id=request.POST['id'], is_deleted=False)
			# 故意这么写的
			old_properties = [product_model for product_model in product_models]
			model_ids = [product_p.id for product_p in product_models]
			models.ProductModelHasPropertyValue.objects.filter(model_id__in=model_ids).update(is_deleted=True)
			product_models.update(is_deleted=True)
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
				new_product_model_ids.append(str(product_model.id))
				new_properties.append(product_model)
				if propertyValues:
					list_propery_create = []
					for property_value in propertyValues:
						list_propery_create.append(models.ProductModelHasPropertyValue(
							model = product_model,
							property_id = property_value['propertyId'],
							property_value_id = property_value['id']
						))
					models.ProductModelHasPropertyValue.objects.bulk_create(list_propery_create)
		sync_weapp_product_store(product_id=int(request.POST['id']), owner_id=request.user.id,
								 source_product=source_product,
								 new_properties=new_properties, old_properties=old_properties)

		if product_sync_weapp_accounts and (old_has_product_model == has_product_model ==1):
			if sorted(old_product_model_ids) != sorted(new_product_model_ids):
				old_products.update(
					product_model_ids = ','.join(set(old_product_model_ids))
				)

		if product_sync_weapp_accounts:
			if (old_has_product_model != has_product_model) or ((old_has_product_model == has_product_model ==1) and (sorted(old_product_model_ids) != sorted(new_product_model_ids))):
				modify_contents.append(u'商品规格')

		#发送钉钉消息
		user_profile = UserProfile.objects.get(user_id=request.user.id)
		
		if product_sync_weapp_accounts and len(modify_contents)>0:
			product_status = u'待同步更新'
			#获取已同步自营平台	
			shop_names = []
			for product_sync_weapp in product_sync_weapp_accounts:
				self_user_name = product_sync_weapp.self_user_name
				if self_user_name in SELF_SHOP2TEXT:
					shop_names.append(SELF_SHOP2TEXT[self_user_name])
			# 组织格式,两个换行
			if len(shop_names)>2:
				for i in range(2,len(shop_names),2):
					shop_names[i] = '\n'+ shop_names[i]

			if len(modify_contents)==1 and (modify_contents[0]==u'库存数量(增加)' or modify_contents[0]==u'库存数量(减少)'):
				product_status = u'已自动更新'

			show_product_name = u"商品名称: " + '%s'%product_name + "\n"
			show_customer_name = u"商家名称: " + user_profile.name + "\n"
			show_modify_contents = u"修改内容 :" + u'、'.join(modify_contents) + "\n"
			show_shop_names = u"涉及平台 :" + u'、'.join(shop_names) + "\n"
			show_product_status = u"状态: " + product_status + "\n"
			message = ('%s%s%s%s%s')%(show_product_name,show_customer_name,show_modify_contents,show_shop_names,show_product_status)
			send_modify_product_ding_talk(message,request.POST['id'])

		response = create_response(200)
		return response.get_response()

	def api_delete(request):
		if models.Product.objects.filter(id=request.POST['id']).count():
			products = models.Product.objects.filter(id=request.POST['id']).update(is_deleted=True)
			models.ProductHasRelationWeapp.objects.filter(product_id__in=request.POST['id']).delete()
			try:
				product = models.Product.objects.get(id=request.POST['id'])
				UserProfile.objects.filter(user=product.owner).update(product_count=F('product_count') - 1)
				sync_deleted_product(product=product)
				# print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..'
			except :
				message = u"api_delete修改帐号商品数异常：{}".format(unicode_full_stack())
				watchdog.watchdog_error(message)
		response = create_response(200)
		return response.get_response()


def sync_weapp_product_store(product_id=None, owner_id=None, source_product=None,
							 new_properties=None, old_properties=None):
	"""
	判断商品是否需要同步并同步
	"""
	# 如果降价（售价，结算价）库存修改自动更新。
	new_product = models.Product.objects.filter(owner=owner_id, id=product_id).first()

	relation = models.ProductHasRelationWeapp.objects.filter(product_id=product_id).first()
	if new_product.has_product_model != source_product.has_product_model:
		return False
	#  未同步的不处理
	if relation:
		if new_product.has_product_model:
			# 多规格,获取规格信息
			model_type = 'custom'
			if not charge_models_product_sync(old_properties=old_properties, new_properties=new_properties):
				return False
			weapp_models_info = get_weapp_model_properties(product=source_product)
		else:
			model_type = 'single'
			if new_product.product_store == source_product.product_store:
				return False
			weapp_models_info = [{'name': 'standard',
								  'product_store': new_product.product_store}]

		params = {
			'model_type': model_type,
			'model_info': json.dumps(weapp_models_info),
			'product_id': relation.weapp_product_id

		}
		resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post({
			'resource': 'panda.product_store',
			'data': params
		})
		if resp and resp.get('code') == 200:
			pass
			# 先删除数据
			# models.ProductSyncWeappAccount.objects.filter(product_id=source_product.id, ).delete()
			# sync_models = [models.ProductSyncWeappAccount(product_id=source_product.id,
			# 											  self_user_name=username)
			# 			   for username in weizoom_self]
			# models.ProductSyncWeappAccount.objects.bulk_create(sync_models)
			# data['code'] = 200
			# data['errMsg'] = u'关联成功'


def charge_models_product_sync(old_properties=None, new_properties=None):
	"""
	判断多规格商品是否要同步
	"""
	new_properties_dict = {}
	new_properties_names = []
	for new_property in new_properties:
		new_properties_dict.update({new_property.name: new_property})
		new_properties_names.append(new_property.name)

	old_properties_dict = {}
	old_properties_name = []
	for old_property in old_properties:
		old_properties_dict.update({old_property.name: old_property})
		old_properties_name.append(old_property.name)

	# 只要有删除的规格就不同步
	if len(new_properties_names) != len(old_properties_name):
		return False
	if len(list(set(old_properties_name) - set(new_properties_names))) > 0:
		return False

	# 有新规格不同步
	if len(list(set(new_properties_names) - set(old_properties_name))) > 0:
		return False

	return True


# from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST

def sync_deleted_product(product):
	"""

	同步删除商品
	"""
	if product:
		relation = models.ProductHasRelationWeapp.objects.filter(product_id=product.id).first()
		if not relation:
			return
		weapp_product_id = relation.weapp_product_id
		params = {
			'weapp_product_id': weapp_product_id
		}
		resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).delete({
			'resource': 'mall.sync_product',
			'data': params
		})
		if not resp or not resp.get('code') != 200:
			watchdog.watchdog_warning('sync_deleted_product failed! procuct_id: {}'.format(product.id))
