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

from util import string_util
from panda.settings import ZEUS_HOST
import nav
import requests

FIRST_NAV = 'fans'
SECOND_NAV = 'fans'

class Fans(resource.Resource):
	app = 'fans'
	resource = 'fans'

	@login_required
	def get(request):
		"""
		显示商品列表
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV
		})
		
		return render_to_response('fans/fans.html', c)

	def api_get(request):
		rows = [{
			'recommend_time': '2016-06-01',
			'fans_pic': 'http://tva2.sinaimg.cn/crop.0.0.133.133.180/a18c1d18jw8eszx1d2hdij203q03p0sn.jpg',
			'fans_id': '2710314264',
			'sex': '男',
			'purchase_index': 70,
			'diffusion_index': 80,
			'status': u'已阅读'
		}]
		data = {
			'rows': rows
		}
		response = create_response(200)
		response.data = data
		return response.get_response()