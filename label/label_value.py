# -*- coding: utf-8 -*-

from eaglet.core import watchdog

import models
from core import resource
from core.exceptionutil import unicode_full_stack
from core.jsonresponse import create_response
from panda.settings import PRODUCT_POOL_OWNER_ID
from product import models as product_models
from product_catalog import models as catalog_models
from util import sync_util


#标签内容
class LabelValue(resource.Resource):
	app = 'label'
	resource = 'label_value'

	def api_put(request):
		label_id = request.POST.get('label_id', -1)
		label_value = request.POST.get('label_value', '')
		try:
			if label_id != -1:

				label_group_relation = models.LabelGroupRelation.objects.filter(label_group_id=label_id).first()
				if label_group_relation:
					db_model = models.LabelGroupValue.objects.create(
						property_id=label_id,
						name=label_value
					)
					response = create_response(200)
					params = {
						'name': label_value,
						'owner_id': PRODUCT_POOL_OWNER_ID,
						'product_label_group_id': label_group_relation.weapp_label_group_id
					}
					resp, resp_data = sync_util.sync_zeus(params=params, resource='mall.product_label', method='put')
					if resp and resp_data:
						models.LabelGroupValueRelation.objects.create(label_value_id=db_model.id,
																	  weapp_label_value_id=resp_data.get('label').get('id'))
					else:
						response = create_response(500)
						models.LabelGroupValue.objects.filter(id=db_model.id).update(is_deleted=True)
				else:
					response = create_response(500)
			else:
				response = create_response(500)
		except:
			response = create_response(500)
			msg = unicode_full_stack()
			watchdog.error(msg)
		return response.get_response()

	def api_delete(request):
		label_value_id = request.POST.get('label_value_id',0)
		response = create_response(500)
		try:
			if label_value_id!=0:
				label_group_values = models.LabelGroupValue.objects.filter(id=label_value_id)
				label_group_values.update(is_deleted=True)
				product_has_labels = product_models.ProductHasLabel.objects.filter(property_id=label_group_values[0].property_id, label_ids__icontains=label_value_id)
				product_catalog_has_labels = catalog_models.ProductCatalogHasLabel.objects.filter(property_id=label_group_values[0].property_id, label_ids__icontains=label_value_id)
				
				for product_has_label in product_has_labels:
					label_ids = [str(label_id) for label_id in product_has_label.label_ids.split(',')]
					label_ids.remove(str(label_value_id))
					if label_ids:
						product_models.ProductHasLabel.objects.filter(id=product_has_label.id).update(label_ids = ','.join(label_ids))
					else:
						product_models.ProductHasLabel.objects.filter(id=product_has_label.id).delete()

				for product_catalog_has_label in product_catalog_has_labels:
					label_ids = [str(label_id) for label_id in product_catalog_has_label.label_ids.split(',')]
					label_ids.remove(str(label_value_id))
					if label_ids:
						product_models.ProductCatalogHasLabel.objects.filter(id=product_catalog_has_label.id).update(label_ids = ','.join(label_ids))
					else:
						product_models.ProductCatalogHasLabel.objects.filter(id=product_catalog_has_label.id).delete()
						
				response = create_response(200)
				relation = models.LabelGroupValueRelation.objects.filter(label_value_id=label_value_id).first()
				if relation:
					params = {
						'owner_id': PRODUCT_POOL_OWNER_ID,
						'product_label_id': relation.weapp_label_value_id
					}
					resp, resp_data = sync_util.sync_zeus(params=params, resource='mall.product_label', method='delete')
					if not resp:
						watchdog.error('sync_delete_label_: %s failed' % label_value_id)
					# 将有这个标签的商品的标签去掉
					params = {
						'owner_id': PRODUCT_POOL_OWNER_ID,
						'label_id': relation.weapp_label_value_id
					}
					resp, resp_data = sync_util.sync_zeus(params=params, resource='mall.disable_product_label', method='delete')
					if not resp:
						watchdog.error('sync_disable_product_label: %s failed' % label_value_id)
					# 将有这个标签的类目的标签删掉
					params = {
						'owner_id': PRODUCT_POOL_OWNER_ID,
						'label_id': relation.weapp_label_value_id
					}
					resp, resp_data = sync_util.sync_zeus(params=params, resource='mall.classification_has_label',
														  method='delete')
		except:
			msg = unicode_full_stack()
			response.innerErrMsg = msg
			watchdog.error(msg)
		return response.get_response()