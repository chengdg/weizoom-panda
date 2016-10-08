auther:徐梓豪 2016-06-24
Feature:运营人员同步商品到云商通平台
"""
1.新增商品后,运营账号同步商品
2.修改商品后,再选择一个自营平台同步
3.删除商品，重新新增商品后再同步
4.在weapp中删除商品后,运营查看商品
5.批量同步商品
"""

Background:
	Given manager登录管理系统
	When manager添加账号
		"""
			{
				"account_type":"运营",
				"account_name":"运营部门",
				"login_account":"yunying",
				"password":123456,
				"ramarks":"运营部门"
			}
		"""
	Given yunying登录系统
	When yunying添加分类
		"""
		{
		"head_classify":"无",
		"classify_name":"电子数码",
		"comments":"1"
		},{
		"head_classify":"无",
		"classify_name":"生活用品",
		"comments":"1"
		},{
		"head_classify":"电子数码",
		"classify_name":"手机",
		"comments":""
		},{
		"head_classify":"电子数码",
		"classify_name":"平板电脑",
		"comments":""
		},{
		"head_classify":"电子数码",
		"classify_name":"耳机",
		"comments":""
		},{
		"head_classify":"生活用品",
		"classify_name":"零食",
		"comments":""
		},{
		"head_classify":"生活用品",
		"classify_name":"肥皂",
		"comments":""
		},{
		"head_classify":"生活用品",
		"classify_name":"清洗用品,
		"comments":""
		}
		"""
		Given manager登录管理系统
		When manager添加账号
		"""
		{
		"account_type":"体验客户",
		'product_style':{
						"电子数码"，
						"生活用品"
						},
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
		}
		"""	
	Given aini登录系统	
	When aini添加规格
		"""
		[{
		"standard_name":"尺码",
		"show_type":"文字",
		"standard":{
					"M","X","XL","XXL","XXXL"
				   }
		},{
		"standard_name":"颜色",
		"show_type":"文字",
		"standard":{
					"红","黄","蓝","黑",
				   }
		}]
		"""

	Then aini添加商品
		"""
		[{
		"first_classify":"生活用品",
		"second_classify":"零食",
		"product_name": "武汉鸭脖",
		"title":"武汉鸭脖",
		"introduction": "这是一种很好吃的鸭脖"
		"standard_promotion":"否",
		"price":10.00,
		"setlement_price":8.00,
		"weight":0.23,
		"repertory":"500.00",
		"picture":"",
		"description":"周黑鸭 鲜卤鸭脖 230g/袋 办公室休闲零食 肉干小食"
		},{
		"first_classify":"电子数码",
		"second_classify":"耳机",
		"product_name": "耐克男鞋",
		"title":"耐克男鞋，耐穿耐磨",
		"standard_promotion":"是",
		"standard":{
					"standard_name":"颜色",
					"standard":"黑色","红色"
					},{
					"standard_name":"尺码",
					"standard":"X,XL"
					}
		"standard_price":{
					|standard_1|standard_2|purchase_price|sale_price|weight|stock_number|product_id|
					|   黑色   |     X    |     14.90    |   29.00  | 0.50 |   2500.00  |    001   |
					|   黑色   |    XL    |     14.90    |   29.00  | 0.50 |   2000.00  |    002   |    
					|   红色   |     X    |     14.90    |   29.00  | 0.50 |   1000.00  |    003   |
					|   红色   |    XL    |     14.90    |   29.00  | 0.50 |   1300.00  |    004   | 
		},{
		"first_classify":"电子数码",
		"second_classify":"平板电脑",
		"shop_name": "ipad",
		"title":"苹果平板",
		"standard_promotion":"否",
		"price":3000.00,
		"setlement_price":2500.00,
		"weight":2.00,
		"repertory":"500.00",
		"picture":"",
		"description":"苹果平板，大屏看电视"
		}
		}]
		"""
