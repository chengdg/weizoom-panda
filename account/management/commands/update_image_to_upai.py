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

import urllib
import re
#####################################
#将老数据上传到upai云
#####################################
class Command(BaseCommand):
	def handle(self, **options):
		USERNAME = 'weizoom'
		PASSWORD = 'weizoom_weapp'
		BUCKETNAME = 'weappimg'
		images = resource_models.Image.objects.filter(path__contains='http://chaozhi.weizoom.com')
		print images.count()
		for image in images:
			path = image.path
			print path
			cur_path = path.split('http://chaozhi.weizoom.com')
			if len(cur_path) >1:
				upyun_path = 'http://weappimg.b0.upaiyun.com'+cur_path[1]				

				dir_path = os.path.abspath('.')+ '/static/upload/' + path.split('/')[-2]
				if not os.path.exists(dir_path):
					os.makedirs(dir_path)
				file_name = path.split('/')[-1]
				file_path = os.path.abspath('.')+ '/static/upload/'+ path.split('/')[-2]+'/' +file_name
				urllib.urlretrieve(path,file_path)

				up = upyun.UpYun(BUCKETNAME, USERNAME, PASSWORD, timeout=300,endpoint=upyun.ED_AUTO)
				with open(file_path, 'rb') as f:
					res = up.put(cur_path[1], f)
					image.path = upyun_path
					image.save()

