# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog
from core import resource
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack
from util import string_util

from resource import models as resource_models
from account.models import *
import nav
import models
from panda.settings import EAGLET_CLIENT_ZEUS_HOST, ZEUS_SERVICE_NAME, SYNC_ACCOUNTS
from account.models import AccountHasSupplier

class UpdateProduct(resource.Resource):
    app = 'product'
    resource = 'update_product'

    @login_required
    def api_post(request):
    	product_id = request.POST.get('product_id',0)
    	response = create_response(200)
    	data = {}
    	data['code'] = 500
        data['errMsg'] = u'更新失败'
        print product_id,"========="
        try:
        	data['code'] = 200
        	data['errMsg'] = u'更新成功'
        except:
        	response.innerErrMsg = unicode_full_stack()
        response.data = data
        return response.get_response()