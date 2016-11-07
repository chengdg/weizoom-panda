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
from django.contrib.auth.models import User
from self_shop.models import SelfShops
from product_catalog.models import ProductCatalogRelation
from product_limit_zone import models as limit_zone_models
from panda.settings import PRODUCT_POOL_OWNER_ID
from product_catalog import models as catalog_models
from label import models as label_models
from util import send_product_message
from util import add_customer_news
from postage_config import models as postage_models


SELF_NAMETEXT2VALUE = {
	u'微众家': 'weizoom_jia',
	u'微众妈妈': 'weizoom_mama' ,
	u'微众学生': 'weizoom_xuesheng',
	u'微众白富美': 'weizoom_baifumei',
	u'微众商城': 'weizoom_shop',
	u'微众俱乐部': 'weizoom_club',
	u'微众Life': 'weizoom_life',
	u'微众一家人': 'weizoom_yjr'
}

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

# # 对应云上通的自营平台账户id(user_id)
# SELF_SHOP2WEAPP_SHOP = {
#	 'weizoom_jia': 3,
#	 'weizoom_mama': 5,
#	 'weizoom_xuesheng': 2,
#	 'weizoom_baifumei': 4,
#	 'weizoom_shop': 6,
#	 'weizoom_club': 7
# }

class WeappRelation(resource.Resource):
	app = 'product'
	resource = 'weapp_relation'

	@login_required
	def api_get(request):
		product_id = request.GET.get('product_id',0)
		product_sync_weapp_account = models.ProductSyncWeappAccount.objects.filter(product_id=product_id)
		product_id2self_user_name = {}
		for product_has_relation in product_sync_weapp_account:
			product_id = product_has_relation.product_id
			self_user_name = product_has_relation.self_user_name
			if product_id not in product_id2self_user_name:
				product_id2self_user_name[product_id] = [self_user_name]
			else:
				product_id2self_user_name[product_id].append(self_user_name)

		self_user_name = [] if product_id not in product_id2self_user_name else product_id2self_user_name[product_id]
		data = {
			'self_user_name': self_user_name
		}

		#构造response
		response = create_response(200)
		response.data = data
		return response.get_response()
	@login_required
	def api_post(request):
		product_data = request.POST.get('product_data',0)
		product_data = '' if not product_data else json.loads(product_data)
		response = create_response(200)
		data = {}
		data['is_error'] = False
		data['error_product_id'] = []
		try:
			if product_data:
				product_ids = product_data[0].get('product_ids')
				product_ids = product_ids.split(',')
				revoke_reasons = product_data[0].get('revoke_reasons')
				product_status = product_data[0].get('product_status')
				# 获取商品要同步到哪个平台
				weizoom_self = product_data[0].get('weizoom_self').split(',')
				weapp_user_ids = [k.weapp_account_id for k in models.SelfUsernameWeappAccount.objects.filter(self_user_name__in=weizoom_self)]
				self_shop_names = [k.self_shop_name for k in SelfShops.objects.filter(weapp_user_id__in=weizoom_self)]
				# 判断是更新还是新曾商品同步
				product_relations = models.ProductHasRelationWeapp.objects.filter(product_id__in=product_ids)
				product_id2relation = {product_relation.product_id:product_relation for product_relation in product_relations}

				# 获取要同步的商品
				products = models.Product.objects.filter(id__in=product_ids)
				product_id2product={product.id:product for product in products}
				product_id2owner_id={product.id:product.owner_id for product in products}
				user_ids= [product.owner_id for product in products]

				# 获取商品图片
				product_images = models.ProductImage.objects.filter(product_id__in=product_ids)
				product_id2image_id = {}
				image_id2paths = {}
				for product in product_images:
					if product.product_id not in product_id2image_id:
						product_id2image_id[product.product_id] = [product.image_id]
					else:
						product_id2image_id[product.product_id].append(product.image_id)
				for image in Image.objects.filter(user_id__in=user_ids):
					image_id2paths[image.id] = image.path

				user_profiles = UserProfile.objects.filter(user_id__in=user_ids)
				account_ids = [user_profile.id for user_profile in user_profiles]
				user_id2account_id = {user_profile.user_id:user_profile.id for user_profile in user_profiles}
				# 获取供货商
				account_has_suppliers = AccountHasSupplier.objects.filter(account_id__in=account_ids)
				user_id2store_name = {account_has_supplier.user_id:account_has_supplier.store_name for account_has_supplier in account_has_suppliers}
				account_id2account_has_supplier = {account_has_supplier.account_id:account_has_supplier for account_has_supplier in account_has_suppliers}
				# 获取商品所属的类目集合
				product_catalog_relations = ProductCatalogRelation.objects.all()
				catalog_id_relations = {}
				[catalog_id_relations.update({relation.catalog_id: relation.weapp_catalog_id})
										for relation in product_catalog_relations]
				# 商品的限制区域数据
				product_limit_zone_info = get_products_limit_info(products=products)
				for product_id in product_ids:
					product_id = int(product_id)
					product = product_id2product[product_id]
					owner_id = product_id2owner_id[product_id]
					account_id = user_id2account_id[int(owner_id)]
					account_has_supplier = account_id2account_has_supplier[int(account_id)]
					weapp_catalog_id = catalog_id_relations.get(product.catalog_id, None)
					return_data = sync_products(request,product_id,product,weizoom_self,
												weapp_user_ids,account_has_supplier,product_id2image_id,
												image_id2paths,product_id2relation, weapp_catalog_id,
												product_limit_zone_info=product_limit_zone_info)
					if return_data['is_error'] == True:
						data['is_error'] = True
						data['error_product_id'].append(str(return_data['error_product_id']))
					try:
						# 发送同步消息给客户档案系统
						owner_id = product.owner_id;
						customer_id = UserProfile.objects.get(user_id=owner_id).corpid
						customer_name = User.objects.get(id=customer_id).username
						add_customer_news.send_sync_product_message(product_name=product.product_name, platforms=self_shop_names, customer_id=customer_id, customer_name=customer_name)
					except:
						msg = unicode_full_stack()
						print '+++++++++++++++++++++++++++++++++++++'
						print msg
						print '+++++++++++++++++++++++++++++++++++++'
				#如果没有选择自营平台,删除表中相关数据
				if not product_data[0].get('weizoom_self'):
					models.ProductSyncWeappAccount.objects.filter(product_id__in=product_ids).delete()

					#商品未同步
					if int(product_status) == 0:
						models.ProductHasRelationWeapp.objects.filter(product_id__in=product_ids).delete()

					#撤销商品原因
					if revoke_reasons:
						for product_id in product_ids:
							models.ProductRevokeLogs.objects.create(product_id=product_id, revoke_reasons=revoke_reasons)
							try:
								# 停售时发送消息给客户档案
								product_id = int(product_id)
								product = product_id2product[product_id]
								owner_id = product.owner_id;
								customer_id = UserProfile.objects.get(user_id=owner_id).corpid
								customer_name = User.objects.get(id=customer_id).username
								add_customer_news.send_stop_sell_product_message(product_name=product.product_name, stop_reason=revoke_reasons, customer_id=customer_id, customer_name=customer_name)
							except Exception as e:
								msg = unicode_full_stack()
								print '+++++++++++++++++++++++++++++++++++++'
								print msg
								print '+++++++++++++++++++++++++++++++++++++'
		except:
			data['is_error'] = True
			msg = unicode_full_stack()
			print '+++++++++++++++++++++++++++++++++++++'
			print msg
			print '+++++++++++++++++++++++++++++++++++++'
			response.innerErrMsg = msg

		if data['is_error'] == False:
			data['code'] = 200
			data['errMsg'] = u'同步成功'
		else:
			data['code'] = 500
			data['errMsg'] = ','.join(data['error_product_id'])+'同步失败'
		#构造response
		response.data = data
		return response.get_response()

	@login_required
	def api_delete(request):
		product_id = request.POST.get('product_id','')
		self_names = request.POST.get('self_names','')
		if product_id and self_names:
			self_names = self_names.split(',')
			models.ProductSyncWeappAccount.objects.filter(product_id=int(product_id),self_user_name__in=self_names).delete()
		response = create_response(200)
		return response.get_response()

