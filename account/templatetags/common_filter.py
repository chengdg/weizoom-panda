# -*- coding:utf-8 -*-

import time
import json
from datetime import timedelta, datetime, date

from django import template

from station_message import models as message_models 

register = template.Library()

@register.filter(name='to_json')
def to_json(obj):
	if not obj:
		return ""
	else:
		result = json.dumps(obj)
		return result


@register.filter(name='get_messages')
def get_messages(user):
	if user.get_profile().role == 1:
		user_messages = message_models.UserMessage.objects.filter(user_id=user.id)
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
				temp_model = message_models.UserMessage(user_id=user.id,
														message_id=sys_message_id)
				bulk_create.append(temp_model)
			message_models.UserMessage.objects.bulk_create(bulk_create)

		messages = message_models.UserMessage.objects.filter(user_id=user.id,status=0)
		message_id2id = dict([m.message_id, m.id] for m in messages)
		print message_id2id
		message_ids = [message.message_id for message in messages] 
		page_messages = message_models.MessageText.objects.filter(message_id__in=message_ids).order_by('-message_id')
		return_list = []
		for page_message in page_messages:
			cur_messge = {}
			cur_messge['cur_id'] = message_id2id[page_message.id]
			cur_messge['title'] = page_message.title
			return_list.append(cur_messge)
		return return_list
	else:
		return []
	
