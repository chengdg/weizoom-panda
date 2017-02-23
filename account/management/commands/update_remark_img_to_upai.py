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
from product import models as product_models

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
		products = product_models.Product.objects.filter(remark__contains='http://chaozhi.weizoom.com')

		pat = '[p|/]>\n*<img src="(.*?)"'
		for product in products:
			remark = product.remark
			src_lists = re.findall(pat, remark, re.M)
			for src_list in src_lists:
				cur_path = src_list.split('http://chaozhi.weizoom.com')
				if len(cur_path) >1:				
					dir_path = os.path.abspath('.')+ '/static/upload/' + cur_path[1].split('/')[-2]
					if not os.path.exists(dir_path):
						os.makedirs(dir_path)
					file_name = cur_path[1].split('/')[-1]
					file_path = dir_path+'/' +file_name
					urllib.urlretrieve(str(src_list),file_path)

					up = upyun.UpYun(BUCKETNAME, USERNAME, PASSWORD, timeout=300,endpoint=upyun.ED_AUTO)
					with open(file_path, 'rb') as f:
						res = up.put(cur_path[1], f)

			update_remark = remark.replace('http://chaozhi.weizoom.com','http://weappimg.b0.upaiyun.com')
			product.remark = update_remark
			product.save()
