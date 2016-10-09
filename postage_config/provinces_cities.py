# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.models import User
from django.contrib import auth

from core import resource
from core.jsonresponse import create_response
from eaglet.utils.resource_client import Resource

from account.models import *
from product import models as models

ZONE_NAMES = [u'直辖市', u'华北-东北', u'华东地区', u'华南-华中', u'西北-西南', u'其它']

PROVINCE_ID2ZONE = {
    1: u'直辖市',
    2: u'直辖市',
    3: u'华北-东北',
    4: u'华北-东北',
    5: u'华北-东北',
    6: u'华北-东北',
    7: u'华北-东北',
    8: u'华北-东北',
    9: u'直辖市',
    10: u'华东地区',
    11: u'华东地区',
    12: u'华东地区',
    13: u'华东地区',
    14: u'华东地区',
    15: u'华东地区',
    16: u'华南-华中',
    17: u'华南-华中',
    18: u'华南-华中',
    19: u'华南-华中',
    20: u'华南-华中',
    21: u'华南-华中',
    22: u'直辖市',
    23: u'西北-西南',
    24: u'西北-西南',
    25: u'西北-西南',
    26: u'西北-西南',
    27: u'西北-西南',
    28: u'西北-西南',
    29: u'西北-西南',
    30: u'西北-西南',
    31: u'西北-西南',
    32: u'其它',
    33: u'其它',
    34: u'其它',
}

#只包含省份
class ProvincesCities(resource.Resource):
	app = 'postage_config'
	resource = 'provinces_cities'

	def api_get(request):
		all_cities = models.City.objects.filter(province_id=-1)
		all_provinces = models.Province.objects.all()
		id2province = dict([(p.id, p) for p in all_provinces])

		provinces = []
		for id in id2province.keys():
			province_has_city = {
				'provinceId': id,
				'provinceName': id2province[id].name,
				'cities': []
			}
			province_has_city = rename_zone(province_has_city)
			for city in filter(lambda city: city.province_id == id, all_cities):
				province_has_city['cities'].append({
					'cityId': city.id,
					'cityName': city.name,
				})
			provinces.append(province_has_city)

		zones = []
		for zone_name in ZONE_NAMES:
			zones.append({
				'zoneName': zone_name,
				'provinces': filter(lambda province: PROVINCE_ID2ZONE[province['provinceId']] == zone_name, provinces)
			})

		response = create_response(200)
		response.data = {'items': zones}
		return response.get_response()


def rename_zone(zone):
	if zone['provinceId'] == 5:
		zone['provinceName'] = u'内蒙古'
	elif zone['provinceId'] == 20:
		zone['provinceName'] = u'广西'
	elif zone['provinceId'] == 26:
		zone['provinceName'] = u'西藏'
	elif zone['provinceId'] == 30:
		zone['provinceName'] = u'宁夏'
	elif zone['provinceId'] == 31:
		zone['provinceName'] = u'新疆'
	elif zone['provinceId'] == 32:
		zone['provinceName'] = u'香港'
	elif zone['provinceId'] == 33:
		zone['provinceName'] = u'澳门'
	elif zone['provinceId'] == 34:
		zone['provinceName'] = u'台湾'
	return zone
