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

from util import db_util
from account.models import *
from util import string_util

import nav
import models

FIRST_NAV = 'label'
SECOND_NAV = 'label-manager'

#标签管理
class LabelManager(resource.Resource):
	app = 'label'
	resource = 'label_manager'

	@login_required
	def get(request):
		"""
		显示标签列表
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
		})

		return render_to_response('label/label_manager.html', c)

	def api_get(request):
		label_properties = models.LabelProperty.objects.filter(is_deleted=False)
		label_property_values = models.LabelPropertyValue.objects.filter(is_deleted=False)
		property_id2name = {}
		for label_property_value in label_property_values:
			if label_property_value.property_id not in property_id2name:
				property_id2name[label_property_value.property_id] = [{
					'label_value_id': label_property_value.id,
					'name': label_property_value.name
				}]
			else:
				property_id2name[label_property_value.property_id].append({
					'label_value_id': label_property_value.id,
					'name': label_property_value.name
				})

		rows = []
		for label_property in label_properties:
			rows.append({
				'id': label_property.id,
				'labelName': label_property.name,
				'labelValues': [] if label_property.id not in property_id2name else json.dumps(property_id2name[label_property.id])
				})
		data = {
			'rows': rows
		}

		# 构造response
		response = create_response(200)
		response.data = data
		return response.get_response()

	def api_put(request):
		try:
			models.LabelProperty.objects.create(
				user_id= request.user.id
			)
			response = create_response(200)
		except Exception, e:
			response = create_response(500)
			msg = unicode_full_stack()
			watchdog.error(msg)
		return response.get_response()

	def api_post(request):
		label_id = request.POST.get('label_id', -1)
		name = request.POST.get('name', '')
		try:
			models.LabelProperty.objects.filter(id=int(label_id)).update(
				name= name
			)
			response = create_response(200)
		except Exception, e:
			response = create_response(500)
			msg = unicode_full_stack()
			watchdog.error(msg)
		return response.get_response()

	def api_delete(request):
		label_id = request.POST.get('label_id', 0)
		response = create_response(500)
		try:
			if label_id != 0:
				models.LabelProperty.objects.filter(id=label_id).update(is_deleted=True)
				models.LabelPropertyValue.objects.filter(property_id=label_id).update(is_deleted=True)
				response = create_response(200)
		except:
			msg = unicode_full_stack()
			watchdog.error(msg)
			response.innerErrMsg = msg
		return response.get_response()