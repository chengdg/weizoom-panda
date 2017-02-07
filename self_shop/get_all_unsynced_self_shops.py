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

#得到所有还未同步的自营平台
class GetAllUnsyncedSelfShops(resource.Resource):
	app = 'self_shop'
	resource = 'get_all_unsynced_self_shops'

	@login_required
	def api_get(request):

		rows,store_name2id=get_self_shops_dict()
		data = {
			'rows': rows
		}
		response = create_response(200)
		response.data = data
		return response.get_response()

def get_self_shops_dict():
	params = {
		'status': 'all'
	}
	resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).get(
		{
			'resource': 'panda.proprietary_account_list',
			'data': params
		}
	)
	rows = []
	store_name2id ={}
	if resp and resp.get('code') == 200:
		data = resp.get('data').get('profiles')
		rows= [{'text':'请选择','value':'-1'}]
		for profile in data:
			rows.append({'text': profile.get('store_name'),'value': profile.get('user_id')})
			store_name2id[profile.get('store_name')] = profile.get('user_id')
	return rows,store_name2id