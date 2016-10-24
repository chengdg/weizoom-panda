# -*- coding: utf-8 -*-
import json

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog

from core import resource
from core.jsonresponse import create_response
import models as product_catalog_models

class GetAllSecondCatalog(resource.Resource):
	app = 'product_catalog'
	resource = 'get_all_second_catalog'

	@login_required
	def api_get(request):
		catalogs = product_catalog_models.ProductCatalog.objects.filter(level=2).order_by('-created_at')
		rows = []
		for catalog in catalogs:
			rows.append({
				'text': catalog.name,
				'value': catalog.id
			})
		data = {
			'rows': rows
		}
		response = create_response(200)
		response.data = data
		return response.get_response()