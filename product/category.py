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
from account.models import *
from util import string_util
from panda.settings import ZEUS_HOST

class Category(resource.Resource):
	app = 'product'
	resource = 'category'

	@login_required
	def api_get(request):
		second_level_id = int(request.GET.get('second_level_id',0))
		print second_level_id,"==========ss======="
		company_type = UserProfile.objects.get(user_id=request.user.id).company_type
		if company_type:
			company_type = json.loads(company_type)
		product_catalogs = catalog_models.ProductCatalog.objects.filter(id__in=company_type)
		first_levels = []
		second_levels = []
		if product_catalogs:
			if second_level_id!=0:
				father_catalog_id = catalog_models.ProductCatalog.objects.filter(id=second_level_id)[0].father_id
			else:
				father_catalog_id = product_catalogs[0].id
			#一级分类
			for product_catalog in product_catalogs.filter(father_id=-1):
				if product_catalog.id == father_catalog_id:
					first_levels.append({
						'id': product_catalog.id,
						'name': product_catalog.name,
						'is_choose': 1
						})
				else:
					first_levels.append({
						'id': product_catalog.id,
						'name': product_catalog.name
						})

			#二级分类
			for product_catalog in catalog_models.ProductCatalog.objects.filter(father_id=father_catalog_id):
				if product_catalog.id == second_level_id:
					second_levels.append({
						'id': product_catalog.id,
						'name': product_catalog.name,
						'father_catalog': product_catalog.father_id,
						'is_choose': 1
						})
				else:
					second_levels.append({
						'id': product_catalog.id,
						'name': product_catalog.name,
						'father_catalog': product_catalog.father_id
						})

		data = {
			'first_levels': json.dumps(first_levels) if first_levels else [],
			'second_levels': json.dumps(second_levels) if second_levels else []
		}

		#构造response
		response = create_response(200)
		response.data = data
		return response.get_response()