# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth

from core import resource
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack
from core import paginator

from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog

from label import models as label_models
from product import models as product_models
import models

#分类配置标签
class CatalogHasLabels(resource.Resource):
	app = 'product_catalog'
	resource = 'catalog_has_labels'

	def api_get(request):
		catalog_id = request.GET.get('catalog_id', -1)
		product_id = request.GET.get('product_id', -1)

		select_catalog_labels = []
		select_labels = []
		product_select_catalog_labels = []
		product_select_labels = []

		#获取分类配置标签
		product_catalog_has_labels = models.ProductCatalogHasLabel.objects.filter(catalog_id=catalog_id)
		if product_catalog_has_labels:
			for product_catalog_has_label in product_catalog_has_labels:
				value_ids = []
				label_ids = product_catalog_has_label.label_ids.split(',')
				for label_id in label_ids:
					select_labels.append(int(label_id))
					value_ids.append(int(label_id))

				select_catalog_labels.append({
					'propertyId': product_catalog_has_label.property_id,
					'valueIds': value_ids
				})

		#获取商品配置标签,展示商品配置优先
		product_has_labels = product_models.ProductHasLabel.objects.filter(product_id=product_id)
		if product_has_labels:
			for product_has_label in product_has_labels:
				value_ids = []
				label_ids = product_has_label.label_ids.split(',')
				for label_id in label_ids:
					product_select_labels.append(int(label_id))
					value_ids.append(int(label_id))

				product_select_catalog_labels.append({
					'propertyId': product_has_label.property_id,
					'valueIds': value_ids
				})
	
		label_group_values = label_models.LabelGroupValue.objects.filter(id__in=select_labels, is_deleted=False)
		all_label_group_values = label_models.LabelGroupValue.objects.filter(is_deleted=False)
		if product_has_labels:
			label_first_id = product_has_labels[0].property_id
		elif label_group_values:
			label_first_id = label_group_values[0].property_id
		elif all_label_group_values:
			label_first_id = all_label_group_values[0].property_id
		else:
			label_first_id = -1

		if product_id != -1:
			select_catalog_labels = select_catalog_labels if not product_select_catalog_labels else product_select_catalog_labels
			select_labels = select_labels if not product_select_labels else product_select_labels

		data = {
			'labelFirstId': str(label_first_id),
			'selectLabels': select_labels,
			'selectCatalogLabels': [] if not select_catalog_labels else json.dumps(select_catalog_labels)
		}
		response = create_response(200)
		response.data = data
		return response.get_response()