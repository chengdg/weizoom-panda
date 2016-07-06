# -*- coding: utf-8 -*-
import json
import time

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

from account.models import *

class Accounts(resource.Resource):
	app = 'manager'
	resource = 'accounts'

	@login_required
	def api_get(request):
		user_profiles = UserProfile.objects.filter(role=CUSTOMER)
		account_has_suppliers = AccountHasSupplier.objects.filter(store_name__startswith='微众')
		users = User.objects.all()
		user_id2username = {user.id:user.username for user in users}

		account_id2supplier_ids = {}
		for account_has_supplier in account_has_suppliers:
			account_id = account_has_supplier.account_id
			supplier_id = str(account_has_supplier.supplier_id)
			if account_id not in account_id2supplier_ids:
				account_id2supplier_ids[account_id] = [supplier_id]
			else:
				account_id2supplier_ids[account_id].append(supplier_id)

		account_infos = []
		try:
			for user_profile in user_profiles:
				if user_profile.id in account_id2supplier_ids:
					supplier_ids = '' if user_profile.id not in account_id2supplier_ids else '_'.join(account_id2supplier_ids[user_profile.id])
					account_infos.append({
						'account_name': user_profile.name,
						'user_name': user_id2username[user_profile.user_id],
						'supplier_ids': supplier_ids
					})
			response = create_response(200)
			response.data = json.dumps(account_infos)
		except Exception,e:
			response = create_response(500)
			response.innerErrMsg = unicode_full_stack()
		return response.get_response()