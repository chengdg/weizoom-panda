#author: 张雪 2016-5-25

Feature:精简版云商通-添加商品、删除商品
"""
	1.客户登录系统
	2.客户添加商品
	3.客户删除商品

	添加商品的文本框为必填项

"""
Background:
	Given jobs登录系统
	When jobs添加账号
	"""
		[{
			"account_type":"体验客户",
			"account_name":"爱昵咖啡",
			"login_account":"aini",
			"password":"123456"
		}]
	"""
@mall3 @weapp
Scenario:1 客户登录系统
	Given aini登录系统
	Then aini可以看到订单列表
	"""
		[]
	"""
	Then aini能获取商品列表
	"""
		[]
	"""


@mall3 @weapp
Scenario:2 客户添加商品
	Given aini登录系统
	When aini添加商品
	"""
		[{
			"name": "叫花鸡",
			"promotion_name":"促销的叫花鸡",
			"settlement_price":10.00,
			"pic_url": "./test/imgs/hangzhou1.jpg",
			"introduction": "叫花鸡的简介",
			"model": {
				"models": {
					"standard": {
						"price": 12.00,
						"weight": 1.00,
						"stock_type": "无限"
						}
					}
				}

		},{
			"name": "五花肉",
			"promotion_name":"促销的五花肉",
			"settlement_price":10.00,
			"pic_url": "./test/imgs/hangzhou1.jpg",
			"introduction": "叫花鸡的简介",
			"model": {
				"models": {
					"standard": {
						"price": 12.00,
						"weight": 1.00,
						"stock_type": "无限"
						}
					}
				}

		}]
	"""


	Then aini能获得商品列表
	"""
		[{
			"name": "五花肉",
			"sales":0,
			"status":"未上架",
			"actions":["编辑","彻底删除"]
		},{
			"name": "叫花鸡",
			"sales":0,
			"status":"未上架",
			"actions":["编辑","彻底删除"]
		}]
	"""



@mall3 @weapp
Scenario:3 客户删除商品
	Given aini登录系统
	When anni添加商品
	"""
		[{
			"name": "叫花鸡",
			"model": {
				"models": {
					"standard": {
						"price": 12.00,
						"weight": 1.00,
						"stock_type": "无限"
						}
					}
				}
		},{
			"name": "五花肉",
			"model": {
				"models": {
					"standard": {
						"price": 12.00,
						"weight": 1.00,
						"stock_type": "无限"
						}
					}
				}
		}]
	"""
	When aini删除商品'叫花鸡'
	Then aini能获得商品列表
	"""
		[{
			"name": "五花肉",
			"sales":0,
			"status":"未上架",
			"actions":["编辑","彻底删除"]
		}]
	"""

	

