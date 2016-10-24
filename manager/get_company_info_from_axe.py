# -*- coding: utf-8 -*-
__author__ = 'lihanyi'

import json
import time
import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.exceptionutil import unicode_full_stack
from core import resource
from core.jsonresponse import create_response
from core import paginator
from util import db_util
import nav
import requests
from panda.settings import AXE_HOST

#从渠道获得公司信息
class GetCompanyInfoFromAxe(resource.Resource):
	app = 'manager'
	resource = 'get_company_info_from_axe'

	@login_required
	def api_get(request):
		company_name = request.GET.get('companyName','')
		params = {
			'name': company_name
		}
		r = requests.post(AXE_HOST + '/api/customers/', data=params)
		res = json.loads(r.text)

		rows = []
		if res and res['code'] == 200:
			axe_datas = res['data']
			#因为reactman的FormSelect没有onClick事件，只有onChange事件，不添加第一个默认值的话无法触发onChange事件
			if len(axe_datas) > 0:
				rows.append({
					'text': '请选择已有公司',
					'value': ''+ '/' +''
				})
			for axe_data in axe_datas:
				for (k,v) in axe_data.items():
					rows.append({
						'text': v['name'],
						'value': v['contact']+ '/' +v['tel']  #把联系人、手机号通过“/”分割开传到前台
					})
		data = {
			'rows': rows
		}
		response = create_response(200)
		response.data = data
		return response.get_response()