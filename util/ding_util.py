#coding=utf8

# 调用接口发送钉钉消息的工具 duhao

from django.conf import settings

from bdem import msgutil

def send_to_ding(text, cid):
	if settings.MODE == "deploy":
		uuid = 199597313
	else:
		uuid = 80035247

	data = {
		"uuid": uuid,
		"content": text
	}
	msgutil.send_queue_message('notify', 'ding', data)
	