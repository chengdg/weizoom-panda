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

class GetAllFirstCatalog(resource.Resource):
	app = 'product_catalog'
	resource = 'get_all_first_catalog'

	@login_required
	def api_get(request):
		is_account_page = request.GET.get('is_account_page','')
		catalogs = product_catalog_models.ProductCatalog.objects.filter(father_id=-1).order_by('-created_at')
		if is_account_page:
			rows = []
		else:
			rows = [{
				'text': u'无',
				'value': -1
			}]
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