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
import models

#分类配置标签
class CatalogHasLabels(resource.Resource):
	app = 'product_catalog'
	resource = 'catalog_has_labels'

	def api_get(request):
		catalog_id = request.GET.get('catalog_id', -1)
		product_catalog_has_labels = models.ProductCatalogHasLabel.objects.filter(catalog_id=catalog_id)
		select_catalog_labels = []
		select_labels = []
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

		label_property_values = label_models.LabelPropertyValue.objects.filter(id__in=select_labels)
		all_label_property_values = label_models.LabelPropertyValue.objects.all()
		if label_property_values:
			label_first_id = label_property_values[0].property_id
		elif all_label_property_values:
			label_first_id = all_label_property_values[0].property_id
		else:
			label_first_id = -1

		data = {
			'labelFirstId': str(label_first_id),
			'selectLabels': select_labels,
			'selectCatalogLabels': [] if not select_catalog_labels else json.dumps(select_catalog_labels)
		}
		response = create_response(200)
		response.data = data
		return response.get_response()