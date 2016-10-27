# -*- coding: utf-8 -*-
__author__ = 'hj'

SECOND_NAVS = [{
	'name': 'postage_list',
	'displayName': '运费模板',
	'href': '/postage_config/postage_list/'
},{
	'name': 'shipper_manage',
	'displayName': '发货人&电子面单',
	'href': '/postage_config/shipper_manage/'
}]

def get_second_navs():
	return SECOND_NAVS