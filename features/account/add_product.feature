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
#@panda
#Scenario:1 客户登录系统
#	Given aini登录系统
#	Then aini可以看到订单列表
#	"""
#		[]
#	"""
#	Then aini能获取商品列表
#	"""
#		[]
#	"""


@panda @hj
Scenario:2 客户添加商品
	Given aini登录系统
	When aini添加商品
	"""
		[{
			"name": "商品1",
			"promotion_name":"促销的商品1",
			"price": 12.00,
			"weight": 1.00,
			"stock_type": "无限"
			"settlement_price":10.00,
			"introduction": "商品1的简介"	
		},{
			"name": "商品2",
			"promotion_name":"促销的商品2",
			"settlement_price":10.00,
			"introduction": "商品2的简介",
			"price": 12.00,
			"weight": 1.00,
			"stock_type": "无限"

		},{
			"name": "商品3",
			"promotion_name":"促销的商品3",		
			"price": 12.00,
			"weight": 1.00,
			"stock_type": "无限"
			"settlement_price":10.00,
			"introduction": "商品3的简介",
		},{
			"name": "商品4",
			"promotion_name":"促销的商品4",
			"price": 12.00,
			"weight": 1.00,
			"stock_type": "无限"
			"settlement_price":10.00,
			"introduction": "商品4的简介",
			
		}]
	"""


	Then aini能获得商品列表
	"""
		[{
			"name": "商品3",
			"sales":0,
			"status":"未上架",
			"actions":["编辑","彻底删除"]
		},{
			"name": "商品2",
			"sales":0,
			"status":"未上架",
			"actions":["编辑","彻底删除"]
		},{
			"name": "商品1",
			"sales":0,
			"status":"未上架",
			"actions":["编辑","彻底删除"]
		}]
	"""


@panda
Scenario:3 客户删除商品
	Given aini登录系统
	When anni添加商品
	"""
		[{
			"name": "叫花鸡",
			"price": 12.00,
			"weight": 1.00,
			"stock_type": "无限"
		},{
			"name": "五花肉",
			"price": 12.00,
			"weight": 1.00,
			"stock_type": "无限"
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

	

