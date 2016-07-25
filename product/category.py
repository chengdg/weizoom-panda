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
from resource import models as resource_models
from product_catalog import models as catalog_models
from account.models import *
from util import string_util
from panda.settings import ZEUS_HOST
from product.sales_from_weapp import sales_from_weapp
import nav
import models
import requests

class Category(resource.Resource):
	app = 'product'
	resource = 'category'

	@login_required
	def api_get(request):
		product_catalogs = catalog_models.ProductCatalog.objects.all()
		father_catalog_id = product_catalogs.exclude(father_catalog=-1)[0].father_catalog
		first_levels = []
		for product_catalog in product_catalogs.filter(father_catalog=-1):
			first_levels.append({
				'id': product_catalog.id,
				'name': product_catalog.catalog_name
				})

		second_levels = []
		for product_catalog in product_catalogs.filter(father_catalog=father_catalog_id):
			father_catalog = product_catalog.father_catalog
			second_levels.append({
				'id': product_catalog.id,
				'name': product_catalog.catalog_name,
				'father_catalog': product_catalog.father_catalog
				})

		data = {
			'first_levels': json.dumps(first_levels) if first_levels else [],
			'second_levels': json.dumps(second_levels) if second_levels else []
		}

		#构造response
		response = create_response(200)
		response.data = data
		return response.get_response()