# -*- coding: utf-8 -*-
__author__ = 'lihanyi'

import json
import time
import os
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from core import resource
from core.jsonresponse import create_response
from core import paginator

from resource import models as resource_models
from product import models as product_models
from account.models import *
from util import string_util
from util import db_util
import requests


class BusinessApply(resource.Resource):
	app = 'business'
	resource = 'apply'

	# def get(request):
	# 	print 'aaaaaaaaaaaaaaa'
	# 	c = RequestContext(request, {
	# 	})
		
	# 	return render_to_response('business/business_apply.html', c)

	# def api_get(request):
	# 	is_export = False
	# 	rows,pageinfo = getCustomerData(request,is_export)
	# 	data = {
	# 		'rows': rows,
	# 		'pagination_info': pageinfo.to_dict()
	# 	}
	# 	response = create_response(200)
	# 	response.data = data
	# 	return response.get_response()

class BussinessUpload(resource.Resource):
	app = 'business'
	resource = 'upload_img'

	def post(request):
		"""
		上传头像
		"""
		print '111111111111111'
		upload_file = request.FILES.get('Filedata', None)
		response = create_response(500)
		if upload_file:
			try:
				now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
				upload_file.name = now + upload_file.name
				file_path = BussinessUpload.__save_player_pic(upload_file, now)
				print file_path
				print 'file_path==============='
			except:
				response.errMsg = u'保存文件出错'
				return response.get_response()

			response = create_response(200)
			response.data = file_path
		else:
			response.errMsg = u'文件错误'
		return response.get_response()

		response = create_response(500)
		return response.get_response()

	@staticmethod
	def __save_player_pic(file, now):
		"""
		@param file: 文件
		@return: 文件保存路径
		"""
		content = []
		curr_dir = os.path.dirname(os.path.abspath(__file__))
		if file:
			for chunk in file.chunks():
				content.append(chunk)
		print '222222222222222222222222'
		print curr_dir
		dir_path = os.path.join(curr_dir, '../../../','static', 'upload', 'now'+now)
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		file_path = os.path.join(dir_path, file.name)

		dst_file = open(file_path, 'wb')
		print >> dst_file, ''.join(content)
		dst_file.close()
		file_path = os.path.join('\static', 'upload', 'now'+now, file.name).replace('\\','/')
		return file_path