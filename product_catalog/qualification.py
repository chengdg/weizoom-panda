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

#配置特殊资质
class GetAllFirstCatalog(resource.Resource):
	app = 'product_catalog'
	resource = 'qualification'

	@login_required
	def api_put(request):
		# 新建/编辑特殊资质
		post = request.POST
		qualification_infos = json.loads(post.get('qualification_infos',''))
		catalog_id = int(post.get('catalog_id'))
		old_ids = [int(catalog.id) for catalog in product_catalog_models.ProductCatalogQualification.objects.filter(catalog_id=catalog_id)]
		new_ids = []
		need_del_ids = []

		#循环第一次，得到编辑后被删除的特殊资质id
		for qualification_info in qualification_infos:
			if qualification_info.has_key('id'):
				new_ids.append(qualification_info['id'])
		for old_id in old_ids:
			if old_id not in new_ids:
				need_del_ids.append(old_id)
		product_catalog_models.ProductCatalogQualification.objects.filter(id__in=need_del_ids).delete()

		# 循环第二次，更新需要修改的特殊资质信息
		for qualification_info in qualification_infos:
			if qualification_info.has_key('id'):
				#编辑分类
				product_catalog_models.ProductCatalogQualification.objects.filter(id=qualification_info['id']).update(
					name = qualification_info['name']
					)
			else:
				#新增分类
				product_catalog_models.ProductCatalogQualification.objects.create(
					catalog_id = catalog_id,
					name = qualification_info['name']
				)
		response = create_response(200)
		return response.get_response()