# -*- coding: utf-8 -*-
__author__ = 'zph'

import json
import math
import os
import random
import time
import datetime
import requests
from collections import OrderedDict
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from resource import models as resource_models

import upyun

#####################################
#将老数据上传到upai云
#####################################
class Command(BaseCommand):
	def handle(self, **options):
		image_path = "http://%s.b0.upaiyun.com%s"
		USERNAME = 'weizoom'
		PASSWORD = 'weizoom_weapp'
		BUCKETNAME = 'weappimg'
		images = resource_models.Image.objects.all()
		for image in images:
			path = image.path
			cur_path = path.split('http://chaozhi.weizoom.com')
			if len(cur_path) >1:
				upyun_path = 'http://weappimg.b0.upaiyun.com'+cur_path[1]
			else:
				upyun_path = cur_path[0]
			image.path = upyun_path
			image.save()
			file_path ='http://chaozhi.weizoom.com' + upyun_path
			up = upyun.UpYun(BUCKETNAME, USERNAME, PASSWORD, timeout=300,endpoint=upyun.ED_AUTO)

			with open(file_path, 'rb') as f:
				try:
					res = up.put(upyun_path, f)
				except:
					print image.user,666666

