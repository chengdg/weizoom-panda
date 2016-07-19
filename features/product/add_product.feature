#author: 张雪 2016-5-25
#editor: 徐梓豪 2016-07-18

Feature:精简版云商通-添加商品、删除商品
"""
	1.客户登录管理系统
	2.客户添加商品
	3.客户删除商品
	4.客户编辑商品
	5.新增带有多规格的商品

	添加商品的文本框为必填项

"""
Background:
	Given jobs登录管理系统
	When jobs添加账号
	"""
		[{
			"account_type":"体验客户",
			"company_name":"爱昵咖啡有限责任公司",
			"shop_name":"爱昵咖啡",
			"manage_type":"休闲食品",
			"purchase_type":"固定底价",
			"connect_man":"aini",
			"mobile_number":"13813985506",
			"login_account":"aini",
			"password":"123456",
			"valid_time":"2016-07-15"至"2017-07-15",
			"ramarks":"爱昵咖啡客户体验账号"
		}{
			"account_type":"运营",
			"account_name":"运营",
			"login_account":"yunying",
			"password":"123456"
		}]
	"""	
	Given yunying登录系统
	Then yunying创建规格样式
	"""
		[{
			"standard_name":"尺码",
			"show_type":"文字",
			"standard":{
						"M","X","XL","XXL","XXXL"
					   }
		},{
			"standard_name":"颜色",
			"show_type":"图片",
			"standard":{
						"","","","",""
					   }		
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

	
@panda @h品j
Scenario:4 客户编辑商
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
@panda @hj
Scenario:5 客户新增具有规格的商品
	Given aini登录系统
	When aini创建商品
	"""
		[{
			"name": "商品12",
			"promotion_name":"促销的商品12",
			"price": 10.00,
			"weight": 1.00,
			"stock_number": "5000",
			"settlement_price":10.00,
			"introduction": "商品1的简介"
			"standard_promotion":"是",
			"standard":{
						"standard_name":"颜色",
						"standard":"黑色","红色"
						},{
						"standard_name":"尺码",
						"standard":"X,XL"
						}
			"standard_price":{
						|standard_1|standard_2|purchase_price|timelimit_price|sale_price|weight|stock_number|product_id|
						|   黑色   |     X    |     14.90    |      14.90    |   29.00  | 0.50 |   2500.00  |    001   |
						|   黑色   |    XL    |     14.90    |      14.90    |   29.00  | 0.50 |   2000.00  |    002   |    
						|   红色   |     X    |     14.90    |      14.90    |   29.00  | 0.50 |   1000.00  |    003   |
						|   红色   |    XL    |     14.90    |      14.90    |   29.00  | 0.50 |   1300.00  |    004   | 
						}
			
		}]
	"""
	Then aini查看商品列表
	"""
		[{
			"name": "商品12",
			"price": "10.00",
			"sales":"0",
			"status":"未上架",
			"actions":["编辑","彻底删除"]
		}]
	"""

