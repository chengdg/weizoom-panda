#author: 徐梓豪 2016-07-14

Feature:商品列表导出商品
"""
	1.商品列表导出商品

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
		}]

	When aini使用密码123456登录系统
	When aini添加商品
	"""
		[{
			"first_classify":"零食",
			"second_classify":"小吃",
			"name": "武汉鸭脖",
			"promotion_name":"武汉鸭脖",
			"price": 10.00,
			"weight": 1.00,
			"stock_number": "5000",
			"settlement_price":10.00,
			"introduction": "这是一种很好吃的鸭脖"
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
						},{
			"name": "耐克男鞋",
			"promotion_name":"耐克男鞋",
			"price": 198.00,
			"weight": 1.00,
			"stock_number": "5000",
			"settlement_price":200.00,
			"introduction": "耐克男鞋"
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
			"actions":["编辑","删除"]
		}]
	"""
@penda @hj
scenario:1 商品列表导出商品
	When aini登录系统
	When aini导出商品列表
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
	| name | price | sales | status | actions |
	|商品1 |