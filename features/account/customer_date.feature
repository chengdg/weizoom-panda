auther:徐梓豪 2016-06-24
Feature:运营人员查看客户报告所需数据 
"""
	1.运营人员查看多商品销量列表
	2.运营人员查看订单销售趋势列表
	3.运营人员查看购买用户数据列表
	4.运营人员查看体验反馈数据列表
	5.运营人员查看平台订单数列表 
	
"""
Background:
	Given manager登录管理系统
	Then manager添加账号
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
		},{
			"account_type":"运营",
			"account_name":"运营部门",
			"login_account":"yunying",
			"password":123456,
			"ramarks":"运营部门"
		}]
	"""
	When tuxiaobao使用密码123456登录管理系统
	When tuxiaobao添加商品
	"""
		[{
			"first_classify":"生活用品",
		"second_classify":"零食",
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
						|standard_1|standard_2|purchase_price|sale_price|weight|stock_number|
						|   黑色   |     X    |     14.90    |   29.00  | 0.50 |   2500.00  |
						|   黑色   |    XL    |     14.90    |   29.00  | 0.50 |   2000.00  |    
						|   红色   |     X    |     14.90    |   29.00  | 0.50 |   1000.00  |
						|   红色   |    XL    |     14.90    |   29.00  | 0.50 |   1300.00  |
			},{
			{
			"first_classify":"居家",
			"second_classify":"鞋子",			
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
						|standard_1|standard_2|purchase_price|sale_price|weight|stock_number|
						|   黑色   |     X    |     14.90    |   29.00  | 0.50 |   2500.00  |
						|   黑色   |    XL    |     14.90    |   29.00  | 0.50 |   2000.00  |   
						|   红色   |     X    |     14.90    |   29.00  | 0.50 |   1000.00  |
						|   红色   |    XL    |     14.90    |   29.00  | 0.50 |   1300.00  |
						}
						
		}]
	"""
		
	Given yunying使用密码123456登录系统
	When yunying绑定商品关联的云商通商品
	"""
		[{
			"name":"武汉鸭脖",
			"weapp_id":["微众家":"2400"]
			},{
			"name":"耐克男鞋",
			"weapp_id":["微众家":"2401"]
		}]
	"""
	When 微信用户批量消费tuxiaobao在云商通商家'微众家'关联的商品
		|	order_id	  | date       | consumer |    type   |businessman|   product | payment  | payment_method | freight |   price  | product_integral |  	 coupon  		| paid_amount | 		weizoom_card 		| alipay | wechat | cash |      action       |  order_status   |
		|对应订单编号001  | 2016-6-24   | bill     |   购买   | 微众商城   | 武汉鸭脖 | 支付     | 支付宝         |  5.00   | 10.00    | 		|          		|          0.00        |   100.00	|              0.00            | 0      | 0    | 100.00 |  待发货         |

@penda @hj
Scenario:1 运营人员查看多商品销量列表
	Given yunying登录系统
	When yunying查看多商品销量列表
	|  goods  | weizoom_jia | weizoom_mama | weizoom_shop | weizoom_baifumei | total |
	|武汉鸭脖 |    0.00     |     0.00     |      10.00   |       0.00       | 10.00 |
	|耐克男鞋 |    0.00     |     0.00     |      0.00    |       0.00       |  0.00 | 

@penda @hj
Scenario:2 运营人员查看订单销售趋势列表
	Then yunying查看订单销售趋势列表
	|first_week|second_week|third_week|fourth_week|
	|   10.00  |    0.00   |   0.00   |   0.00    |

@penda @hj
Scenario:3 运营人员查看购买用户数据列表
	Then yunying查看购买用户数据列表
	|total_people| buy_sinal | buy_again |
	|     1.00   |   1.00    |   0.00    |

@penda @hj
Scenario:4 运营人员查看体验反馈数据列表
	When tuxiaobao将订单'对应订单编号001'发货
	"""
	{
		"company":"圆通快递",
		"odd_numbers":"123456"
	}
	"""	
	Then tuxiaobao查看订单列表
		|business|price/number|customer|order_price|order_statues|  order_number  |   time   |
		|武汉鸭脖|10.00/10.00 |  bill  |   100.00  |   已发货    |对应订单编号001 |2016-06-24|

	When tuxiaobao将订单'对应订单编号001'标记完成
	Then tuxiaobao查看订单列表
		|business|price/number|customer|order_price|order_statues|  order_number  |   time   |
		|武汉鸭脖|10.00/10.00 |  bill  |   100.00  |   已完成    |对应订单编号001 |2016-06-24|

	When 微信用户对订单'对应订单编号001'发表评价
	{
		"goods_evaluate":"123456"
	}

	Then yunying登录系统
	Then yunying查看体验反馈数据
	|person_number|list_number|
	|     1.00    |    1.00   |

@penda @hj
Scenario:5 运营人员查看平台订单数列表
	When yunying登录管理系统
	Then yunying查看平台订单数列表
	| weizoom_jia | weizoom_mama | weizoom_shop | weizoom_baifumei |
	|    0.00     |     0.00     |    10.00     |        0.00      | 
