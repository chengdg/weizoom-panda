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
from core.exceptionutil import unicode_full_stack
from core import paginator
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog

from util import string_util
from account import models as account_models
from product import models as product_models
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
from util import db_util
from panda.settings import CESHI_USERNAMES

import nav
import models


FIRST_NAV = 'postage_config'
SECOND_NAV = 'postage_list'
COUNT_PER_PAGE = 20


class PostageList(resource.Resource):
	"""
	运费模板列表
	"""
	app = 'postage_config'
	resource = 'postage_list'

	@login_required
	def get(request):
		postages = [{
			"postage_name": u"普通快递",
			"postage_default": u"全国1",
			"postage_id": "2"
		},{
			"postage_name": u"普通快递",
			"postage_default": u"全国2",
			"postage_id": "1"
		}]
		print json.dumps(postages),"------"
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
			'postages': json.dumps(postages)
		})
		return render_to_response('postage_config/postage_list.html', c)

	@login_required
	def api_get(request):
		rows = [{
			'postage_method': u'普通快递',
			'postage_destination': u'全国',
			'postage_weight': '2',
			'postage_price': '5.00',
			'over_weight': '1',
			'over_price': '0.00'
		}]
		data = {
			'rows': rows
		}	

		# 构造response
		response = create_response(200)
		response.data = data
		return response.get_response()
