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

class LabelValue(resource.Resource):
	app = 'label'
	resource = 'label_value'

	def api_put(request):
		label_id = request.POST.get('label_id', -1)
		label_value = request.POST.get('label_value', '')
		try:
			if label_id != -1:
				models.LabelPropertyValue.objects.create(
					property_id= label_id,
					name= label_value
				)
				response = create_response(200)
		except Exception, e:
			response = create_response(500)
			msg = unicode_full_stack()
			watchdog.error(msg)
		return response.get_response()

	def api_delete(request):
		label_value_id = request.POST.get('label_value_id',0)
		response = create_response(500)
		try:
			if label_value_id!=0:
				models.LabelPropertyValue.objects.filter(id=label_value_id).delete()
				response = create_response(200)
		except:
			msg = unicode_full_stack()
			response.innerErrMsg = msg
			watchdog.error(msg)
		return response.get_response()