def get_weapp_model_properties(product=None):
	"""
	获取多规格的商品,对应的云上通的规格组合信息
	"""
	weapp_models_info = []
	models_info = models.ProductModel.objects.filter(product_id=product.id,
													 is_deleted=False)
	# print '=========================================', product
	for model_info in models_info:
		name = model_info.name
		single_model_properties = name.split('_')
		weapp_model_properties = []
		for single_model_property in single_model_properties:
			temp_list = single_model_property.split(':')
			model_property_id = temp_list[0]
			relation = models.ProductModelPropertyRelation. \
				objects.filter(model_property_id=model_property_id).first()
			value_relation = models.ProductModelPropertyValueRelation.objects \
				.filter(property_value_id=temp_list[1]).first()
			if not relation or not value_relation:
				continue
			weapp_property_id = relation.weapp_property_id
			weapp_property_value_id = value_relation.weapp_property_value_id
			weapp_model_properties.append(str(weapp_property_id) + ':' + str(weapp_property_value_id))
		# 组织传递给zeus的数据
		temp_model_info = {}
		temp_model_info.update({'name': '_'.join(weapp_model_properties),
								'purchase_price': model_info.market_price,
								'price': model_info.price,
								'stock_type': 'limit',
								'panda_model_info_id': model_info.id,
								'stocks': model_info.stocks,
								'weight': model_info.weight,
								'is_deleted': model_info.is_deleted,
								'is_standard': False})
		weapp_models_info.append(temp_model_info)
	return weapp_models_info


