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

from util import string_util
from account import models as account_models
from product import models as product_models
from panda.settings import ZEUS_HOST
from util import db_util
import nav
import models

FIRST_NAV = 'freight_service'
SECOND_NAV = 'service'

class service(resource.Resource):
	app = 'freight_service'
	resource = 'service'

	@login_required
	def get(request):
		user_profile = account_models.UserProfile.objects.filter(user_id=request.user.id)
		pre_sale_tel = user_profile[0].pre_sale_tel
		after_sale_tel = user_profile[0].after_sale_tel
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
			'pre_sale_tel': str(pre_sale_tel)if pre_sale_tel else '-1',
			'after_sale_tel': str(after_sale_tel) if after_sale_tel else '-1'
		})
		return render_to_response('freight_service/service.html', c)

	@login_required
	def api_put(request):
		user_id = request.user.id
		pre_sale_tel = request.POST.get('pre_sale_tel','')
		after_sale_tel = request.POST.get('after_sale_tel','')
		response = create_response(200)
		data = {}
		try:
			user_profile = account_models.UserProfile.objects.filter(user_id=user_id)
			if user_profile:
				user_profile.update(
					pre_sale_tel= pre_sale_tel,
					after_sale_tel = after_sale_tel
				)
			data['code'] = 200
			response.data=data
		except Exception, e:
			data['code'] = 500
			response.data=data
			response.innerErrMsg = unicode_full_stack()
		return response.get_response()