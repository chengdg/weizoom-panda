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
from product_catalog import models as catalog_models

import models

#分类配置标签
class CataloLabel(resource.Resource):
	app = 'label'
	resource = 'catalog_label'

	def api_get(request):
		label_properties = models.LabelProperty.objects.filter(is_deleted=False)
		label_values = models.LabelPropertyValue.objects.all()
		
		label_catalogs = []
		label_id2name = {}
		for label_property in label_properties:
			label_catalogs.append({
				'text': label_property.name,
				'value': label_property.id
			})
			label_id2name[label_property.id] = label_property.name

		property_id2name = {}
		value_id2name = {}
		for label_value in label_values:
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

		data = {
			'labelCatalogs': [] if not label_catalogs else json.dumps(label_catalogs),
			'propertyId2name': property_id2name,
			'valueId2name': value_id2name,
			'labelId2name': label_id2name,
			'labelFirstId': -1 if not label_properties else label_properties[0].id
		}
		response = create_response(200)
		response.data = data
		return response.get_response()

	# 保存分类跟标签的对应关系
	def api_put(request):
		select_catalog_labels = request.POST.get('select_catalog_labels', '')
		catalog_id = request.POST.get('catalog_id', -1)
		if select_catalog_labels:
			catalog_models.ProductCatalogHasLabel.objects.filter(catalog_id=catalog_id).delete()
			select_catalog_labels = json.loads(select_catalog_labels)
			
			for select_catalog_label in select_catalog_labels:
				value_ids = []
				select_value_ids = select_catalog_label['valueIds']
				property_id = select_catalog_label['propertyId']
				for value_id in select_value_ids:
					value_ids.append(str(value_id))
			
				catalog_models.ProductCatalogHasLabel.objects.create(
					catalog_id = catalog_id,
					label_ids = ','.join(value_ids),
					property_id = property_id
				)
		response = create_response(200)
		return response.get_response()