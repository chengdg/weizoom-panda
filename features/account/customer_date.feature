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
			"account_name":"土小宝",
			"login_account":"tuxiaobao",
			"password":123456,
			"ramarks":"土小宝客户体验账号"
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
			"commodity_name":"武汉鸭脖",
			"title"："周黑鸭 鲜卤鸭脖 230g/袋 办公室休闲零食 肉干小食",
			"product_price":9.9,
			"setlement_price":9.9,
			"product_weight":0.23,
			"repertory":{
						"is_limit":"on",
						"limit_num":500
			},
			"picture":"",
			"description":"周黑鸭 鲜卤鸭脖 230g/袋 办公室休闲零食 肉干小食"
			},{
			"commodity_name":"NIKE耐克男鞋便减震舒适休闲跑步鞋",
			"title"："旗舰店—618粉丝狂欢， 赢200元粉丝券！",
			"product_price":322,
			"setlement_price":298,
			"product_weight":0.5,
			"repertory":{
						"is_limit":"off"
			},
			"description":"旗舰店—618粉丝狂欢，关注微信公众号"jdxyyz" 赢200元粉丝券！"
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
	When jobs登录系统:weapp
	Then jobs取消订单'对应订单编号001'
	Then yunying查看多商品销量列表
			|  goods  | weizoom_jia | weizoom_mama | weizoom_shop | weizoom_baifumei | total |
			|武汉鸭脖 |    0.00     |     0.00     |      0.00    |       0.00       | 10.00 |
			|耐克男鞋 |    0.00     |     0.00     |      0.00    |       0.00       |  0.00 | 

@penda @hj
Scenario:2 运营人员查看订单销售趋势列表
	Then yunying查看订单销售趋势列表
		|first_week|second_week|third_week|fourth_week|
		|   10.00  |    0.00   |   0.00   |   0.00    |
	When jobs登录系统:weapp
	Then jobs取消订单'对应订单编号001'
	Then yunying查看订单销售趋势列表
		|first_week|second_week|third_week|fourth_week|
		|   10.00  |    0.00   |   0.00   |   0.00    |


@penda @hj
Scenario:3 运营人员查看购买用户数据列表
	Then yunying查看购买用户数据列表
		|total_people| buy_sinal | buy_again |
		|     1.00   |   1.00    |   0.00    |
	When jobs登录系统:weapp
	Then jobs取消订单'对应订单编号001'
	Then yunying查看购买用户数据列表
		|total_people| buy_sinal | buy_again |
		|     0.00   |   1.00    |   0.00    |


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
	When jobs登录系统:weapp
	Then jobs取消订单'对应订单编号001'
	Then yunying查看平台订单数列表
		| weizoom_jia | weizoom_mama | weizoom_shop | weizoom_baifumei |
		|    0.00     |     0.00     |    10.00     |        0.00      |

