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

		page_infos, page_messages = paginator.paginate(messages, cur_page, 2)
		# page_messages = page_infos[1]
		# print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..'
		# print page_messages[0]
		# print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..'
		message_to_text = dict([(message.id, message.text_id) for message in page_messages])
		texts = message_models.MessageText.objects.filter(id__in=message_to_text.values())
		text_id_to_info = dict([(text.id, {'title': text.title, 'text': text.text}) for text in texts])
		results = []
		for temp_msg in page_messages:
			text_info = text_id_to_info.get(message_to_text.get(temp_msg.id))
			temp_dict = {
				'title': text_info.get('title'),
				'text': text_info.get('text'),
				'created_at': temp_msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
				'id': temp_msg.id
			}
			results.append(temp_dict)
		# return results, page_infos

		data = {
			'rows': results,
			'pagination_info': page_infos.to_dict()
		}

		# 构造response
		response = create_response(200)
		response.data = data
		return response.get_response()
