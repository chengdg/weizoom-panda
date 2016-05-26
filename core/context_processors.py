# -*- coding: utf-8 -*-

from django.conf import settings
from account.models import *
#===============================================================================
# top_navs : 获得top nav集合
#===============================================================================
def top_navs(request):
	role = UserProfile.objects.get(user_id=request.user.id).role
	print(role)
	if role == CUSTOMER:
		top_navs = [{
			'name': 'order',
			'displayName': '订单',
			'icon': 'list-alt',
			'href': '/order/datas/'
		}, {
			'name': 'product',
			'displayName': '商品',
			'icon': 'credit-card',
			'href': '/product/product_list/'
		}, {
			'name': 'fans',
			'displayName': '粉丝投放',
			'icon': 'cog',
			'href': '#'
		}, {
			'name': 'reconcile',
			'displayName': '对账',
			'icon': 'cog',
			'href': '#'
		}]
	elif role == AGENCY:
		top_navs = []
	elif role == YUN_YING:
		top_navs = [{
			'name': 'order',
			'displayName': '订单',
			'icon': 'list-alt',
			'href': '/order/datas/'
		}, {
			'name': 'product',
			'displayName': '商品',
			'icon': 'credit-card',
			'href': '/product/product_list/'
		}]
	else:
		top_navs = [{
			'name': 'order',
			'displayName': '订单',
			'icon': 'list-alt',
			'href': '/order/datas/'
		}, {
			'name': 'product',
			'displayName': '商品',
			'icon': 'credit-card',
			'href': '/product/product_list/'
		}, {
			'name': 'fans',
			'displayName': '粉丝投放',
			'icon': 'cog',
			'href': '#'
		}, {
			'name': 'reconcile',
			'displayName': '对账',
			'icon': 'cog',
			'href': '#'
		}, {
			'name': 'manager',
			'displayName': '账号管理',
			'icon': 'cog',
			'href': '/manager/account/'
		}]
	return {'top_navs': top_navs}


def webpack_bundle_js(request):
	return {
		'webpack_bundle_js': settings.WEBPACK_BUNDLE_JS
	}