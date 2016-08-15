# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack
from eaglet.core import watchdog

from account.models import *
from eaglet.utils.resource_client import Resource
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST
from resource.models import Image
from panda.settings import PANDA_HOST
import models

class BatchSync(resource.Resource):
	app = 'product'
	resource = 'batch_sync'

	@login_required
	def api_post(request):
		product_ids = request.POST.get('product_ids','')
		print product_ids.split(','),"=========="
		product_ids = product_ids.split(',')
		response = create_response(200)
		data = {}
		response.data = data
		return response.get_response()