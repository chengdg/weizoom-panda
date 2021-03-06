# -*- coding: utf-8 -*-
import json


from core import resource
from core.jsonresponse import create_response

from product_catalog import models as catalog_models
from product import models as product_models

import models
from util import sync_util
from panda.settings import PRODUCT_POOL_OWNER_ID


#分类配置标签
class CataloLabel(resource.Resource):
	app = 'label'
	resource = 'catalog_label'

	def api_get(request):
		label_groups = models.LabelGroup.objects.filter(is_deleted=False)
		label_group_values = models.LabelGroupValue.objects.filter(is_deleted=False)

		label_catalogs = []
		label_id2name = {}
		for label_property in label_groups:
			label_catalogs.append({
				'text': label_property.name,
				'value': label_property.id
			})
			label_id2name[label_property.id] = label_property.name

		property_id2name = {}
		value_id2name = {}
		for label_value in label_group_values:
			if label_value.property_id not in property_id2name:
				property_id2name[label_value.property_id] = [{
					'name': label_value.name,
					'property_id': label_value.property_id,
					'value_id': label_value.id
				}]
			else:
				property_id2name[label_value.property_id].append({
					'name': label_value.name,
					'property_id': label_value.property_id,
					'value_id': label_value.id
				})

			value_id2name[label_value.id] = label_value.name

		if not label_catalogs:
			label_catalogs = [{
				'text': u'暂无分类',
				'value': -1
			}]

		data = {
			'labelCatalogs': json.dumps(label_catalogs),
			'propertyId2name': property_id2name,
			'valueId2name': value_id2name,
			'labelId2name': label_id2name,
			'labelFirstId': -1 if not label_groups else label_groups[0].id
		}
		response = create_response(200)
		response.data = data
		return response.get_response()

	def api_put(request):
		"""
		保存分类跟标签的对应关系
		"""
		select_catalog_labels = request.POST.get('select_catalog_labels', '')
		catalog_id = request.POST.get('catalog_id', -1)
		product_id = int(request.POST.get('product_id', -1))
		select_catalog_labels = json.loads(select_catalog_labels)

		if len(select_catalog_labels)>0:		
			catalog_label_create = []
			product_label_create = []
			label_ids = []

			for select_catalog_label in select_catalog_labels:
				value_ids = []
				select_value_ids = select_catalog_label['valueIds']
				label_ids += select_value_ids
				property_id = select_catalog_label['propertyId']
				for value_id in select_value_ids:
					value_ids.append(str(value_id))

				str_value_ids = ','.join(value_ids)

				#分类配置标签
				catalog_label_create.append(catalog_models.ProductCatalogHasLabel(
					catalog_id = catalog_id,
					label_ids = str_value_ids,
					property_id = property_id
				))

				#商品配置标签
				product_label_create.append(product_models.ProductHasLabel(
					product_id = product_id,
					label_ids = str_value_ids,
					property_id = property_id
				))

			if product_id == -1:
				# 类目下的标签
				catalog_relation = catalog_models.ProductCatalogRelation.objects.filter(catalog_id=catalog_id).first()
				# label_ids = []
				# label_ids = select_catalog_labels[0].get('valueIds')
				label_relations = models.LabelGroupValueRelation.objects.filter(label_value_id__in=label_ids)

				weapp_classification_id = catalog_relation.weapp_catalog_id
				params = {
					'label_ids': json.dumps([relation.weapp_label_value_id for relation in label_relations]),
					'classification_id': weapp_classification_id,
					'owner_id': PRODUCT_POOL_OWNER_ID
				}
				resp, resp_data = sync_util.sync_zeus(params=params, resource='mall.classification_has_label', method='post')
				if resp:
					# 分类关联标签
					catalog_models.ProductCatalogHasLabel.objects.filter(catalog_id=catalog_id).delete()
					catalog_models.ProductCatalogHasLabel.objects.bulk_create(catalog_label_create)
				else:
					response = create_response(500)
					return response.get_response()
			else:
				product_relation = product_models.ProductHasRelationWeapp.objects.filter(product_id=product_id).first()
				if product_relation:
					weapp_product_id = product_relation.weapp_product_id

					# label_ids = select_catalog_labels[0].get('valueIds')
					label_relations = models.LabelGroupValueRelation.objects.filter(label_value_id__in=label_ids)
					params = {
						'product_id': weapp_product_id,
						'owner_id': PRODUCT_POOL_OWNER_ID,
						'label_ids': json.dumps([relation.weapp_label_value_id for relation in label_relations]),
					}
					resp, resp_data = sync_util.sync_zeus(params=params, resource='mall.product_has_label',
														  method='post')
					if resp:
						# 商品关联标签
						product_models.ProductHasLabel.objects.filter(product_id=product_id).delete()
						product_models.ProductHasLabel.objects.bulk_create(product_label_create)
						print product_label_create, select_catalog_labels
						print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
					else:
						response = create_response(500)
						return response.get_response()
				else:
					product_models.ProductHasLabel.objects.filter(product_id=product_id).delete()
					product_models.ProductHasLabel.objects.bulk_create(product_label_create)
		else:
			if product_id != -1:
				product_models.ProductHasLabel.objects.filter(product_id=product_id).delete()
				product_models.ProductHasLabel.objects.create(
					product_id = product_id,
					label_ids = '',
					property_id = -1
				)
				# 同步到weapp
				product_relation = product_models.ProductHasRelationWeapp.objects.filter(product_id=product_id).first()
				if product_relation:
					weapp_product_id = product_relation.weapp_product_id
					params = {
						'product_id': weapp_product_id,
						'owner_id': PRODUCT_POOL_OWNER_ID,
						'label_ids': '',
					}
					resp, resp_data = sync_util.sync_zeus(params=params, resource='mall.product_has_label',
														  method='post')

			else:
				# 更新类目的标签
				catalog_models.ProductCatalogHasLabel.objects.filter(catalog_id=catalog_id).delete()
				# 同步到weapp
				catalog_relation = catalog_models.ProductCatalogRelation.objects.filter(catalog_id=catalog_id).first()
				if catalog_relation:
					weapp_classification_id = catalog_relation.weapp_catalog_id
					params = {
						'label_ids': '',
						'classification_id': weapp_classification_id,
						'owner_id': PRODUCT_POOL_OWNER_ID
					}
					resp, resp_data = sync_util.sync_zeus(params=params, resource='mall.classification_has_label',
														  method='post')

		response = create_response(200)
		return response.get_response()
