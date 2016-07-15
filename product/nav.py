# -*- coding: utf-8 -*-
__author__ = 'hj'

SECOND_NAVS = [{
	'name': 'product-list',
	'displayName': '商品',
	'href': '/product/product_list/'
},{
	'name': 'product-model',
	'displayName': '商品规格管理',
	'href': '/product/product_model/'
}]

def get_second_navs():
	return SECOND_NAVS