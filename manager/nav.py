# -*- coding: utf-8 -*-
__author__ = 'hj'

SECOND_NAVS = [{
	'name': 'account-list',
	'displayName': '账号管理',
	'href': '/manager/account/'
},{
	'name': 'account-no－product-list',
	'displayName': '未添加商品账号',
	'href': '/manager/account_no_product/'
}]

def get_second_navs():
	return SECOND_NAVS