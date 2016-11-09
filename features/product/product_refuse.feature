#author:徐梓豪 2016-10-12
Feature:商品入库驳回
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
	When aini添加运费模板
		"""
		[{
		"moudle_name":"测试模板1",
		"freight_style":"默认运费",
		"first_weight":1.00,
		"freight":5.00,
		"follow_weight":3.00,
		"follow_freight":7.00,
		"special_place_setting":"no",
		"special_free_freight_setting":"no"
		},{
		"moudle_name":"测试模板2",
		"special_place_setting":"yes",
			{
			"area":"新疆,西藏",
			"first_weight":4.00,
			"freight":5.00,
			"follow_weight":3.00,
			"follow_freight":7.00,
			"operate":"删除"
			},
		"special_free_freight_setting":"no"
		},{
		"moudle_name":"测试模板3",
		"freight_style":"默认运费",
		"first_weight":1.00,
		"freight":5.00,
		"follow_weight":3.00,
		"follow_freight":7.00,
		"special_place_setting":"no",
		"special_free_freight_setting":"yes",
			{
			"area":"江苏,上海",
			"style":"金额", 
			"condition":60.00,
			"operate":"删除"
			}
		}]
		"""
	Given aini使用密码123456登录系统
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
		"area_setting":"不发货地区",
		"area_limit":"不发货模板",
		"freight":"使用运费模板",
			{
			"freight_moudle":"测试模板1"
			},
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
		"area_setting":"不发货地区",
		"area_limit":"不发货模板",
		"freight":"使用运费模板",
			{
			"freight_moudle":"测试模板1"
			},
		},{
		"first_classify":"电子数码",
		"second_classify":"平板电脑",
		"shop_name": "ipad",
		"title":"苹果平板",
		"standard_promotion":"否",
		"price":3000.00,
		"setlement_price":2500.00,
		"weight":2.00,
		"area_setting":"不发货地区",
		"area_limit":"不发货模板",
		"freight":"使用运费模板",
			{
			"freight_moudle":"测试模板1"
			},
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

@panda @refuse
Scenario:运营驳回用户上传的商品
	Then yunying查看商品列表
		|product_name|consumer|	   classify      | source | sale | status |
		|  武汉鸭脖  |爱伲咖啡|   生活用品-零食  |        | 0.00 | 待入库 |
		| 耐克男鞋   |爱伲咖啡|   电子数码-耳机  |        | 0.00 | 待入库 |
		|  ipad      |爱伲咖啡|电子数码——平板电脑|        | 0.00 | 待入库 |
	When yunying驳回商品'耐克男鞋'
		"""
		[{
		"reason":"商品名称不规格"
		}]
		"""
	Then yunying查看商品列表
		|product_name|consumer|	   classify      | source | sale | status |
		|  武汉鸭脖  |爱伲咖啡|   生活用品-零食  |        | 0.00 | 待入库 |
		| 耐克男鞋   |爱伲咖啡|   电子数码-耳机  |        | 0.00 |入库驳回|
		|  ipad      |爱伲咖啡|电子数码——平板电脑|        | 0.00 | 待入库 |