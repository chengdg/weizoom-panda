#author: 张雪 2016-5-25
#editor: 徐梓豪 2016-09-05

Feature:精简版云商通-添加商品、删除商品
"""
	1.客户登录管理系统
	2.客户添加商品
	3.客户删除商品

	添加商品的文本框为必填项

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
				},
	"standard_price":{
				|standard_1|standard_2|purchase_price|sale_price|weight|stock_number|product_id|
				|   黑色   |     X    |     14.90    |   29.00  | 0.50 |   2500.00  |    001   |
				|   黑色   |    XL    |     14.90    |   29.00  | 0.50 |   2000.00  |    002   |    
				|   红色   |     X    |     14.90    |   29.00  | 0.50 |   1000.00  |    003   |
				|   红色   |    XL    |     14.90    |   29.00  | 0.50 |   1300.00  |    004   | 
				},
	"area_setting":""
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


	Then aini能获得商品列表
		|  name   |costumer_name|     classify     |sale_price| sales |   creat_time   | status |
		|武汉鸭脖 |  爱伲咖啡   |  生活用品-零食   |    8.00  | 0.00  |2016-07-25 16:30| 未上架 |
		|耐克男鞋 |  爱伲咖啡   |  电子数码-耳机   |   29.00  | 0.00  |2016-07-25 16:30| 未上架 |
		|  ipad   |  爱伲咖啡   |电子数码——平板电脑|  2500.00 | 0.00  |2016-08-22 11:03| 未上架 |

@panda @hj
Scenario:3 客户删除商品
	When aini使用密码123456登录系统
	When aini添加商品
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

	When aini删除商品
	"""
	{
	"product_name": "耐克男鞋"
	}
	"""
	Then aini能获得商品列表
		|  name   |costumer_name|     classify     | set_price |sale_price| sales |   creat_time   | status |
		|武汉鸭脖 |  爱伲咖啡   |  生活用品-零食   |   10.00   |    8.00  | 0.00  |2016-07-25 16:30| 未上架 |
		|  ipad   |  爱伲咖啡   |电子数码——平板电脑|  3000.00  |  2500.00 | 0.00  |2016-08-22 11:03| 未上架 |
	

	
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

