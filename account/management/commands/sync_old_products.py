# -*- coding: utf-8 -*-
# __author__ = 'charles'

from django.core.management.base import BaseCommand
from eaglet.utils.resource_client import Resource
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST

from product import models as product_models
from account import models as account_models
from resource.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        同步旧的没有同步过得商品
        """
        # product_models.A.objects.filter()

        # user_id = models.IntegerField(default=0)  # 对应自营平台user_id
        # account_id = models.IntegerField(default=0)  # UserProfile id
        # supplier_id = models.IntegerField(default=0)  # 云上通的供货商id
        # store_name = models.CharField(max_length=1024, default='')  # y供货商名称
        products = product_models.Product.objects.filter()
        # 获取用户名和对应云上通的user_id(兼容老版本）
        username_to_account = product_models.SelfUsernameWeappAccount.objects.all()
        usernames = [u.self_user_name for u in username_to_account]
        weapp_account_id = [u.weapp_account_id for u in username_to_account]
        username_to_account_id = dict(zip(usernames, weapp_account_id))
        for product in products:
            owner_id = product.owner_id
            account_supplier = account_models.AccountHasSupplier.objects.filter(user_id=owner_id).first()
            if account_supplier:
                weapp_supplier_id = account_supplier.supplier_id
                image_ids = [image.image_id for image in
                             product_models.ProductImage.objects.filter(product_id=product.id)]
                images = [{"order": 1, "url": i.path} for i in Image.objects.filter(id__in=image_ids)]
                # 获取商品同步到哪个平台了
                relations = product_models.ProductHasRelationWeapp.objects.filter(product_id=product.id)
                # if not relations:
                #     continue

                self_user_names = [relation.self_user_name for relation in relations]
                weapp_user_ids = []
                for username in self_user_names:
                    weapp_user_ids.append(username_to_account_id.get(username))

                # print '++++++++++++++++++++++++++++', product.id, self_user_names, weapp_user_ids
                # if not self_user_names:
                #     self_user_names = ['weizoom_jia', 'weizoom_mama', 'weizoom_xuesheng']
                # if not weapp_user_ids:
                #     weapp_user_ids = [3,5,2]
                params = {
                    'supplier': weapp_supplier_id,
                    'name': product.product_name,
                    'promotion_title': product.promotion_title if product.promotion_title else '',
                    'purchase_price': product.clear_price,
                    'price': product.product_price,
                    'weight': product.product_weight,
                    'stock_type': 'unbound' if product.product_store == -1 else product.product_store,
                    'images': json.dumps(images),
                    'product_id': product.id,
                    'model_type': 'single',
                    'stocks': product.product_store if product.product_store > 0 else 0,
                    # 商品需要同步到哪个自营平台
                    'accounts': json.dumps(weapp_user_ids)
                }
                resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put({
                    'resource': 'mall.product',
                    'data': params
                })
                if resp:

                    if resp.get('code') == 200 and resp.get('data'):
                        ids = product_models.ProductHasRelationWeapp.objects.filter(product_id=product.id)\
                            .values('id')

                        if ids:
                            ids = [i.get('id') for i in ids]
                        print ids
                        if ids:
                            product_id = product.id
                            product_models.ProductHasRelationWeapp.objects.filter(id__in=ids)\
                                .update(product_id=-product_id)

                        weapp_product_id = resp.get('data').get('product').get('id')
                        # for user_name in self_user_names:
                        product_models.ProductHasRelationWeapp.objects.create(
                            product_id=product.id,
                            weapp_product_id=weapp_product_id,
                            self_user_name=''
                        )
                        # 更新同步到哪个平台了映射关系
                        sync_models = [product_models.ProductSyncWeappAccount(product_id=product.id,
                                                                              self_user_name=username)
                                       for username in self_user_names]
                        product_models.ProductSyncWeappAccount.objects.bulk_create(sync_models)

                        print 'product_id: %s is success!' % product.id
                    else:
                        print 'product_id: %s is failed!' % product.id
                else:
                    print 'product_id: %s is failed!' % product.id
