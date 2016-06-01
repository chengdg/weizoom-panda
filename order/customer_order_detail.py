# -*- coding: utf-8 -*-
import json
import time
import base64

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
import nav
import models
from resource import models as resource_models
from util import string_util

FIRST_NAV = 'order'
SECOND_NAV = 'order-list'


class Data(resource.Resource):
	app = 'order'
	resource = 'data'
	
	@login_required
	def get(request):
		#获取业务数据
		order_id = request.GET.get('id', None)
		jsons = {'items':[]}
		if order_id:
			order_data = []
			jsons['items'].append(('order', json.dumps(order_data)))
		else:
			jsons['items'].append(('order', json.dumps(None)))

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
			'jsons': jsons
		})
		return render_to_response('order/customer_order_detail.html', c)