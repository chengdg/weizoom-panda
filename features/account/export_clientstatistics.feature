#author: 徐梓豪 2016.06.04
Feature:运营人员导出客户统计
"""
	1.运营人员导出客户统计
"""

Background:
	Given manager登录系统
	Then manager添加账号
	"""
		[{
			"account_type":"合作客户",
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
  	Then yunying查看客户统计列表
		| name | start_time | sales |order_number| price | cash | card |discount_coupon|feedback|
		|土小宝| 2016-06-01 | 0.00  |      0     |  0.00 | 0.00 | 0.00 |     0.00      |查看报告|

@penda @hj
Scenario:1 运营账号导出客户统计列表 
	Given tuxiaobao导出客户统计列表
		| name | start_time | sales |order_number| price | cash | card |discount_coupon|feedback|
		|土小宝| 2016-06-01 | 0.00  |      0     |  0.00 | 0.00 | 0.00 |     0.00      |查看报告|
                                                                                                                                                                                                    