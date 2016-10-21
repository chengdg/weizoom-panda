# -*- coding: utf-8 -*-
import json
import requests
from hashlib import md5
import base64


url = 'http://testapi.kdniao.cc:8081/api/eorderservice'

headers = {'content-type': 'application/json'}

post_data = {
    "OrderCode": "PM20160406234133",
    "ShipperCode": "SF",
    "PayType": 1,
    "ExpType": 1,
    "Sender": {
        "Name" : "李先生",
        "Mobile" : "18888888888",
        "ProvinceName" : "李先生",
        "CityName" : "深圳市",
        "ExpAreaName" : "福田区",
        "Address" : "赛格广场5401AB"
    },
    "Receiver":{
        "Name" : "李先生",
        "Mobile" : "18888888888",
        "ProvinceName" : "李先生",
        "CityName" : "深圳市",
        "ExpAreaName" : "福田区",
        "Address" : "赛格广场5401AB"
    },
    "Commodity": [{
        "GoodsName" : "其他"
    }],
    "IsReturnPrintTemplate": 1
}

DataSign = base64.b64encode(md5(json.dumps(post_data) + "6642ea21-2d79-4ebc-a451-de4922dcf412").hexdigest())

params = {
        "RequestData": json.dumps(post_data),
        "EBusinessID": "1256042",
        "RequestType": "1007",
        "DataSign": DataSign,
        "DataType": "2"
        }


response = requests.post(url, data=json.dumps(params), headers=headers)
response_data = response.json()
#print response_data['PrintTemplate']
with open('order.html', 'w') as f:
    print_template = response_data['PrintTemplate']
    print print_template.encode('utf-8')
    f.write(print_template.encode('utf-8'))
    f.close()
    print "success"