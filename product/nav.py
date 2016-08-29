# -*- coding: utf-8 -*-
__author__ = 'hj'
from product.models import *
from account.models import *

def get_second_navs(request):
	user_profile = UserProfile.objects.get(user_id=request.user.id)
	role = user_profile.role
	if role == YUN_YING:
		sync_product_ids = []
		product_sync_weapps = ProductSyncWeappAccount.objects.all()
		for product_sync_weapp in product_sync_weapps:
			if product_sync_weapp.product_id not in sync_product_ids:
				sync_product_ids.append(product_sync_weapp.product_id)
		product_updated_count = Product.objects.filter(id__in=sync_product_ids, is_update=True, is_deleted=False).count()
		if product_updated_count > 0:
			title = '商品更新('+str(product_updated_count)+')'
		else:
			title = '商品更新'
		SECOND_NAVS = [{
			'name': 'product-relation-list',
			'displayName': '商品',
			'href': '/product/product_relation/'
		},{
			'name': 'product-update-list',
			'displayName': title,
			'href': '/product/product_updated/'
		}]
	else:
		SECOND_NAVS = [{
			'name': 'product-list',
			'displayName': '商品',
			'href': '/product/product_list/'
		},{
			'name': 'product-model',
			'displayName': '商品规格管理',
			'href': '/product/product_model/'
		}]
	return SECOND_NAVS