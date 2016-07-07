# -*- coding: utf-8 -*-
import json
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from core import resource
from core.jsonresponse import create_response
from core import paginator

from util import string_util
from account import models as account_models
from panda.settings import ZEUS_HOST
from util import db_util
import models as fans_models
import nav
import requests

filter2field ={
	'status': 'status',
	'recommend_time': 'recommend_time'
}

FIRST_NAV = 'fans'
SECOND_NAV = 'fans'

class Fans(resource.Resource):
	app = 'fans'
	resource = 'fans'

	@login_required
	def get(request):
		"""
		显示商品列表
		"""
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': nav.get_second_navs(),
			'second_nav_name': SECOND_NAV
		})
		
		return render_to_response('fans/fans.html', c)

	def api_get(request):
		cur_page = request.GET.get('page', 1)
		filter_idct = dict([(db_util.get_filter_key(key, filter2field), db_util.get_filter_value(key, request)) for key in request.GET if key.startswith('__f-')])
		status = filter_idct.get('status',-1)
		# recommend_time = filter_idct.get('recommend_time__range','')
		user_has_fans = fans_models.UserHasFans.objects.filter(user_id=request.user.id)
		#查询
		if status != -1:
			user_has_fans = user_has_fans.filter(status=status)
		# if recommend_time:
		# 	recommend_time_start = recommend_time[0]
		# 	recommend_time_end = recommend_time[1]
		# 	user_has_fans = user_has_fans.filter(pushed_date__gte=recommend_time_start,pushed_date__lte=recommend_time_end)
		pageinfo, user_has_fans = paginator.paginate(user_has_fans, cur_page, 10, query_string=request.META['QUERY_STRING'])
		fans_id = [fans.fans_id for fans in user_has_fans]
		fans = fans_models.Fans.objects.filter(id__in=fans_id)
		fans_id2fans = {fan.id:fan for fan in fans}

		rows=[]
		i = 0
		for user_fans in user_has_fans:
			if user_fans.fans_id in fans_id2fans:
				fans = fans_id2fans[user_fans.fans_id]
				status = user_fans.status
				rows.append({
					# 'recommend_time': user_fans.pushed_date.strftime("%Y-%m-%d"),
					'fans_pic': fans.fans_url,
					'fans_id': fans.weibo_id,
					'purchase_index': fans.purchasing_index * 10,
					'diffusion_index': fans.spread_index * 10,
					'status': fans_models.STATUS2NAME[status],
					'order_id': user_fans.related_order_id
				})
		data = {
			'rows': rows,
			'pagination_info': pageinfo.to_dict()
		}
		response = create_response(200)
		response.data = data
		return response.get_response()