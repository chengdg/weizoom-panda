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
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
from util import db_util
from manage import get_all_synced_self_shops

#得到所有已经同步过的自营平台
class GetAllSyncedSelfShops(resource.Resource):
	app = 'self_shop'
	resource = 'get_all_synced_self_shops'

	@login_required
	def api_get(request):
		is_for_search = False
		if request.GET.get('is_for_search', '') == 'true':
			is_for_search = True
		data = get_all_synced_self_shops(request, is_for_search)
		response = create_response(200)
		response.data = data
		return response.get_response()