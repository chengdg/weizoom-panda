# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from core.exceptionutil import unicode_full_stack
from core import resource
from core.jsonresponse import create_response


class ChangePassword(resource.Resource):
	"""
	修改密码
	"""
	app = 'account'
	resource = 'change_pwd'
	
	@login_required
	def api_put(request):
		old_pwd = request.POST.get('old_pwd', '')
		new_pwd = request.POST.get('new_pwd', '')
		user_id = int(request.user.id)
		try:
			user = User.objects.get(id=user_id)
			if user.check_password(old_pwd):
				user.set_password(new_pwd)
				user.save()
				response = create_response(200)
			else:
				response = create_response(500)
				response.errMsg = u'旧密码错误'
			return response.get_response()
		except:
			response = create_response(500)
			response.innerErrMsg = unicode_full_stack()
			response.errMsg = u'重置密码失败'
		return response.get_response()