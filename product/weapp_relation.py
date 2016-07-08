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
from core.exceptionutil import unicode_full_stack

from util import db_util
from resource import models as resource_models
from account.models import *
from util import string_util
from panda.settings import ZEUS_HOST
import nav
import models
import requests

SELF_NAMETEXT2VALUE = {
	u'微众家': 'weizoom_jia',
	u'微众妈妈': 'weizoom_mama' ,
	u'微众学生': 'weizoom_xuesheng',
	u'微众白富美': 'weizoom_baifumei',
	u'微众商城': 'weizoom_shop',
	u'微众俱乐部': 'weizoom_club'
}

SELF_SHOP2TEXT = {
	'weizoom_jia': u'微众家',
	'weizoom_mama': u'微众妈妈',
	'weizoom_xuesheng': u'微众学生',
	'weizoom_baifumei': u'微众白富美',
	'weizoom_shop': u'微众商城',
	'weizoom_club': u'微众俱乐部'
}

class ProductRelation(resource.Resource):
	app = 'product'
	resource = 'weapp_relation'

	@login_required
	def api_get(request):
		product_id = request.GET.get('product_id',0)
		product_relations = models.ProductHasRelationWeapp.objects.filter(product_id=product_id).order_by('self_user_name')
		#组装数据
		relations = {}
		if product_relations:
			for product in product_relations:
				relations[product.self_user_name] = product.weapp_product_id
		data = {
			'rows': relations
		}
		#构造response
		response = create_response(200)
		response.data = data
		return response.get_response()

	@login_required
	def api_post(request):
		product_data = request.POST.get('product_data',0)
		account_has_suppliers = AccountHasSupplier.objects.all()
		user_id2store_name = {account_has_supplier.user_id:account_has_supplier.store_name for account_has_supplier in account_has_suppliers}
		product_data = '' if not product_data else json.loads(product_data)
		response = create_response(200)
		data = {}
		data['code'] = 500
		data['errMsg'] = u'关联失败'
		try:
			if product_data:
				sync_product_datas = []
				account_id = product_data[0]['account_id']
				product_id = product_data[0]['product_id']
				weizoom_self = product_data[0]['weizoom_self'].split(',')
				weizoom_self_text = []
				for name in weizoom_self:
					weizoom_self_text.append(SELF_SHOP2TEXT[name])
				account_has_suppliers = AccountHasSupplier.objects.filter(account_id=account_id,store_name__in=weizoom_self_text)
				supplier_ids = []
				user_ids = []
				for account_has_supplier in account_has_suppliers:
					supplier_id = str(account_has_supplier.supplier_id)
					user_id = str(account_has_supplier.user_id)
					supplier_ids.append(supplier_id)
					user_ids.append(user_id)

				image_paths = product_data[0]['image_path'].split(',')
				swipe_images = []
				if image_paths:
					for image_path in image_paths:
						swipe_images.append({
							'id': -1,
							'url': '%s' %image_path,
							'width': 100,
							'height': 100
						})
				print ('+++user_ids+++:',user_ids)
				print ('+++suppliers+++:',supplier_ids)
				product_price = float(product_data[0]['product_price'])
				stock_type = 1 if int(product_data[0]['product_store']) > -1 else 0
				params = {
					'owner_ids': '_'.join(user_ids),#所属账号的user id
					'suppliers': '_'.join(supplier_ids),#供货商 id
					'name': product_data[0]['product_name'],
					'purchase_price': product_data[0]['clear_price'],
					'stock_type': stock_type,
					'promotion_title': product_data[0]['promotion_title'],
					'price': product_price if product_price > -1 else '',
					'weight': product_data[0]['product_weight'],
					'stocks': product_data[0]['product_store'],
					'detail': product_data[0]['detail'],
					'swipe_images': '' if not swipe_images else json.dumps(swipe_images)
				}
				r = requests.post(ZEUS_HOST+'/mall/sync_product/?_method=put',params=params)
				print ('+++r+++:',r)
				res = json.loads(r.text)
				if res['code'] == 200:
					sync_product_datas = res['data']
					if sync_product_datas:
						list_create = []
						for sync_product_data in sync_product_datas:
							owner_id = sync_product_data['owner_id']
							name = '' if int(owner_id) not in user_id2store_name else user_id2store_name[int(owner_id)]
							if name in SELF_NAMETEXT2VALUE.keys() and SELF_NAMETEXT2VALUE[name] in weizoom_self:
								list_create.append(models.ProductHasRelationWeapp(
									product_id = product_id,
									self_user_name = SELF_NAMETEXT2VALUE[name],
									weapp_product_id = sync_product_data['product_id']
								))
								data['code'] = 200
								data['errMsg'] = u'关联成功'

						models.ProductHasRelationWeapp.objects.bulk_create(list_create)
						if data['code'] == 200:
							product_has_relations = models.ProductHasRelationWeapp.objects.exclude(weapp_product_id='')
							product_has_relations = product_has_relations.filter(product_id=product_id)
							if len(product_has_relations)>0:
								models.Product.objects.filter(id=product_id).update(product_status=1)#{0:未上架,1:已上架}
							else:
								models.Product.objects.filter(id=product_id).update(product_status=0)
				else:
					print(res)
					print("==========")
					
		except Exception,e:
			print(e)
			print("++++++++++++")
			response.innerErrMsg = unicode_full_stack()

		relations = {}
		data['rows'] = relations
		#构造response
		response.data = data
		return response.get_response()

	@login_required
	def api_put(request):
		post = request.POST
		relations = post.get('relations','')
		product_id = post.get('product_id','')
		try:
			if relations:
				models.ProductHasRelationWeapp.objects.filter(product_id=product_id).delete()
				relations=json.loads(relations)
				list_create = []
				for (k,v) in relations[0].items():
					list_create.append(models.ProductHasRelationWeapp(
						product_id = product_id,
						self_user_name = k,
						weapp_product_id = v
					))
				models.ProductHasRelationWeapp.objects.bulk_create(list_create)

				product_has_relations = models.ProductHasRelationWeapp.objects.exclude(weapp_product_id='')
				product_has_relations = product_has_relations.filter(product_id=product_id)
				if len(product_has_relations)>0:
					models.Product.objects.filter(id=product_id).update(product_status=1)#{0:未上架,1:已上架}
				else:
					models.Product.objects.filter(id=product_id).update(product_status=0)
			response = create_response(200)
			response.data.code = 200
			response.data.Msg = u'关联成功'
		except:
			response = create_response(500)
			response.data.code = 500
			response.innerErrMsg = unicode_full_stack()
			response.data.Msg = u'关联失败'
		return response.get_response()