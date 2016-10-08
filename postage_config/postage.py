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


class Postage(resource.Resource):
	"""
	运费模板列表
	"""
	app = 'postage_config'
	resource = 'postage'

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
