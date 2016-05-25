# -*- coding: utf-8 -*-

from django.conf import settings

#===============================================================================
# top_navs : 获得top nav集合
#===============================================================================
def top_navs(request):
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
		'name': 'account_manage',
		'displayName': '账号管理',
		'icon': 'cog',
		'href': '/manager/account/'
	}]
	return {'top_navs': top_navs}


def webpack_bundle_js(request):
	return {
		'webpack_bundle_js': settings.WEBPACK_BUNDLE_JS
	}