@panda @hj
Scenario:1  新增商品后,运营账号同步商品
	Given yunying登录系统
	When yunying同步商品'武汉鸭脖'
	"""
	{
	"synchronous_goods":"微众商城",
	"synchronous_goods":"微众家",
	"synchronous_goods":"微众白富美"
	}
	"""

	Then yunying同步商品'耐克男鞋'
	"""
	{
	"synchronous_goods":"微众家",
	"synchronous_goods":"微众白富美"
	}
	"""
	Then yunying查看商品列表
		
		|01|武汉鸭脖|生活用品,零食|爱伲咖啡|      |  10.00  |    8.00  | 0.00  |2016-07-25 16:30|已入库,已同步 |同步/修改分类|
		|02|耐克男鞋|电子数码,耳机|爱伲咖啡|      |  14.90  |   29.00  | 0.00  |2016-07-25 16:30| 未上架 |同步/修改分类|
		|03|  ipad  |电子数码,平板|爱伲咖啡|      | 3000.00 |  2500.00 | 0.00  |2016-08-22 11:03| 未上架 |同步/修改分类|
	Given jobs登录系统:weapp
	When jobs查看商品池
	|  information  | supplier   | group | price |     stocks      | profit |purchase_type|
	|    武汉鸭脖   | p-爱伲咖啡 |       | 10.00 |     500.00      |  2.00  |   固定底价  |
	|    耐克男鞋   | p-爱伲咖啡 |       | 29.00 |1000.00-2500.00  | 14.10  |   固定底价  |
	Then jobs上架商品
	"""
	{
	"information":"武汉鸭脖",
	"information":"耐克男鞋"
	}
	"""
	Then jobs查看商品池
	|  information  | supplier   | group | price | stocks | synchronous_time |
	And jobs查看在售商品列表
	|  information  | supplier   | group | price |     stocks      | sales |  putaway_time  |
	|    武汉鸭脖   | p-爱伲咖啡 |       | 10.00 |     500.00      |  0.00 |2016-08-23 10:06|              
	|    耐克男鞋   | p-爱伲咖啡 |       | 29.00 | 1000.00-2500.00 |  0.00 |2016-08-23 10:06| 

	Given aini登录系统:panda
	When aini查看商品列表
	|  name   | set_price |sale_price| sales |   creat_time   | status |
	|武汉鸭脖 |   10.00   |    8.00  | 0.00  |2016-07-25 16:30| 已上架 |
	|耐克男鞋 |   14.90   |   29.00  | 0.00  |2016-07-25 16:30| 已上架 |
	|  ipad   |  3000.00  |  2500.00 | 0.00  |2016-08-22 11:03| 未上架 |
               

@penda @hj
Scenario:2 修改商品后,再选择一个自营平台同步
	Given tuxiaobao登录系统
	When tuxiaobao查看商品列表
		|business_name| end_price | sales | cerat_time | statues |
		|   武汉鸭脖  |   10.00   |  0.00 | 2016-06-24 |  added  |
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
		|   武汉鸭脖  |   10.00   |  0.00 | 2016-06-24 |  added  |
		|   耐克男鞋  |  300.00   |  0.00 | 2016-06-24 |  added  |

	Then yunying登录系统
	And yunying查看商品列表
		|id|  name  |   classify  |supplier|source|set_price|sale_price| sales |   creat_time   | status |operate|
		|01|武汉鸭脖|生活用品,零食|爱伲咖啡|      |  10.00  |    8.00  | 0.00  |2016-07-25 16:30|已入库,已同步 |同步/修改分类|
		|02|耐克男鞋|电子数码,耳机|爱伲咖啡|      |  14.90  |   29.00  | 0.00  |2016-07-25 16:30| 未上架 |同步/修改分类|
		|03|  ipad  |电子数码,平板|爱伲咖啡|      | 3000.00 |  2500.00 | 0.00  |2016-08-22 11:03| 未上架 |同步/修改分类|
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
		|id|  name  |   classify  |supplier|source|set_price|sale_price| sales |   creat_time   | status |operate|
		|01|武汉鸭脖|生活用品,零食|爱伲咖啡|      |  10.00  |    8.00  | 0.00  |2016-07-25 16:30|已入库,已同步 |同步/修改分类|
		|02|耐克男鞋|电子数码,耳机|爱伲咖啡|      |  14.90  |   29.00  | 0.00  |2016-07-25 16:30| 未上架 |同步/修改分类|
		|03|  ipad  |电子数码,平板|爱伲咖啡|      | 3000.00 |  2500.00 | 0.00  |2016-08-22 11:03| 未上架 |同步/修改分类|

	When jobs登录系统
    Then jobs查看待售商品列表
		|  information  | supplier   | group | price | stocks | synchronous_time |
	Then jobs查看在售商品列表
		| goods_information | supplier | group | price |  stock  | sales | synchronous_time |
		|      武汉鸭脖     |          |       | 10.00 |  无限   | 0.00  | 2016-06-24 17:40 |
		|      耐克男鞋     |          |       |298.00 |  无限   | 0.00  | 2016-06-24 17:41 |

