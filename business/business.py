# -*- coding: utf-8 -*-
__author__ = 'lihanyi'

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

from resource import models as resource_models
from product import models as product_models
from account.models import *
from util import string_util
from util import db_util
import requests


class BusinessApply(resource.Resource):
	app = 'business'
	resource = 'apply'

	# def get(request):
	# 	print 'aaaaaaaaaaaaaaa'
	# 	c = RequestContext(request, {
	# 	})
		
	# 	return render_to_response('business/business_apply.html', c)

	# def api_get(request):
	# 	is_export = False
	# 	rows,pageinfo = getCustomerData(request,is_export)
	# 	data = {
	# 		'rows': rows,
	# 		'pagination_info': pageinfo.to_dict()
	# 	}
	# 	response = create_response(200)
	# 	response.data = data
	# 	return response.get_response()
