auther:徐梓豪 2016-06-24
Feature:运营人员同步商品到云商通平台
"""
1.新增商品后,运营账号同步商品
2.修改商品后,再选择一个自营平台同步
3.删除商品，重新新增商品后再同步
"""

Background:
	Given manager登录管理系统
	When manager添加账号
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

		"""
	When tuxiaobao使用密码123456登录管理系统
	When tuxiaobao添加商品
		"""
		[{
		"name":"武汉鸭脖",
		"title"："周黑鸭 鲜卤鸭脖 230g/袋 办公室休闲零食 肉干小食",
		"price":10.00,
		"setlement_price":10.00,
		"weight":0.23,
		"repertory":{
					"is_limit":"on",
					"limit_num":500.00
		},
		"picture":"",
		"description":"周黑鸭 鲜卤鸭脖 230g/袋 办公室休闲零食 肉干小食"
		},{
		"name":"NIKE耐克男鞋便减震舒适休闲跑步鞋",
		"title"："旗舰店—618粉丝狂欢， 赢200元粉丝券!",
		"price":322.00,
		"setlement_price":298.00,
		"weight":0.50,
		"repertory":{
					"is_limit":"off"
		},
		"description":"旗舰店—618粉丝狂欢，关注微信公众号"jdxyyz" 赢200元粉丝券!"
		}]
		"""

	When jobs登录系统:weapp
	When jobs新增商品
		"""
		[{
		"name":"武汉鸭脖weapp",
		"supplier":"你咋不上天了",
		"type":"normal",
		"price":"20.00",
		"weight":"0.20",
		"stock_type":"无限",
		"freight_type":{"unification_freight",
						"unification_freight":"5.00"	
		},
		"payment_type":"online"
		},{
		"name":"耐克男鞋weapp",
		"supplier":"你咋不上天了",
		"type":"normal",
		"price":"298.00",
		"weight":"0.50",
		"stock_type":"无限",
		"freight_type":{"unification_freight",
						"unification_freight":"5.00"	
		},
		"payment_type":"online"
		}]
	Then jobs查看待售商品列表
		|  information  | supplier   | group | price | stocks | synchronous_time |
		|   周黑鸭weapp |你咋不上天了|       | 10.00 |  无限  |                  |
		| 耐克男鞋weapp |你咋不上天了|       |322.00 |  无限  |                  |
	When jobs将商品'周黑鸭weapp','耐克男鞋weapp'上架
	Then jobs查看代售商品列表
		|  information  | supplier   | group | price | stocks | synchronous_time |
	Then jobs查看在售商品列表
		|  information  | supplier   | group | price | stocks | sales | synchronous_time |  order   |
		|   周黑鸭weapp |你咋不上天了|       | 10.00 |  无限  | 0.00  |                  |   0.00   |
		| 耐克男鞋weapp |你咋不上天了|       |322.00 |  无限  | 0.00  |                  |   0.00   |

@penda @hj
Scenario:1 新增商品后，运营账号同步商品
	Given yunying登录系统
	When yunying同步商品'周黑鸭'
		"""
		{
		"synchronous_goods":"weizoom_shop"
		}
		"""
	Then yunying同步商品'耐克男鞋'
		"""
		{
		"synchronous_goods":"weizoom_baifumei"
		}
		"""
	Then yunying查看商品列表
		|goods_name| costumer_name |sales|synchronous_goods|
		|  周黑鸭  |     土小宝    | 0.00|  weizoom_shop   |
		|  耐克男鞋|     土小宝    | 0.00|weizoom_baifumei |
	When jobs登录系统:weapp
	Then 运营人员根据弹出信息选择商品进行同步
	And jobs查看在售商品列表
		| goods_information | supplier | group | price |  stock  | sales | synchronous_time |
		|     周黑鸭weapp   |          |       | 10.00 |  无限   | 0.00  | 2016-06-24 17:25 |
		|   耐克男鞋weapp   |          |       |298.00 |  无限   | 0.00  | 2016-06-24 17:26 |

