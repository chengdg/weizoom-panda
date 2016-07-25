# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from util import db_util
from resource import models as resource_models
from account.models import *
from util import string_util
from panda.settings import ZEUS_HOST
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
from eaglet.utils.resource_client import Resource

def sales_from_weapp(product_has_relations):
	product_ids = []
	product_weapp_id2product_id = {}
	for product_has_relation in product_has_relations:
		weapp_product_ids = product_has_relation.weapp_product_id.split(';')
		for weapp_product_id in weapp_product_ids:
			#获得所有绑定过云商通的云商通商品id
			product_ids.append(weapp_product_id)
			#构造panda数据库内商品id，与云商通内商品id的关系
			product_weapp_id2product_id[weapp_product_id] = product_has_relation.product_id

	#请求接口获得数据
	id2sales = {}
	product_ids = '_'.join(product_ids)
	if product_ids:
		try:
			params = {
				'product_ids': product_ids
			}
			resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).get({
				'resource': 'mall.product_sales',
				'data': params
			})
			# r = requests.get(ZEUS_HOST+'/mall/product_sales/',params=params)
			# res = json.loads(r.text)
			if resp and resp['code'] == 200:
				product_sales = resp['data']['product_sales']
				if product_sales:
					for product_sale in product_sales:
						product_id = str(product_sale['product_id'])
						if product_id in product_weapp_id2product_id:
							p_id = product_weapp_id2product_id[product_id]
							p_sales = product_sale['sales']
							if p_id not in id2sales:
								id2sales[p_id] = p_sales
							else:
								id2sales[p_id] += p_sales
			else:
				print(resp)
		except Exception,e:
			print(e)
	return id2sales