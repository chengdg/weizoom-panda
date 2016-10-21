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
SECOND_NAVS = [{
	'name': 'message_list',
	'displayName': '系统消息',
	'href': '/message/customer_messages/'
}]


class ProductCatalog(resource.Resource):
	app = 'message'
	resource = 'customer_messages'

	@login_required
	def get(request):
		"""
		显示商品列表
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': SECOND_NAVS,
			'second_nav_name': SECOND_NAV
		})
		return render_to_response('customer_messages.html', c)

	@login_required
	def api_get(request):
		"""

		"""

		cur_page = request.GET.get('page', 1)
		# messages = message_models.Message.objects.filter(is_deleted=False,).order_by('-created_at')
		user_messages = message_models.UserMessage.objects.filter(user_id=request.user.id)
		# 已经插入用户消息的系统消息
		user_message_ids = [user_message.message_id for user_message in user_messages]
		# 未插入的系统消息
		sys_messages = message_models.Message.objects.exclude(id__in=user_message_ids,)

		sys_messages = sys_messages.exclude(is_deleted=True,)
		sys_messages = sys_messages.filter(receive_id=-1)
		sys_message_ids = [sys_message.id for sys_message in sys_messages]
		# print '++++++++++++++++++++++++++++++=='
		# print sys_message_ids, user_message_ids
		# print '++++++++++++++++++++++++++++++=='
		if sys_message_ids:
			# 说明有新的系统消息
			bulk_create = []
			for sys_message_id in sys_message_ids:
				temp_model = message_models.UserMessage(user_id=request.user.id,
														message_id=sys_message_id)
				bulk_create.append(temp_model)
			message_models.UserMessage.objects.bulk_create(bulk_create)
		# 查询消息
		messages = message_models.UserMessage.objects.filter(user_id=request.user.id).order_by('status', '-message_id')
		page_infos, page_user_messages = paginator.paginate(messages, cur_page, 20)
		# page_messages = page_infos[1]
		page_message_ids = [user_message.message_id for user_message in page_user_messages]
		# 本页的信息详情
		page_messages = message_models.MessageText.objects.filter(message_id__in=page_message_ids)
		message_id_to_obj = dict([(message.id, message) for message in page_messages])

		# message_to_text_id = dict([(message.id, message.text_id) for message in page_messages])
		# texts = message_models.MessageText.objects.filter(id__in=message_to_text_id.values())
		# text_id_to_info = dict([(text.id, {'title': text.title, 'text': text.text}) for text in texts])
		results = []
		for temp_msg in page_user_messages:
			text_info = message_id_to_obj.get(temp_msg.message_id)
			temp_dict = {
				'title': text_info.title,
				'created_at': text_info.created_at.strftime('%Y-%m-%d %H:%M:%S') if text_info.created_at else '',
				'id': temp_msg.id,
				'status': temp_msg.status
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