def sync_products(request,product_id,product,weizoom_self,weapp_user_ids,
				  account_has_supplier,product_id2image_id,image_id2paths,
				  product_id2relation, weapp_catalog_id, product_limit_zone_info=None):
	data = {}
	data['is_error'] = False
	try:
		if account_has_supplier:
			weapp_supplier_id = account_has_supplier.supplier_id
			# 获取商品图片
			images = []
			image_ids = product_id2image_id[product_id]
			for i_id in image_ids:
				if i_id in image_id2paths:
					images.append({
						"order": 1,
						"url": image_id2paths[i_id]
					})

			# 获取是单品还是多规格
			model_type = 'single' if not product.has_product_model else 'custom'
			weapp_models_info = []
			if product.has_product_model:
				# 多规格,获取规格信息
				weapp_models_info = get_weapp_model_properties(product=product)
			if product.limit_zone_type == models.NO_LIMIT:
				limit_zone_type = 'no_limit'
			elif product.limit_zone_type == models.FORBIDDEN_SALE_LIMIT:
				limit_zone_type = 'forbidden'
			else:
				limit_zone_type = 'only'

			if product.has_same_postage:
				#{0:统一运费,1:默认模板运费}
				postage_money = product.postage_money
				postage_type = 'custom_postage_type'
				relation = postage_models.PostageConfigRelation.objects.filter(postage_config_id=product.postage_id)\
					.first()
				if relation:
					postage_id = relation.weapp_config_relation_id
				else:
					postage_id = 0
			else:
				postage_type = 'unified_postage_type'
				postage_id = -1
				postage_money = product.postage_money
			params = {
				'supplier': weapp_supplier_id,
				'name': product.product_name,
				'promotion_title': product.promotion_title if product.promotion_title else '',
				'purchase_price': float(product.clear_price),
				'price': float(product.product_price),
				'weight': product.product_weight,
				'stock_type': 'unbound' if product.product_store == -1 else product.product_store,
				'images': json.dumps(images),
				'product_id': product_id,
				'model_type': model_type,
				'model_info': json.dumps(weapp_models_info),
				'stocks': product.product_store if product.product_store > 0 else 0,
				'detail': product.remark,
				'limit_zone_type': limit_zone_type,
				'limit_zone': product_limit_zone_info.get(product.limit_zone),
				'postage_id': postage_id,
				'postage_type': postage_type,
				'postage_money': str(postage_money)
			}

			# 判断是更新还是新曾商品同步(只处理添加)
			relation = [] if product_id not in product_id2relation else product_id2relation[product_id]
			if not relation:

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
							self_user_name=request.user.username
						)
						# 更新同步到哪个平台了映射关系
						sync_models = [models.ProductSyncWeappAccount(
							product_id=product.id,
							self_user_name=username
						)for username in weizoom_self]
						models.ProductSyncWeappAccount.objects.bulk_create(sync_models)
						# 同步到那些平台
						account_params = {
							'product_id': weapp_product_id,
							'accounts': json.dumps(weapp_user_ids)
						}
						account_resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put({
							'resource': 'mall.product_pool',
							'data': account_params
						})
						if not account_resp or not account_resp.get('code') == 200:
							watchdog.error({'errorMsg': 'Panda product: %s sync account failed!' % product_id})
						# 同步类目
						if weapp_catalog_id:
							catalog_params = {'classification_id': weapp_catalog_id,
											  'product_id': weapp_product_id}
							resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put({
								'resource': 'mall.classification_product',
								'data': catalog_params
							})
							if not resp or resp.get('code') != 200:
								watchdog.error({'errorMsg': 'Panda product: %s sync catalog failed!' % product_id})
						# 同步标签
						sync_product_label(product=product, weapp_product_id=weapp_product_id)
						# 发送同步信息
						try:
							send_product_message.send_sync_product_message(product=product, user_id=request.user.id,
																		   image_paths=images[0].get('path'))
						except:
							msg = unicode_full_stack()
							watchdog.error('send_sync_product_message:weapp_relation{}'.format(msg))
				else:
					data['is_error'] = True
					data['error_product_id'] = product_id

			else:
				account_params = {
					'product_id': relation.weapp_product_id,
					'accounts': json.dumps(weapp_user_ids)
				}
				account_resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post({
					'resource': 'mall.product_pool',
					'data': account_params
				})
				if not account_resp or not account_resp.get('code') == 200:
					watchdog.error({'errorMsg': 'Panda product: %s sync catalog failed!' % product_id})
				else:
					models.ProductSyncWeappAccount.objects.filter(product_id=product_id).delete()
					sync_models = [models.ProductSyncWeappAccount(
						product_id=product.id,
						self_user_name=username
					) for username in weizoom_self]
					models.ProductSyncWeappAccount.objects.bulk_create(sync_models)
					# 更新商品平台信息
					try:
						send_product_message.send_sync_weapp_account_change(product_id=product_id)
					except:
						msg = unicode_full_stack()
						watchdog.error(u'send_sync_weapp_account_change:weapp_relation:{}'.format(msg))
						print msg
	except:
		data['is_error'] = True
		data['error_product_id'] = product_id
	return data


