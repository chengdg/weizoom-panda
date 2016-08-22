# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from core import resource
from core.jsonresponse import create_response
from core import paginator

from util import db_util
from resource import models as resource_models
from account.models import *
from util import string_util
from panda.settings import ZEUS_HOST
from panda.settings import PANDA_HOST
from product.sales_from_weapp import sales_from_weapp
import nav
import models
import requests
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
from eaglet.utils.resource_client import Resource
from product_catalog import models as product_catalog_models

second_navs = [{
	'name': 'product-relation-list',
	'displayName': '商品',
	'href': '/product/product_relation/'
},
{
	'name': 'product-update-list',
	'displayName': '商品更新',
	'href': '/product/product_updated/'
}]

FIRST_NAV = 'product'
SECOND_NAV = 'product-update-list'

class ProductUpdated(resource.Resource):
	app = 'product'
	resource = 'product_updated'

	@login_required
	def get(request):
		"""
		显示商品列表
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': second_navs,
			'second_nav_name': SECOND_NAV
		})

		return render_to_response('product/product_updated.html', c)