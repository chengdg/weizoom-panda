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
import models

SELF_NAMETEXT2VALUE = {
    u'微众家': 'weizoom_jia',
    u'微众妈妈': 'weizoom_mama' ,
    u'微众学生': 'weizoom_xuesheng',
    u'微众白富美': 'weizoom_baifumei',
    u'微众商城': 'weizoom_shop',
    u'微众俱乐部': 'weizoom_club',
    u'微众Life': 'weizoom_life',
    u'微众一家人': 'weizoom_yjr'
}

SELF_SHOP2TEXT = {
    'weizoom_jia': u'微众家',
    'weizoom_mama': u'微众妈妈',
    'weizoom_xuesheng': u'微众学生',
    'weizoom_baifumei': u'微众白富美',
    'weizoom_shop': u'微众商城',
    'weizoom_club': u'微众俱乐部',
    'weizoom_life': u'微众Life',
    'weizoom_yjr': u'微众一家人'
}

# # 对应云上通的自营平台账户id(user_id)
# SELF_SHOP2WEAPP_SHOP = {
#     'weizoom_jia': 3,
#     'weizoom_mama': 5,
#     'weizoom_xuesheng': 2,
#     'weizoom_baifumei': 4,
#     'weizoom_shop': 6,
#     'weizoom_club': 7
# }

class ProductRelation(resource.Resource):
    app = 'product'
    resource = 'weapp_relation'

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
            # print ('+++++++++++++++++product_data', product_data)

            if product_data:
                # 当前平台的的供应商账户（账户id)
                # 获取当前供货商的对应的weapp供货商的id
                account_id = product_data[0].get('account_id')
                account_has_supplier = AccountHasSupplier.objects.filter(account_id=account_id).first()
                if account_has_supplier:
                    weapp_supplier_id = account_has_supplier.supplier_id

                    # 获取商品（从数据库查询）
                    product_id = product_data[0].get('product_id')
                    product = models.Product.objects.get(id=product_id)
                    # 发送请求
                    # 获取商品图片
                    image_ids = [image.image_id for image in models.ProductImage.objects.filter(product_id=product_id)]
                    images = [{"order": 1, "url": i.path} for i in Image.objects.filter(id__in=image_ids)]

                    # 获取商品要同步到哪个平台

                    weizoom_self = product_data[0].get('weizoom_self').split(',')

                    weapp_user_ids = [k.weapp_account_id for k in models.SelfUsernameWeappAccount.objects
                        .filter(self_user_name__in=weizoom_self)]
                    # print weapp_user_ids
                    params = {
                        'supplier': weapp_supplier_id,
                        'name': product.product_name,
                        'promotion_title': product.promotion_title if product.promotion_title else '',
                        'purchase_price': product.clear_price,
                        'price': product.product_price,
                        'weight': product.product_weight,
                        'stock_type': 'unbound' if product.product_store == -1 else product.product_store,
                        'images': json.dumps(images),
                        'product_id': product_id,
                        'model_type': 'single',
                        'stocks': product.product_store if product.product_store > 0 else 0,
                        # 商品需要同步到哪个自营平台
                        'accounts': json.dumps(weapp_user_ids),
                        'detail': product.remark
                    }
                    # 判断是更新还是新曾商品同步
                    relations = models.ProductHasRelationWeapp.objects.filter(product_id=product_id)
                    if relations.count() == 0:
                        resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).put({
                            'resource': 'mall.product',
                            'data': params
                        })
                        # 同步到商品中间关系表
                        if resp:
                            if resp.get('code') == 200:
                                weapp_product_id = resp.get('data').get('product').get('id')
                                models.ProductHasRelationWeapp.objects.create(
                                    product_id=product.id,
                                    weapp_product_id=weapp_product_id,
                                    self_user_name=request.user.username
                                )
                                # 更新同步到哪个平台了映射关系
                                sync_models = [models.ProductSyncWeappAccount(product_id=product.id,
                                                                              self_user_name=username)
                                               for username in weizoom_self]
                                models.ProductSyncWeappAccount.objects.bulk_create(sync_models)
                                if product.has_limit_time:
                                    # TODO 同步限时抢购
                                    pass

                    else:
                        relation = relations.first()
                        if relation:
                            params = {
                                'name': product.product_name,
                                'promotion_title': product.promotion_title,
                                'purchase_price': product.clear_price,
                                'price': product.product_price,
                                'weight': product.product_weight,
                                'stock_type': 'unbound' if product.product_store == -1 else product.product_store,
                                'swipe_images': json.dumps(images),
                                'product_id': relation.weapp_product_id,
                                'model_type': 'single',
                                'stocks': product.product_store if product.product_store > 0 else 0,
                                # 商品需要同步到哪个自营平台
                                'accounts': json.dumps(weapp_user_ids),
                                'detail': product.remark,
                            }
                            resp = Resource.use(ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST).post({
                                'resource': 'mall.product',
                                'data': params
                            })
                            if resp:
                                # 先删除数据
                                models.ProductSyncWeappAccount.objects.filter(product_id=product.id,).delete()
                                sync_models = [models.ProductSyncWeappAccount(product_id=product.id,
                                                                              self_user_name=username)
                                               for username in weizoom_self]
                                models.ProductSyncWeappAccount.objects.bulk_create(sync_models)

                data['code'] = 200
                data['errMsg'] = u'关联成功'
        except:
            msg = unicode_full_stack()
            response.innerErrMsg = msg
            watchdog.error(msg)
        relations = {}
        data['rows'] = relations
        #构造response
        response.data = data
        return response.get_response()

    @login_required
    def api_delete(request):
        product_id = request.POST.get('product_id','')
        self_name = request.POST.get('self_name',0)
        if product_id:
            models.ProductSyncWeappAccount.objects.filter(product_id=int(product_id),self_user_name=self_name).delete()
        response = create_response(200)
        return response.get_response()
