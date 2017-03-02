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
	messages = message_models.UserMessage.objects.filter(user_id=user.id,status=0)
	message_ids = [message.message_id for message in messages] 
	page_messages = message_models.MessageText.objects.filter(message_id__in=message_ids)

	return page_messages
	
