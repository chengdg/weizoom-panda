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
from resource import models as resource_models
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
		message_id = request.GET.get('id')
		message = message_models.Message.objects.filter(id=message_id).first()
		title = ''
		text = ''
		attachments = []
		if message:
			message_text = message_models.MessageText.objects.filter(id=message.text_id).first()
			if message_text:
				title = message_text.title
				text = message_text.text
			attachment_ids = [attachment.document_id for attachment in message_models.MessageAttachment
				.objects.filter(message_id=message_id)]
			attachments = resource_models.Document.objects.filter(id__in=attachment_ids)
			attachments = [{'id': at.id,
							'name': at.filename,
							'type': at.type,
							'path': at.path} for at in attachments]

		print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.'
		print attachments, title, text
		print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.'
		jsons = {'items': []}
		jsons['items'].append(('message', json.dumps({
				'attachment': attachments,
				'id': message_id,
				'title': title,
				'text': text,
			}),))
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV,
			'jsons': jsons,

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
				# 信息详情里边加上一个message_id
				text_model.message_id = message_model.id
				text_model.save()
				if message_model and attachments:
					bulk_create = []
					for attachment in attachments:
						temp = message_models.MessageAttachment(message_id=message_model.id,
																document_id=attachment.get('id'))
						bulk_create.append(temp)
					message_models.MessageAttachment.objects.bulk_create(bulk_create)
		except:
			msg = "{}".format(unicode_full_stack())
			watchdog.error(msg)
			response = create_response(500)
			# print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
			# print msg
			return response.get_response()
		response = create_response(200)
		return response.get_response()

	@login_required
	def api_delete(request):
		"""

		"""
		data = request.POST
		message_id = data.get('message_id')
		try:
			message_models.Message.objects.filter(id=message_id).update(is_deleted=True)
			message_models.UserMessage.objects.filter(message_id=message_id).delete()
		except:
			# msg = unicode_full_stack()
			msg = "{}".format(unicode_full_stack())
			watchdog.error(msg)
			response = create_response(500)
			print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
			print msg
			return response.get_response()
		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		"""

		"""

		data = request.POST
		parser = HTMLParser.HTMLParser()
		# : {u'text': [u'<p>12</p>'], u'_method': [u'put'], u'timestamp': [u'1471846427863'],
		#  u'title': [u'12']}>
		title = data.get('title')
		message_id = data.get('message_id')
		text = data.get('text')

		text = parser.unescape(text)
		attachments = data.get('attachment')
		if attachments:
			attachments = json.loads(attachments)
		message = message_models.Message.objects.filter(id=message_id).first()
		if message:
			text_id = message.text_id
			try:
				message_models.MessageText.objects.filter(id=text_id).update(title=title,
																			 text=text)
				message_models.MessageAttachment.objects.filter(message_id=message_id).delete()
				bulk_create = []
				if attachments:
					for attachment in attachments:
						temp = message_models.MessageAttachment(message_id=message_id,
																document_id=attachment.get('id'))
						bulk_create.append(temp)
					message_models.MessageAttachment.objects.bulk_create(bulk_create)
				response = create_response(200)
				return response.get_response()
			except:
				msg = "{}".format(unicode_full_stack())
				watchdog.error(msg)
				print msg

				response = create_response(500)
				return response.get_response()
		else:
			response = create_response(500)
			return response.get_response()
