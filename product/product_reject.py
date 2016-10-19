# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack
from eaglet.core import watchdog

from account.models import *
import models
from util import send_product_message


class ProductReject(resource.Resource):
	app = 'product'
	resource = 'product_reject'

	@login_required
	def api_post(request):
		#运营查看商品列表，入库驳回
		product_ids = request.POST.get('product_id',-1)
		reasons = request.POST.get('reasons','')
		data = {}
		product_ids = product_ids.split(',')
		try:
			for product_id in product_ids:
				product_id = int(product_id)
				models.Product.objects.filter(id=product_id).update(is_refused=True)
				models.ProductRejectLogs.objects.create(
					product_id = product_id,
					reject_reasons = reasons
				)
				try:
					send_product_message.send_reject_product_change(product_id=product_id)
				except:
					msg = unicode_full_stack()
					watchdog.error("product_reject.send_reject_product_change: {}".format(msg))
			data['code'] = 200
			response = create_response(200)
		except:
			data['code'] = 500
			response = create_response(500)
			response.errMsg = u'驳回失败'
		response.data = data
		return response.get_response()