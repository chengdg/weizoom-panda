# -*- coding: utf-8 -*-
import json

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response

from product import models as product_models
from account import models as account_models
from util import sync_util
import nav
import models

FIRST_NAV = 'postage_config'
SECOND_NAV = 'shipper_manage'
COUNT_PER_PAGE = 20

class PostageList(resource.Resource):
	"""
	运费模板列表
	"""
	app = 'postage_config'
	resource = 'shipper_manage'

	@login_required
	def get(request):
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV
		})
		return render_to_response('shipper_manage/shipper_manage.html', c)
