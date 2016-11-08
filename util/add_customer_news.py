# -*- coding: utf-8 -*-

from bdem import msgutil
topic_name  = 'customer-news-add'
# test_topic_name = 'test-panda-readmine'
# test_func_name = 'test-panda-new-redmine-log'
def send_reject_product_message(product_name=None, reject_reason=None, customer_id=None, customer_name=None):
	"""
	商品驳回
	"""
	customer_id = customer_id if customer_id.startswith('wzc_') else ''
	msg_name = 'add_customer_news'
	data = {
		'news': {
			'author_username': 'youdongdong',
			'author_name': '小机器人',
			'title': '审核通知',
			'summary': '商品审核未通过（已通过）',
			'description': '商品名：%s，已被操作为：入库审核驳回，驳回原因：%s' % (product_name.encode('utf8'), reject_reason.encode('utf8')),
			'customer_id': str(customer_id).encode('utf8'),
			'customer_name': customer_name.encode('utf8')
		}
	}
	msgutil.send_message(topic_name, msg_name, data)


def send_sync_product_message(product_name=None, platforms=[], customer_id=None, customer_name=None):
	"""
	商品同步
	"""
	customer_id = customer_id if customer_id.startswith('wzc_') else ''
	msg_name = 'add_customer_news'
	platforms_string = u'、'.join(platforms)
	data = {
		'news': {
			'author_username': 'youdongdong',
			'author_name': '小机器人',
			'title': '审核通知',
			'summary': '商品审核已通过',
			'description': '商品名：%s，已被操作为：已入库，已同步，同步同平台分别为：%s' % (product_name.encode('utf8'), platforms_string.encode('utf8')),
			'customer_id': str(customer_id).encode('utf8'),
			'customer_name': customer_name.encode('utf8')
		}
	}

	msgutil.send_message(topic_name, msg_name, data)


def send_stop_sell_product_message(product_name=None, stop_reason=None, customer_id=None, customer_name=None):
	"""
	商品停售
	"""
	customer_id = customer_id if customer_id.startswith('wzc_') else ''
	msg_name = 'add_customer_news'
	data = {
		'news': {
			'author_username': 'youdongdong',
			'author_name': '小机器人',
			'title': '停售通知',
			'summary': '商品撤架停售',
			'description': '商品名：%s，已被操作为：已入库，已停售，停售原因：%s' % (product_name.encode('utf8'), stop_reason.encode('utf8')),
			'customer_id': str(customer_id).encode('utf8'),
			'customer_name': customer_name.encode('utf8')
		}
	}

	msgutil.send_message(topic_name, msg_name, data)