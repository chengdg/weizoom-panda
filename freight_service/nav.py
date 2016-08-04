# -*- coding: utf-8 -*-
__author__ = 'hj'

SECOND_NAVS = [{
	'name': 'freight',
	'displayName': '运费设置',
	'href': '/freight_service/freight/'
},{
	'name': 'service',
	'displayName': '客服设置',
	'href': '/freight_service/service/'
}]

def get_second_navs():
	return SECOND_NAVS