def get_products_limit_info(products=None):
	if products:
		limit_zone_ids = [p.limit_zone for p in products]
		limit_zone_infos = limit_zone_models.ProductLimitZoneTemplateRelation.objects.filter(template_id__in=limit_zone_ids)
		return {limit_zone.template_id: limit_zone.weapp_template_id for limit_zone in limit_zone_infos}



def sync_product_label(weapp_product_id=None, product=None, method='PUT'):
	"""

	"""

	# 同步标签
	product_labels = models.ProductHasLabel.objects.filter(product_id=product.id)
	label_params = {}
	if product_labels.count() == 0:
		# 需要商品的类目下的标签
		product_catalog_id = product.catalog_id
		catalog_relation = catalog_models.ProductCatalogRelation.objects.filter(catalog_id=product_catalog_id) \
			.last()
		catalog_labels = catalog_models.ProductCatalogHasLabel.objects.filter(catalog_id=product_catalog_id)
		catalog_label_ids = []
		for catalog_label in catalog_labels:
			catalog_label_ids += catalog_label.label_ids.split(',')
		label_relations = label_models.LabelGroupValueRelation.objects.filter(label_value_id__in=catalog_label_ids)
		# label_params.update({'label_ids': label_ids})
		label_ids = [relation.weapp_label_value_id for relation in label_relations]
		label_params.update({'classification_id': catalog_relation.weapp_catalog_id})
		# print 'fucking >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>的>>>>>>.'
		# print label_ids
		# print 'fucking >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.'
	else:
		product_labels = product_labels.exclude(property_id=-1)

		label_ids = []
		for product_label in product_labels:
			label_ids += product_label.label_ids.split(',')
		# print 'fucking >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.'
		# print label_ids
		# print 'fucking >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.'
		label_relations = label_models.LabelGroupValueRelation.objects.filter(
			label_value_id__in=label_ids)
		label_ids = [relation.weapp_label_value_id for relation in label_relations]
	label_params.update({'label_ids': json.dumps(label_ids),
						 'product_id': weapp_product_id,
						 'owner_id': PRODUCT_POOL_OWNER_ID })
	# label_params.update({'product_id': weapp_product_id})
	if method == 'PUT':
		resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put({
			'resource': 'mall.product_has_label',
			'data': label_params
		})
	else:
		resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post({
			'resource': 'mall.product_has_label',
			'data': label_params
		})
