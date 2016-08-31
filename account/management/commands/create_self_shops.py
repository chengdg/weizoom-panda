# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from eaglet.utils.resource_client import Resource
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST

from self_shop import models as self_shop_models
from account import models as account_models


class Command(BaseCommand):

    def handle(self, **options):
        """
        把已经存在的自营平台到自营平台管理表中
        """
        selfShops = [{
            'name': u'微众白富美',
            'value': 'weizoom_baifumei'
        },{
            'name': u'微众俱乐部',
            'value': 'weizoom_club'
        },{
            'name': u'微众家',
            'value': 'weizoom_jia'
        },{
            'name': u'微众妈妈',
            'value': 'weizoom_mama'
        },{
            'name': u'微众商城',
            'value': 'weizoom_shop'
        },{
            'name': u'微众学生',
            'value': 'weizoom_xuesheng'
        },{
            'name': u'微众Life',
            'value': 'weizoom_life'
        },{
            'name': u'微众一家人',
            'value': 'weizoom_yjr'
        },{
            'name': u'惠惠来啦',
            'value': 'weizoom_fulilaile'
        },{
            'name': u'居委汇',
            'value': 'weizoom_juweihui'
        },{
            'name': u'微众中海',
            'value': 'weizoom_zhonghai'
        },{
            'name': u'微众club',
            'value': 'weizoom_zoomjulebu'
        },{
            'name': u'微众吃货',
            'value': 'weizoom_chh'
        },{
            'name': u'微众圈',
            'value': 'weizoom_pengyouquan'
        },{
            'name': u'少先队',
            'value': 'weizoom_shxd'
        },{
            'name': u'津美汇',
            'value': 'weizoom_jinmeihui'
        },{
            'name': u'微众便利店',
            'value': 'weizoom_wzbld'
        },{
            'name': u'微众佳人',
            'value': 'weizoom_jiaren'
        },{
            'name': u'微众良乡商城',
            'value': 'weizoom_xiaoyuan'
        },{
            'name': u'微众精英',
            'value': 'weizoom_jy'
        },{
            'name': u'爱尔康',
            'value': 'weizoom_aierkang'
        },{
            'name': u'开发测试',
            'value': 'devceshi'
        },{
            'name': u'财务测试',
            'value': 'caiwuceshi'
        }]
        for selfShop in selfShops:
            print selfShop['name']
            self_shop_models.SelfShops.objects.create(
                self_shop_name = selfShop['name'],
                user_name = selfShop['value']
                )