#author:徐梓豪 2016-07-21
Feature:运营新增产品类目
"""
	1.运营新增一级类目
	2.运营编辑一级类目
	3.运营新增二级类目
	4.运营编辑二级类目
	5.运营删除类目
		未被使用的类目
		正在使用的类目
	6.新增带有类别的商品后查看列表
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

@penda @lhy
Scenario:1 运营新增一级类目
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
		}
	"""
	Then yunying查看类目列表
	|classify_name|     creat_time    | business_number |
	|   电子数码  |2016-07-21 15:30:08|      0.00       |
	|   生活用品  |2016-07-21 15:30:25|      0.00       |

@penda @lhy
Scenario:2 运营编辑一级类目	
	Given yunying登录系统
	When yunying编辑'电子数码'
	"""
		{
		"head_classify":"无",
		"classify_name":"电子数码1",
		"comments":"2"
		}
	"""
	Then yunying查看类目列表
	|classify_name|     creat_time    | business_number |
	|  电子数码1  |2016-07-21 15:30:08|      0.00       |
	|   生活用品  |2016-07-21 15:30:25|      0.00       |
@penda @lhy
Scenario:3 运营新增二级类目
	Given yunying登录系统
	When yunying添加分类
	"""
		{
		"head_classify":"电子数码1",
		"classify_name":"手机",
		"comments":""
		},{
		"head_classify":"电子数码1",
		"classify_name":"平板电脑",
		"comments":""
		},{
		"head_classify":"电子数码1",
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
	Then yunying获取分类列表
	|classify_name|     creat_time    | business_number |
	|  电子数码1  |2016-07-21 15:30:08|      0.00       |
	|   生活用品  |2016-07-21 15:30:25|      0.00       |
	|     手机    |2016-07-21 15:31:25|      0.00       |
	|   平板电脑  |2016-07-21 15:32:25|      0.00       |
	|     耳机    |2016-07-21 15:31:27|      0.00       |
	|     零食    |2016-07-21 15:31:25|      0.00       |
	|     肥皂    |2016-07-21 15:31:25|      0.00       |
	|   清洗用品  |2016-07-21 15:31:25|      0.00       |
@penda @lhy
Scenario:4 运营编辑二级类目
	Given yunying登录系统
	When yunying新建类目
	"""
	{
		head_classify":"无",
		"classify_name":"育婴产品",
		"comments":"1"
		},{
		"head_classify":"育婴产品",
		"classify_name":"奶粉",
		"comments":"国产"
	}
	"""
	When yunying编辑类目'育婴产品'
	"""
	{
		"head_classify":"无",
		"classify_name":"育婴产品",
		"comments":"2"
	}
	"""
	When yunying编辑'奶粉'
	"""
	{
		"head_classify":"育婴产品",
		"classify_name":"进口奶粉",
		"comments":""
	}
	"""
	Then yunying获取类目列表
	|classify_name|     creat_time    | business_number |
	|   育婴产品  |2016-07-21 15:31:25|      0.00       |
	|   进口奶粉  |2016-07-21 15:31:25|      0.00       |

@penda @lhy
Scenario:5 运营删除二级类目
	#删除没有商品的二级类目
	Given yunying登录系统
	When yunying新建类目
	"""
	{
		head_classify":"无",
		"classify_name":"育婴产品",
		"comments":"1"
		},{
		"head_classify":"育婴产品",
		"classify_name":"奶粉",
		"comments":"国产",
		},{
		"head_classify":"育婴产品",
		"classify_name":"婴儿服饰",
		"comments":"国产"
	}
	"""
	When yunying删除'奶粉'
	Then yunying获得类目列表
		|classify_name|     creat_time    | business_number |
		|   育婴产品  |2016-07-21 15:30:08|      0.00       |
		|   婴儿服饰  |2016-07-21 15:30:08|      1.00       |

	#删除有商品的二级类目
	Given aini登录系统
	When aini新增商品
		"""
		[{
			"firest_classify":"育婴产品"
			"second_classify":"婴儿服饰"
			"name": "婴儿服饰",
			"promotion_name":"婴儿服饰",
			"price": 198.00,
			"weight": 1.00,
			"stock_number": "5000",
			"settlement_price":200.00,
			"introduction": "婴儿服饰"
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
	When yunying删除'奶粉'
	#提示'该分类正在被使用，请先将商品调整分类后再删除分类'
	Then yunying获得类目列表
		|classify_name|     creat_time    | business_number |
		|   育婴产品  |2016-07-21 15:30:08|      0.00       |
		|   婴儿服饰  |2016-07-21 15:30:08|      1.00       |


@penda @hj
Scenario:6 新增带有类别的商品后查看列表
	Given yunying登录系统
	When yunying新建类目
	"""
	{
		head_classify":"无",
		"classify_name":"生活用品",
		"comments":"1"
		},{
		"head_classify":"生活用品",
		"classify_name":"零食",
		"comments":"国产"
		},{
		head_classify":"无",
		"classify_name":"居家",
		"comments":""
		},{
		head_classify":"居家",
		"classify_name":"鞋子",
		"comments":""
		}
	}
	"""

	Given aini登录系统
	When aini新增商品
	"""
		[{
			"firest_classify":"生活用品"
			"second_classify":"零食"
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
			"firest_classify":"居家"
			"second_classify":"鞋子"
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
						}
		}]
	"""
	When yunying登录系统
	Then yunying获取类目列表
	|classify_name|     creat_time    | business_number |
	|  生活用品   |2016-07-21 15:30:08|      1.00       |
	|    零食     |2016-07-21 15:30:08|      1.00       |
	|    居家     |2016-07-21 15:30:08|      1.00       |
	|    鞋子     |2016-07-21 15:30:08|      1.00       |
	