@penda @hj
Scenario:3 删除商品，重新新增商品后再同步
	When tuxiaobao登录系统:penda
	Then tuxiaobao查看商品列表
		|  information  | price | sales |   creat_time   |  statues  |
		|    武汉鸭脖   | 10.00 |  0.00 |2016-06-24 17:32|  not_add  |
		|    耐克男鞋   | 298.00|  0.00 |2016-06-24 17:32|  not_add  |
	Then tuxioobao将商品'武汉鸭脖','耐克男鞋'删除
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
		|    武汉鸭脖   | 10.00 |  0.00 |2016-06-24 17:32|  not_add  |
		|    耐克男鞋   | 298.00|  0.00 |2016-06-24 17:32|  not_add  |
	When yunying查看商品列表
		|goods_name| costumer_name |sales|        synchronous_goods        |
		| 武汉鸭脖 |     土小宝    | 0.00|                                 |
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
		| 武汉鸭脖 |     土小宝    | 0.00|          weizoom_jia            |
		| 耐克男鞋 |     土小宝    | 0.00|          weizoom_mama           |
	When jobs登录系统
	TThen jobs查看待售商品列表
		|  information  | supplier   | group | price | stocks | synchronous_time |
		|    武汉鸭脖   |你咋不上天了|       | 10.00 |  无限  |                  |
	When jobs将商品'周黑鸭'上架
	Then jobs查看待售商品列表
		|  information  | supplier   | group | price | stocks | synchronous_time |
	And jobs查看在售商品列表
		| goods_information |  supplier  | group | price |  stock  | sales | synchronous_time |
		|      武汉鸭脖     |你咋不上天了|       | 10.00 |  无限   | 0.00  | 2016-06-24 17:25 |

@penda @hj
Scenario:4 在云商通中删除商品后，运营查看商品列表时，商品显示为未同步
	Given yunying登录系统
	When yunying同步商品'武汉鸭脖'
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
		| 武汉鸭脖 |     土小宝    | 0.00|  weizoom_shop   |
		| 耐克男鞋 |     土小宝    | 0.00|weizoom_baifumei |
	Then tuxiaobao查看商品列表
		|goods_name|   price   |  sales  |     creat_time    |  statu  |
		| 武汉鸭脖 |    10.00  |   0.00  |2016-06-28 12:01:04| 已上架  | 
		|  耐克男鞋|   298.00  |   0.00  |2016-06-28 12:02:05| 已上架  | 
	When jobs登录系统:weapp
	Then jobs查看待售商品列表
		|  information  | supplier   | group | price | stocks | synchronous_time |
		|    武汉鸭脖   |你咋不上天了|       | 10.00 |  无限  |                  |
		|    耐克男鞋   |你咋不上天了|       |322.00 |  无限  |                  |
	When jobs将商品'周黑鸭weapp','耐克男鞋weapp'上架
	Then jobs查看待售商品列表
		|  information  | supplier   | group | price | stocks | synchronous_time |
	And jobs查看在售商品列表
		| goods_information |  supplier  | group | price |  stock  | sales | synchronous_time |
		|      武汉鸭脖     |你咋不上天了|       | 10.00 |  无限   | 0.00  | 2016-06-24 17:25 |
		|      耐克男鞋     |你咋不上天了|       |298.00 |  无限   | 0.00  | 2016-06-24 17:26 |
	And jobs删除商品'武汉鸭脖','耐克男鞋'
	Then jobs查看在售商品列表
		| goods_information |  supplier  | group | price |  stock  | sales | synchronous_time |
	Then tuxiaobao查看商品列表
		|goods_name|   price   |  sales  |     creat_time    |  statu  |
		| 武汉鸭脖 |    10.00  |   0.00  |2016-06-28 12:01:04| 未同步  | 
		|  耐克男鞋|   298.00  |   0.00  |2016-06-28 12:02:05| 未同步  |

@penda @hj
Scenario:5 批量同步商品
	Given yunying登录系统
	When yunying对商品'周黑鸭','耐克男鞋'批量同步
	"""
	[{
		"synchronous_goods":{
						"weizoom_shop",
						"weizoom_home",
						"weizoom_yijiaren",
						"weizoom_shop"
	}]
	"""
	Given tuxiaobao登录系统
	When tuxiaobao查看商品列表
	|  name   | set_price |sale_price| sales |   creat_time   | status |
	|武汉鸭脖 |   10.00   |   10.90  | 0.00  |2016-07-25 16:30| 未上架 |
	|耐克男鞋 |   198.00  |  322.00  | 0.00  |2016-07-25 16:30| 未上架 |

	Given jobs登录 系统:weapp
	When jobs查看商品池
	|  name   | set_price |sale_price| sales |   creat_time   | status |
	|武汉鸭脖 |   10.00   |   10.90  | 0.00  |2016-07-25 16:30| 未上架 |
	|耐克男鞋 |   198.00  |  322.00  | 0.00  |2016-07-25 16:30| 未上架 |
	When jobs上架商品'武汉鸭脖'
	Then jobs查看在售商品列表
	|  name   | set_price |sale_price| sales |   creat_time   | status |
	|武汉鸭脖 |   10.00   |   10.90  | 0.00  |2016-07-25 16:30| 已上架 |
	Given tuxiaobao登录系统:panda
	When tuxiaobao查看商品列表
	|  name   | set_price |sale_price| sales |   creat_time   | status |
	|武汉鸭脖 |   10.00   |   10.90  | 0.00  |2016-07-25 16:30| 已上架 |
	|耐克男鞋 |   198.00  |  322.00  | 0.00  |2016-07-25 16:30| 未上架 |

	
		