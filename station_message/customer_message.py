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
from resource import models as resource_models
import nav

FIRST_NAV = 'message'
SECOND_NAV = 'message_list'
# COUNT_PER_PAGE = 10
SECOND_NAVS = [{
	'name': 'message_list',
	'displayName': '系统消息',
	'href': '/message/customer_messages/'
}]


class CustomerMessage(resource.Resource):
	app = 'message'
	resource = 'read_message'

	@login_required
	def get(request):
		"""
		读取某个消息
		"""
		message_id = request.GET.get('message_id')
		user_message = message_models.UserMessage.objects.filter(id=message_id).first()
		title = ''
		text = ''
		created_at = ''
		message_models.UserMessage.objects.filter(id=message_id).update(status=1)
		if user_message:
			message = message_models.MessageText.objects.filter(message_id=user_message.message_id).first()
			title = message.title
			text = message.text
			created_at = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
		jsons = {'items': []}
		attachment_ids = [attachment.document_id for attachment in message_models.MessageAttachment
			.objects.filter(message_id=user_message.message_id)]
		# print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..'
		# print attachment_ids, message_id
		# print '=======================================..'
		attachments = resource_models.Document.objects.filter(id__in=attachment_ids)
		attachments = [{'id': at.id,
						'filename': at.filename,
						'type': at.type,
						'path': at.path} for at in attachments]

		jsons['items'].append(('message', json.dumps({
			'title': title,
			'text': text,
			'created_at': created_at,
			'attachments': attachments
		}),))
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': SECOND_NAVS,
			'second_nav_name': SECOND_NAV,
			'jsons': jsons
		})
		return render_to_response('customer_message.html', c)
