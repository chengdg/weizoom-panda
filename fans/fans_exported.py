# -*- coding: utf-8 -*-
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from core import resource
from excel_response import ExcelResponse
import models as fans_models

class FansExported(resource.Resource):
	app = 'fans'
	resource = 'fans_exported'

	def get(request):
		user_has_fans = fans_models.UserHasFans.objects.filter(user_id=139)
		fans_ids = [fans.fans_id for fans in user_has_fans]
		fans = fans_models.Fans.objects.filter(id__in=fans_ids)
		titles = [
			u'昵称', u'购买指数',u'推荐传播指数'
		]
		table = []
		table.append(titles)
		for fan in fans:
			table.append([
				fan['name'],
				fan['purchasing_index'],
				fan['spread_index']
			])

		return ExcelResponse(table,output_name=u'粉丝投放统计列表'.encode('utf8'),force_csv=False)