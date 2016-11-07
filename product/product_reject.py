# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack
from eaglet.core import watchdog

from account.models import *
import models
from django.contrib.auth.models import User
from util import send_product_message
from util import add_customer_news


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
				cur_product = models.Product.objects.filter(id=product_id)
				cur_product.update(is_refused=True)
				models.ProductRejectLogs.objects.create(
					product_id = product_id,
					reject_reasons = reasons
				)
				try:
					send_product_message.send_reject_product_change(product_id=product_id)
					send_product_message.send_reject_product_ding_message(product_id=product_id, reasons=reasons)

					# 给客户系统发送日志消息
					owner_id = cur_product[0].owner_id;
					customer_id = UserProfile.objects.get(user_id=owner_id).corpid
					customer_name = User.objects.get(id=customer_id).username
					add_customer_news.send_reject_product_message(product_name=cur_product[0].product_name, reject_reason=reasons, customer_id=customer_id, customer_name=customer_name)
				except:
					msg = unicode_full_stack()
					watchdog.error("product_reject.send_reject_product_change: {}".format(msg))
					print msg

			data['code'] = 200
			response = create_response(200)
		except:
			data['code'] = 500
			response = create_response(500)
			response.errMsg = u'驳回失败'
		response.data = data
		return response.get_response()