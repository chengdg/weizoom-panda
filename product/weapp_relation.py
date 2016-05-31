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

class ProductRelation(resource.Resource):
	app = 'product'
	resource = 'weapp_relation'

	@login_required
	def api_get(request):
		product_id = request.GET.get('product_id',0)
		product_relations = models.ProductHasRelationWeapp.objects.filter(product_id=product_id)
		#组装数据
		relations = {}
		if product_relations:
			for product in product_relations:
				relations[product.self_user_name] = product.weapp_product_id
		data = {
			'rows': relations
		}
		#构造response
		response = create_response(200)
		response.data = data
		return response.get_response()

	@login_required
	def api_put(request):
		post = request.POST
		relations = post.get('relations','')
		product_id = post.get('product_id','')
		try:
			if relations:
				print json.loads(relations),"=========="
				models.ProductHasRelationWeapp.objects.filter(product_id=product_id).delete()
				relations=json.loads(relations)
				list_create = []
				for (k,v) in relations[0].items():
					list_create.append(models.ProductHasRelationWeapp(
						product_id = product_id,
						self_user_name = k,
						weapp_product_id = v
					))
				models.ProductHasRelationWeapp.objects.bulk_create(list_create)
			response = create_response(200)
			response.data.code = 200
			response.data.Msg = u'关联成功'
		except:
			response = create_response(500)
			response.data.code = 500
			response.innerErrMsg = unicode_full_stack()
			response.data.Msg = u'关联失败'
		return response.get_response()