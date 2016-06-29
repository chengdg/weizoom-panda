#author: 张雪 2016-5-25

Feature:精简版云商通-添加商品、删除商品
"""
	1.客户登录管理系统
	2.客户添加商品
	3.客户删除商品

	添加商品的文本框为必填项

"""
Background:
	Given jobs登录管理系统
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
#Scenario:1 客户登录管理系统
#	Given jobs登录管理系统
#	Then jobs可以看到订单列表
#	"""
#		[]
#	"""
#	Then jobs能获取商品列表
#	"""
#		[]
#	"""


@panda @hj
Scenario:2 客户添加商品
	When aini使用密码123456登录系统
	When aini添加商品
	"""
		[{
			"name": "商品1",
			"promotion_name":"促销的商品1",
			"price": 12.00,
			"weight": 1.00,
			"stock_type": "无限",
			"settlement_price":10.00,
			"introduction": "商品1的简介"
		},{
			"name": "商品2",
			"promotion_name":"促销的商品2",
			"settlement_price":10.00,
			"introduction": "商品2的简介",
			"price": 12.00,
			"weight": 1.00,
			"stock_type": "无限",
			"settlement_price":10.00,
			"introduction": "商品2的简介"

		},{
			"name": "商品3",
			"promotion_name":"促销的商品3",
			"price": 12.00,
			"weight": 1.00,
			"stock_type": "无限",
			"settlement_price":10.00,
			"introduction": "商品3的简介"
		}]
	"""


	Then aini能获得商品列表
	"""
		[{
			"name": "商品3",
			"price": "12.00",
			"sales":"0",
			"status":"未上架",
			"actions":["编辑","彻底删除"]
		},{
			"name": "商品2",
			"price": "12.00",
			"sales":"0",
			"status":"未上架",
			"actions":["编辑","彻底删除"]
		},{
			"name": "商品1",
			"price": "12.00",
			"sales":"0",
			"status":"未上架",
			"actions":["编辑","彻底删除"]
		}]
	"""


@panda @hj
Scenario:3 客户删除商品
	When aini使用密码123456登录系统
	When aini添加商品
	"""
		[{
			"name": "叫花鸡",
			"promotion_name":"促销的商品1",
			"price": 12.00,
			"weight": 1.00,
			"stock_type": "无限",
			"settlement_price":10.00,
			"introduction": "商品1的简介"
		},{
			"name": "五花肉",
			"promotion_name":"促销的商品1",
			"price": 12.00,
			"weight": 1.00,
			"stock_type": "无限",
			"settlement_price":10.00,
			"introduction": "商品1的简介"
		}]
	"""
	When aini删除商品'叫花鸡'
	Then aini能获得商品列表
	"""
		[{
			"name": "五花肉",
			"price": "12.00",
			"sales": "0",
			"status":"未上架",
			"actions":["编辑","彻底删除"]
		}]
	"""

	
@panda @hj
Scenario:4 客户编辑商品
	When aini使用密码123456登录系统
	When aini添加商品
	"""
		[{
			"name": "商品1",
			"promotion_name":"促销的商品1",
			"price": 12.00,
			"weight": 1.00,
			"stock_type": "无限",
			"settlement_price":10.00,
			"introduction": "商品1的简介"
		}]
	"""
	When aini编辑商品'商品1'
	"""
		[{
			"name": "商品11",
			"promotion_name":"促销的商品11",
			"price": 10.00,
			"weight": 1.00,
			"stock_type": "无限",
			"settlement_price":10.00,
			"introduction": "商品1的简介"
		}]
	"""
	Then aini能获得商品列表
	"""
		[{
			"name": "商品11",
			"price": "10.00",
			"sales":"0",
			"status":"未上架",
			"actions":["编辑","彻底删除"]
		}]
	"""

