#author: 徐梓豪 2016-10-24
Feature:订单列表打印电子账单
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
	When aini新增电子账单
		"""
		[{
		"shipper":"测试01",
		"local_space":"江苏省南京市玄武区",
		"address":"中央门223号",
		"postcode":"210026",
		"mobile_number":13813984402,
		"company_name":"爱伲咖啡",
		"comment":"123"
		},{
		"shipper":"测试02",
		"local_space":"江苏省南京市秦淮区",
		"address":"国创园47",
		"postcode":"210036",
		"mobile_number":13813984403,
		"company_name":"土小宝",
		"comment":"备注"
		},{
		"express_company":"申通快递",
		"CustomerName:93005812,
		"CustomerPwd":20161018001,
		"monthcode":2016100005,
		"sendsite":"玄武网点",
		"comment":"备注"
		},{
		"express_company":"圆通快递",
		"CustomerName:'YT00369',
		"CustomerPwd":,
		"monthcode":'P2016k26%sp001at',
		"sendsite":"玄武网点"
		"comment":"备注"
		},{
		"express_company":"韵达快递",
		"CustomerName:'Yd00421',
		"CustomerPwd":,
		"monthcode":'P2016k26%sp001at',
		"sendsite":"玄武网点"
		"comment":"备注"
		}]
		"""
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
	Given yunying登录系统
	When yunying同步商品'周黑鸭'
		"""
		[{
		"synchronous_goods":{
						"weizoom_home",
						"weizoom_yijiaren",
						"weizoom_shop"
		}]
		"""

	When aini'测试02'设为默认
	Then aini查看面单列表
		|shipper     |mobile_number|    local_space   |   address   | postcode |
		|测试01      | 13813984402 |江苏省南京市玄武区| 中央门223号 |  210026  |
		|测试02(默认)| 13813984403 |江苏省南京市秦淮区|   国创园47  |  210036  |

		|express_company|CustomerName|CustomerPwd|    monthcode   | SendSite |
		|   申通快递    |  93005812  |20161018001|   2016100005   | 下关网点 |
		|   圆通快递    |  YT00369   |    --     |P2016k30%ef213dl| 玄武网点 |
		|   秦淮网点    |  Yd00421   |    --     |P2016k26%sp001at| 秦淮网点 |
	Given jobs 登录系统:weapp
	When jobs上架商品
		"""
		[{
		"product_name":"武汉鸭脖"
		},{
		"product_name":"耐克男鞋"
		},{
		"product_name":"ipad"
		}]
	When 微信用户在公众号上下订单后，panda这获取订单列表
	Then aini查看订单列表
		|      order_id       |product_name|   price/num   |customer| order_price |freight| statute | date |
		|       201606121001  |  武汉鸭脖  |    10.00/1.00 |        |    10.00    |  10.00| 待发货  |下单时间|
		|       201606121002  |  耐克男鞋  |    29.00/1.00 |        |    29.00    |  15.00| 待发货  |下单时间|
		|20161019180211777^37s|    ipad    | 3000.00/1.00  |        |   3000.00   |   0.00| 待发货  |下单时间|

@panda @electronic
Scenario:订单列表打印电子账单
	When aini选择所有商品,点击批量打印面单
	When aini选择物流公司
		"""
		[{
		"express_company":"中通速递"
		}]
		"""
	Then 系统提示'没有该物流公司的面单设置'
	When aini选择所有商品,点击批量打印面单
	When aini选择物流公司
		"""
		[{
		"express_company":"圆通通速递"
		}]
		""
	Then aini预览面单
	Then aini店里立即打印
