# -*- coding: utf-8 -*-

import json
from datetime import datetime
import os
import random
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.conf import settings

from core import resource
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack
import models
import base64
try:
	from PIL import Image
except:
	import Image

class Image(resource.Resource):
	"""
	图片
	"""
	app = 'resource'
	resource = 'image'

	def __get_file_name(file_name):
		"""
		基于上传的文件的文件名file_name，生成一个server端唯一的文件名
		"""
		pos = file_name.rfind('.')
		if pos == -1:
			suffix = ''
		else:
			suffix = file_name[pos:]
			
		return '%s_%d%s' % (str(time.time()).replace('.', '0'), random.randint(1, 1000), suffix)
	
	@login_required
	def put(request):
		file = request.FILES.get('image', None)

		#读取二进制内容
		content = []
		if file:
			for chunk in file.chunks():
				content.append(chunk)

		#获取存储图片的目录和文件信息
		file_name = Image.__get_file_name(file.name)
		store_dir = time.strftime('%Y%m%d')
		dir_path = os.path.join(settings.UPLOAD_DIR, store_dir)
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		file_path = os.path.join(dir_path, file_name)

		#写图片文件内容
		dst_file = open(file_path, 'wb')
		print >> dst_file, ''.join(content)
		dst_file.close()

		#保存图片信息到mysql中

		image_path = '/static/upload/%s/%s' % (store_dir, file_name)
		value = save_and_zip_base64_img_file_for_mobileApp(request, file_name,image_path)
		print value,"============"

		image = models.Image.objects.create(
			user = request.user,
			path = image_path
		)

		response = create_response(200)
		response.data = {
			'id': image.id,
			'path': image_path
		}
		return response.get_response()

########################################################################
# save_and_zip_base64_img_file_for_mobileApp: 存储手机上传的图片压缩大于1M的图片
########################################################################
def save_and_zip_base64_img_file_for_mobileApp(request, file_name, ajax_path):
	date = time.strftime('%Y%m%d')
	dir_path_suffix = 'panda/%d_%s' % (request.user.id, date)
	# dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)
	# if not os.path.exists(dir_path):
	# 	os.makedirs(dir_path)

	# #获取文件的扩展名
	# file_name = '%s.%s' % (time.strftime("%Y_%m_%d_%H_%M_%S"), 'png')
	# ajax_path = '%s/%s' % (dir_path, file_name)
	# # ajax_file = ajax_file.split(',')
	# try:
	# 	print ajax_file,"======2=2=22=2=22==2=="
	# 	image_content = base64.b64decode(ajax_file)
	# 	print image_content,"=====333333333=="
	# 	file = open(ajax_path, 'wb')
	# 	file.write(image_content)
	# 	file.close()
	# 	image_file = Image.open(ajax_path)
	# 	max_height = 640.0
	# 	max_width = 480.0
	# 	ori_width,ori_height = image_file.size
	# 	h_ratio = w_ratio = 1
	# 	ratio = 1
	# 	if ori_height>max_height or ori_width>max_width:
	# 		if ori_height>max_height:
	# 			h_ratio = max_height/ori_height
	# 		if ori_width>max_width:
	# 			w_ratio = max_width/ori_width
	# 		if h_ratio > w_ratio:
	# 			ratio = w_ratio
	# 		else:
	# 			ratio = h_ratio
	# 		new_width = int(ori_width*ratio)
	# 		new_height = int(ori_height*ratio)
	# 		image_file.resize((new_width,new_height),Image.ANTIALIAS).save(ajax_path)
	# 	new_img_file = Image.open(ajax_path)
	# except Exception,e:
	# 	print unicode_full_stack(),e
	# 	raise

	# if __validate_image(ajax_path):
	try:
		image_path = upload_image_to_upyun(ajax_path,'/upload/%s/%s' % (dir_path_suffix, file_name))
		print image_path,"==========ttttt44========"
		return image_path
	except:
		notify_msg = u"上传图片到又拍云时失败, cause:\n{}".format(unicode_full_stack())
		watchdog_error(notify_msg)
		return '/static/upload/%s/%s' % (dir_path_suffix, file_name)
		#return '/static/upload/%s/%s' % (dir_path_suffix, file_name)
	# else:
	# 	return None

image_path = "http://%s.b0.upaiyun.com%s"
def upload_image_to_upyun(file_path, upyun_path):
	if settings.MODE == 'develop':
		return '/static%s' % upyun_path
		
	up = upyun.UpYun(BUCKETNAME, USERNAME, PASSWORD, timeout=300,
			endpoint=upyun.ED_AUTO)
	#headers = {"x-gmkerl-rotate": "180"}
	try:
		with open(file_path, 'rb') as f:
			try:
				res = up.put(upyun_path, f)
			except:
				res = up.put(upyun_path, f)
			
			return image_path % (BUCKETNAME, upyun_path)
	except:
		notify_message = u"upload_image_to_upyun error {}".format(unicode_full_stack())
		watchdog_error(notify_message)
		return '/static%s' % upyun_path
	return None

########################################################################
# __validate_image: 检查上传的文件格式是否正确
########################################################################
def __validate_image(path):
	try:
		print path,"==========222222========"
		im = Image.open(path)
		im.load()
		return True
		#image is validate
	except:
		import sys
		import traceback
		type, value, tb = sys.exc_info()
		print type
		print value
		traceback.print_tb(tb)
		if 'image file is truncated' in str(value):
			return False
		else:
			return False