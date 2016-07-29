# -*- coding: utf-8 -*-
__author__ = 'lihanyi'

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
from django.contrib.auth.models import User
from core import resource
from core.jsonresponse import create_response
from resource import models as models

class BusinessApply(resource.Resource):
	app = 'business'
	resource = 'customer_apply'

	def get(request):
		c = RequestContext(request, {
		})
		
		return render_to_response('business/business_apply_1.html', c)

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

class BusinessImage(resource.Resource):
    """
    图片
    """
    app = 'business'
    resource = 'upload_image'

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
    
    def post(request):
        file = request.FILES.get('image', None)

        #读取二进制内容
        content = []
        if file:
            for chunk in file.chunks():
                content.append(chunk)

        #获取存储图片的目录和文件信息
        file_name = BusinessImage.__get_file_name(file.name)
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
        image = models.Image.objects.create(
            user = User.objects.filter(is_staff=1).first(),
            path = image_path
        )

        response = create_response(200)
        response.data = {
            'id': image.id,
            'path': image_path
        }
        return response.get_response()
