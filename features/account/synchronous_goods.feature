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
	Then jobs登录系统:weapp
	And jobs查看待售商品列表
		| goods_information | supplier | group | price |  stock  | sales | synchronous_time |
		|       周黑鸭      |          |       | 10.00 | 500.00  | 0.00  | 2016-06-24 17:25 |
		|      耐克男鞋     |          |       |322.00 |no_limit | 0.00  | 2016-06-24 17:26 |

@penda @hj
Scenario:1 修改商品后,再选择一个自营平台同步
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
		|  耐克男鞋|     土小宝    | 0.00|weizoom_baifumei/weizoom_xuesheng|
	


