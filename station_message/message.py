# -*- coding: utf-8 -*-
import json
import HTMLParser
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog

from core.jsonresponse import create_response
from core import resource

import models as message_models
import nav

FIRST_NAV = 'message'
SECOND_NAV = 'message_list'
# COUNT_PER_PAGE = 10


class ProductCatalog(resource.Resource):
	app = 'message'
	resource = 'message'

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
		return render_to_response('message.html', c)

	@login_required
	def api_put(request):
		"""

		"""

		data = request.POST
		parser = HTMLParser.HTMLParser()
		# : {u'text': [u'<p>12</p>'], u'_method': [u'put'], u'timestamp': [u'1471846427863'],
		#  u'title': [u'12']}>
		title = data.get('title')
		text = data.get('text')
		text = parser.unescape(text)
		attachments = data.get('attachment')
		if attachments:
			attachments = json.loads(attachments)
		# print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..1'
		# print title, text, attachments
		# print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..2'
		try:
			text_model = message_models.MessageText.objects.create(title=title,
																   text=text)
			if text_model:
				message_model = message_models.Message.objects.create(send_id=request.user.id,
																	  text_id=text_model.id)
				if message_model and attachments:
					bulk_create = []
					for attachment in attachments:
						temp = message_models.MessageAttachment(message_id=message_model.id,
																document_id=attachment.get('id'))
						bulk_create.append(temp)
					message_models.MessageAttachment.objects.bulk_create(bulk_create)
		except:
			msg = unicode_full_stack()
			watchdog.error(msg)
			response = create_response(500)
			print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
			print msg
			return response.get_response()
		response = create_response(200)
		return response.get_response()
