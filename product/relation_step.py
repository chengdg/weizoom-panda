# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from core import resource
from core.jsonresponse import create_response
from core import paginator
from core.exceptionutil import unicode_full_stack

from util import db_util
from resource import models as resource_models
from account.models import *
from util import string_util
import nav
import models

class RelationStep(resource.Resource):
	app = 'product'
	resource = 'relation_step'

	@login_required
	def api_put(request):
		product_id = request.POST.get('product_id',0)
		weapps = request.POST.get('weapps','')
		product_relations = models.ProductRelation.objects.all()
		if weapps:
			models.ProductHasRelationWeapp.objects.filter(product_id=product_id).delete()
			self_first_name2self_user_name = {}
			for product in product_relations:
				self_first_name2self_user_name[product.self_first_name] = product.self_user_name
			for weapp in json.loads(weapps):
				list_create = []
				for (weapp_name,weapp_id) in weapp.items():
					list_create.append(models.ProductHasRelationWeapp(
						product_id = product_id,
						self_user_name = self_first_name2self_user_name[weapp_name],
						weapp_product_id = weapp_id
					))
				models.ProductHasRelationWeapp.objects.bulk_create(list_create)
		else:
			models.ProductHasRelationWeapp.objects.filter(product_id=product_id).delete()
			models.ProductHasRelationWeapp.objects.create(
				product_id = product_id,
				weapp_product_id= '',
				self_user_name = ''
			)
		response = create_response(200)
		return response.get_response()