# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from django.contrib import auth

from core.jsonresponse import create_response, JsonResponse
from core.exceptionutil import unicode_full_stack

#===============================================================================
# index : 商家入驻
#===============================================================================

def index(request):
	c = RequestContext(request, {
		# 'webpack_bundle_js' : settings.WEBPACK_BUNDLE_JS
	})
		
	return render_to_response('business/business_apply_1.html', c)