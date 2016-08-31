# -*- coding: utf-8 -*-
# __author__ = 'charles'

from django.core.management.base import BaseCommand
from eaglet.utils.resource_client import Resource
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST

from self_shop import models as self_shop_models
from account import models as account_models


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        把已经存在的自营平台到自营平台管理表中
        """
        selfShop = [{
            'name': '微众白富美',
            'value': 'weizoom_baifumei'
        },{
            'name': '微众俱乐部',
            'value': 'weizoom_club'
        },{
            'name': '微众家',
            'value': 'weizoom_jia'
        },{
            'name': '微众妈妈',
            'value': 'weizoom_mama'
        },{
            'name': '微众商城',
            'value': 'weizoom_shop'
        },{
            'name': '微众学生',
            'value': 'weizoom_xuesheng'
        },{
            'name': '微众Life',
            'value': 'weizoom_life'
        },{
            'name': '微众一家人',
            'value': 'weizoom_yjr'
        },{
            'name': '惠惠来啦',
            'value': 'weizoom_fulilaile'
        },{
            'name': '居委汇',
            'value': 'weizoom_juweihui'
        },{
            'name': '微众中海',
            'value': 'weizoom_zhonghai'
        },{
            'name': '微众club',
            'value': 'weizoom_zoomjulebu'
        },{
            'name': '微众吃货',
            'value': 'weizoom_chh'
        },{
            'name': '微众圈',
            'value': 'weizoom_pengyouquan'
        },{
            'name': '少先队',
            'value': 'weizoom_shxd'
        },{
            'name': '津美汇',
            'value': 'weizoom_jinmeihui'
        },{
            'name': '微众便利店',
            'value': 'weizoom_wzbld'
        },{
            'name': '微众佳人',
            'value': 'weizoom_jiaren'
        },{
            'name': '微众良乡商城',
            'value': 'weizoom_xiaoyuan'
        },{
            'name': '微众精英',
            'value': 'weizoom_jy'
        }]


