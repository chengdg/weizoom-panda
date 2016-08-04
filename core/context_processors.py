# -*- coding: utf-8 -*-

from django.conf import settings
from account.models import *
#===============================================================================
# top_navs : 获得top nav集合
#===============================================================================
def top_navs(request):
	try:
		role = UserProfile.objects.get(user_id=request.user.id).role
		if role == CUSTOMER:
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
			}
			# , {
			# 	'name': 'fans',
			# 	'displayName': '粉丝投放',
			# 	'icon': 'cog',
			# 	'href': '#'
			# }, {
			# 	'name': 'reconcile',
			# 	'displayName': '对账',
			# 	'icon': 'cog',
			# 	'href': '#'
			# }
			]
		elif role == AGENCY:
			top_navs = [{
				'name': 'customer',
				'displayName': '客户统计',
				'icon': 'credit-card',
				'href': '/customer/statistics/'
			}]
		elif role == YUN_YING:
			top_navs = [
			# {
			# 	'name': 'product_catalog',
			# 	'displayName': '商品分类',
			# 	'icon': 'credit-card',
			# 	'href': '/product_catalog/product_catalogs/'
			# },
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
			}]
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
			},
			# {
			# 	'name': 'reconcile',
			# 	'displayName': '对账',
			# 	'icon': 'cog',
			# 	'href': '#'
			# },
			{
				'name': 'manager',
				'displayName': '账号管理',
				'icon': 'cog',
				'href': '/manager/account/'
			}]
		return {'top_navs': top_navs}
	except:
		top_navs = [{
			'name': 'product',
			'displayName': '商品',
			'icon': 'credit-card',
			'href': '/product/product_list/'
		},{
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


def webpack_bundle_js(request):
	return {
		'webpack_bundle_js': settings.WEBPACK_BUNDLE_JS
	}