# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth

from core import resource
from core.jsonresponse import create_response
from core import paginator

from util import db_util
from product_catalog import models as catalog_models
from util import string_util

class SecondCategory(resource.Resource):
	app = 'product'
	resource = 'second_category'

	@login_required
	def api_get(request):
		first_id = request.GET.get('first_id',0)
		product_catalogs = catalog_models.ProductCatalog.objects.filter(father_id=first_id)
		second_levels = []
		for product_catalog in product_catalogs:
			second_levels.append({
				'id': product_catalog.id,
				'name': product_catalog.name,
				'father_catalog': product_catalog.father_id
				})

		data = {
			'second_levels': json.dumps(second_levels) if second_levels else [],
			'first_id':first_id
		}

		#构造response
		response = create_response(200)
		response.data = data
		return response.get_response()