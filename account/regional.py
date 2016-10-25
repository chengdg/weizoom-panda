# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth

from core.jsonresponse import create_response
from core import resource
from product import models as product_models

class Regional(resource.Resource):
	"""
	收货地址调用的地区信息
	"""
	app = 'account'
	resource = 'regional'

	def api_get(request):
		regional_type = request.GET.get('type')
		select_id = request.GET.get('id')

		if regional_type == 'provinces':
			regional_info = get_all_provinces()
		elif regional_type == 'cities':
			regional_info = get_cities_for_province(select_id)
		elif regional_type == 'districts':
			regional_info = get_districts_for_city(select_id)

		print regional_info,"====sssss======"
		response = create_response(200)
		response.data = {'regional_info': regional_info}
		return response.get_response()

def get_all_provinces():
		provinces = {}
		for province in product_models.Province.objects.all():
			provinces[province.id] = province.name
		return provinces

def get_cities_for_province(select_id):
	cities = {}
	for city in product_models.City.objects.filter(province_id=select_id):
		cities[city.id] = city.name
	return cities

def get_districts_for_city(select_id):
	cities = {}
	for city in product_models.District.objects.filter(city_id=select_id):
		cities[city.id] = city.name
	return cities