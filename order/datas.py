# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from core import paginator
from util import db_util
import nav
import models

FIRST_NAV = 'order'
SECOND_NAV = 'order-list'

class Datas(resource.Resource):
	app = 'order'
	resource = 'datas'

	@login_required
	def get(request):
		"""
		响应GET
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV
		})
		
		return render_to_response('order/datas.html', c)

	def api_get(request):
		rows = []
		data = {
			'rows': rows,
		}

		#构造response
		response = create_response(200)
		response.data = data

		return response.get_response()
