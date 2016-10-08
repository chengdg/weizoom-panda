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
SECOND_NAV = 'template'
COUNT_PER_PAGE = 20


class PostageConfig(resource.Resource):
	"""

	"""

	app = 'postage_config'
	resource = 'new_template'

	def get(request):
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV
		})
		return render_to_response('postage_config/new_template.html', c)

