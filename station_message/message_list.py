# -*- coding: utf-8 -*-
import json

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog

from core import resource
from core import paginator
from core.jsonresponse import create_response

from account import models as account_models
from product import models as product_models
from panda.settings import EAGLET_CLIENT_ZEUS_HOST, ZEUS_SERVICE_NAME

import models as message_models
import nav

FIRST_NAV = 'message'
SECOND_NAV = 'message_list'
# COUNT_PER_PAGE = 10


class ProductCatalog(resource.Resource):
	app = 'message'
	resource = 'message_list'

	@login_required
	def get(request):
		"""
		显示商品列表
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV
		})
		return render_to_response('message_list.html', c)

	@login_required
	def api_get(request):
		"""

		"""

		cur_page = request.GET.get('page', 1)
		messages = message_models.Message.objects.filter(is_deleted=False).order_by('-created_at')

		page_messages = paginator.paginate(messages, cur_page, 20)
		print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..'
		print page_messages
		print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..'
		return None