@penda @hj
Scenario:2 修改商品后,再选择一个自营平台同步
	Given tuxiaobao登录系统
	When tuxiaobao查看商品列表
		|business_name| end_price | sales | cerat_time | statues |
		|    周黑鸭   |   10.00   |  0.00 | 2016-06-24 |  added  |
		|   耐克男鞋  |  298.00   |  0.00 | 2016-06-24 |  added  |
	Then tuxiaobao修改商品信息
		"""
		[{
		"name":"武汉鸭脖",
		"title"："周黑鸭 鲜卤鸭脖 230g/袋 办公室休闲零食 肉干小食",
		"price":10.00,
		"setlement_price":10.00,
		"weight":0.50,
		"repertory":{
					"is_limit":"on",
					"limit_num":430.00
		},
		"picture":"",
		"description":"周黑鸭 鲜卤鸭脖"
		},{
		"name":"NIKE耐克男鞋便减震舒适休闲跑步鞋",
		"title"："旗舰店—618粉丝狂欢， 赢200元粉丝券!",
		"price":322.00,
		"setlement_price":300.00,
		"weight":0.50,
		"repertory":{
					"is_limit":"on",
					"limit_num":320.00
		},
		"description":"旗舰店—618粉丝狂欢，关注微信公众号"jdxyyz" 赢200元粉丝券!"
		}]
	Then tuxiaobao查看商品列表
		|business_name| end_price | sales | cerat_time | statues |
		|    周黑鸭   |   10.00   |  0.00 | 2016-06-24 |  added  |
		|   耐克男鞋  |  300.00   |  0.00 | 2016-06-24 |  added  |

	Then yunying登录系统
	And yunying查看商品列表
		|goods_name| costumer_name |sales|synchronous_goods|
		|  周黑鸭  |     土小宝    | 0.00|  weizoom_shop   |
		|  耐克男鞋|     土小宝    | 0.00|weizoom_baifumei |
	When yunying同步商品'周黑鸭'
		"""
		{
		"synchronous_goods":"weizoom_mama"
		}
		"""
	Then yunying同步商品'耐克男鞋'
		"""
		{
		"synchronous_goods":"weizoom_xuesheng"
		}
		"""
	Then yunying查看商品列表
		|goods_name| costumer_name |sales|        synchronous_goods        |
		|  周黑鸭  |     土小宝    | 0.00|    weizoom_shop/weizoom_mama    |
		| 耐克男鞋 |     土小宝    | 0.00|weizoom_baifumei/weizoom_xuesheng|

	When jobs登录系统
	Then 运营人员根据弹出信息同步商品
	Then jobs查看在售商品列表
		| goods_information | supplier | group | price |  stock  | sales | synchronous_time |
		|     周黑鸭weapp   |          |       | 10.00 |  无限   | 0.00  | 2016-06-24 17:40 |
		|   耐克男鞋weapp   |          |       |298.00 |  无限   | 0.00  | 2016-06-24 17:41 |

@penda @hj
Scenario:3 删除商品，重新新增商品后再同步
	When tuxiaobao登录系统:penda
	Then tuxiaobao查看商品列表
		|  information  | price | sales |   creat_time   |  statues  |
		|     周黑鸭    | 10.00 |  0.00 |2016-06-24 17:32|  not_add  |
		|    耐克男鞋   | 298.00|  0.00 |2016-06-24 17:32|  not_add  |
	Then tuxioobao将商品'周黑鸭','耐克男鞋'删除
	Then tuxiaobao查看商品列表
		|goods_name| costumer_name |sales|        synchronous_goods        |

	When tuxiaobao新增商品
	"""
		[{
		"name":"武汉鸭脖",
		"title"："周黑鸭 鲜卤鸭脖 230g/袋 办公室休闲零食 肉干小食",
		"price":10.00,
		"setlement_price":10.00,
		"weight":0.50,
		"repertory":{
					"is_limit":"on",
					"limit_num":430.00
		},
		"picture":"",
		"description":"周黑鸭 鲜卤鸭脖"
		},{
		"name":"NIKE耐克男鞋便减震舒适休闲跑步鞋",
		"title"："旗舰店—618粉丝狂欢， 赢200元粉丝券!",
		"price":322.00,
		"setlement_price":300.00,
		"weight":0.50,
		"repertory":{
					"is_limit":"on",
					"limit_num":320.00
		},
		"description":"旗舰店—618粉丝狂欢，关注微信公众号"jdxyyz" 赢200元粉丝券!"
		}]

	Then tuxiaobao查看商品列表
		|  information  | price | sales |   creat_time   |  statues  |
		|     周黑鸭    | 10.00 |  0.00 |2016-06-24 17:32|  not_add  |
		|    耐克男鞋   | 298.00|  0.00 |2016-06-24 17:32|  not_add  |
	When yunying查看商品列表
		|goods_name| costumer_name |sales|        synchronous_goods        |
		|  周黑鸭  |     土小宝    | 0.00|                                 |
		| 耐克男鞋 |     土小宝    | 0.00|                                 |
	When yunying选择商品'周黑鸭','耐克男鞋'同步至自营平台
		"""
		[{
		"synchronous_goods":"weizoom_xuesheng"
		},{
		"synchronous_goods":"weizoom_mama"
		}]
		"""
	Then yunying查看商品列表
		|goods_name| costumer_name |sales|        synchronous_goods        |
		|  周黑鸭  |     土小宝    | 0.00|       weizoom_xuesheng          |
		| 耐克男鞋 |     土小宝    | 0.00|        weizoom_mama             |
	When jobs登录系统
	Then jobs根据弹出的信息同步商品
	Then jobs查看在售商品列表
		| goods_information | supplier | group | price |  stock  | sales | synchronous_time |
		|     周黑鸭weapp   |          |       | 10.00 |  无限   | 0.00  | 2016-06-24 17:35 |
		|   耐克男鞋weapp   |          |       |298.00 |  无限   | 0.00  | 2016-06-24 17:35 |