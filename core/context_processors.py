# -*- coding: utf-8 -*-

from django.conf import settings
from account.models import *
from station_message import models as message_model
#===============================================================================
# top_navs : 获得top nav集合
#===============================================================================
def top_navs(request):
	try:
		role = UserProfile.objects.get(user_id=request.user.id).role
		if role == CUSTOMER:
			# 获取该登录用户有多少条站内信(未读)
			# TODO 每次都查询有点不科学,想办法优化
			user_messages = message_model.UserMessage.objects.filter(user_id=request.user.id)
			all_user_message_id = [user_message.message_id for user_message in user_messages]

			un_read_messages = user_messages.filter(status=0)
			# 所有系统消息
			all_sys_messages = message_model.Message.objects.filter(is_deleted=False,
																	receive_id=-1)
			all_sys_message_id = [m.id for m in all_sys_messages]
			# 系统消息,但是未插入用户表的消息
			un_insert_sys_message = list(set(all_sys_message_id) - set(all_user_message_id))
			un_read_message_count = len(un_insert_sys_message) + len(un_read_messages)
			message_title = '站内消息 (%s)' % un_read_message_count
			
			top_navs = [{
				'name': 'product',
				'displayName': '商品',
				'icon': 'credit-card',
				'href': '/product/product_list/'
			},
			# {
			# 	'name': 'fans',
			# 	'displayName': '粉丝投放',
			# 	'icon': 'list-alt',
			# 	'href': '/fans/fans/'
			# },
			{
				'name': 'order',
				'displayName': '订单',
				'icon': 'list-alt',
				'href': '/order/customer_orders_list/'
			},{
				'name': 'finance',
				'displayName': '对账结算',
				'icon': 'list-alt',
				'href': 'http://finance.weizoom.com/balance_account/account_profile/?token=' + user_token(request) #登录财务系统
			},
			# {
			# 	'name': 'freight_service',
			# 	'displayName': '商家设置',
			# 	'icon': 'list-alt',
			# 	'href': '/freight_service/freight/'
			# },
			{
				'name': 'postage_config',
				'displayName': '商家设置',
				'icon': 'glyphicon glyphicon-file',
				'href': '/postage_config/postage_list'
			},{
				'name': 'message',
				'displayName': message_title,
				'icon': 'glyphicon glyphicon-comment',
				'href': '/message/customer_messages'
			},{
				'name': 'limit_zone',
				'displayName': '禁售仅售模板',
				'icon': 'glyphicon glyphicon-file',
				'href': '/limit_zone/template_list'
			}]
		elif role == AGENCY:
			top_navs = [{
				'name': 'customer',
				'displayName': '客户统计',
				'icon': 'credit-card',
				'href': '/customer/statistics/'
			}]
		elif role == YUN_YING:
			top_navs = [
			{
				'name': 'product_catalog',
				'displayName': '商品分类',
				'icon': 'credit-card',
				'href': '/product_catalog/product_catalogs/'
			},
			{
				'name': 'label',
				'displayName': '标签管理',
				'icon': 'list-alt',
				'href': '/label/label_manager/'
			},
			{
				'name': 'product',
				'displayName': '商品',
				'icon': 'credit-card',
				'href': '/product/product_relation/'
			},{
				'name': 'order',
				'displayName': '订单',
				'icon': 'list-alt',
				'href': '/order/yunying_orders_list/'
			},{
				'name': 'customer',
				'displayName': '客户统计',
				'icon': 'credit-card',
				'href': '/customer/statistics/'
			},{
				'name': 'self_shop',
				'displayName': '自营平台管理',
				'icon': 'credit-card',
				'href': '/self_shop/manage/'
			},{
				'name': 'business',
				'displayName': '客户管理',
				'icon': 'credit-card',
				'href': '/business/manager/'
			},{
				'name': 'message',
				'displayName': '站内消息',
				'icon': 'glyphicon glyphicon-comment',
				'href': '/message/message_list'
			}
			]
		elif role == MANAGER:
			top_navs = [{
				'name': 'manager',
				'displayName': '账号管理',
				'icon': 'cog',
				'href': '/manager/account/'
			}]
		else:
			top_navs = [{
				'name': 'product',
				'displayName': '商品',
				'icon': 'credit-card',
				'href': '/product/product_list/'
			}, {
				'name': 'order',
				'displayName': '订单',
				'icon': 'list-alt',
				'href': '/order/yunying_orders_list/'
			}, {
				'name': 'manager',
				'displayName': '账号管理',
				'icon': 'cog',
				'href': '/manager/account/'
			}]
		return {'top_navs': top_navs}
	except Exception,e:
		top_navs = [{
			'name': 'product',
			'displayName': '商品',
			'icon': 'credit-card',
			'href': '/product/product_list/'
		}, {
			'name': 'order',
			'displayName': '订单',
			'icon': 'list-alt',
			'href': '/order/yunying_orders_list/'

		}]
	return {'top_navs': top_navs}

def webpack_bundle_js(request):
	return {
		'webpack_bundle_js': settings.WEBPACK_BUNDLE_JS
	}

def user_token(request):
	if not hasattr(request, 'user') or request.user is None:
		return ''

	from account import account_util
	user_token = account_util.get_token_for_logined_user(request.user)
	return user_token