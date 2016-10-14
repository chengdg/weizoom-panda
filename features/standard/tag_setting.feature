auther:徐梓豪 2016-08-31
Feature:运营人员配置标签
"""
1.运营人员为分类进行标签配置
2.运营人员为商品配置标签
3.运营人员在商品配置过标签后更换商品标签
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
	When manager添加客户账号
	"""
		{
		"account_type":"体验客户",
		"company_name":"爱昵咖啡有限责任公司",
		"manage_type"{"电子数码"，
					  "生活用品"
						},
		"shop_name":"爱昵咖啡",
		"manage_type":"休闲食品",
		"purchase_type":"固定底价",
		"connect_man":"aini",
		"mobile_number":"13813985506",
		"login_account":"aini",
		"password":"123456",
		"valid_time":"2016-07-15"至"2017-07-15",
		"settlement_time":"15天"
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

	Given yunying登录管理系统
	When yunying新增标签
		"""
		{
		"classify":"国家",
		"tag":{
				"美国"，"法国","中国","德国","意大利","澳大利亚"
		},{
		"classify":"省市",
		"tag":{
				"江苏"，"黑龙江","广东","浙江","北京","江西"
		},{
		"classify":"基本信息",
		"tag":{
				"男"，"女","新生儿","9-13岁","14-18岁","成年"
			}
		}
		"""
		Then yunying查看标签列表
		|classify|                tag                 |
		|  国家  |美国，法国,中国,德国,意大利,澳大利亚|
		|  省市  |  江苏，黑龙江,广东,浙江,北京,江西  |
		|基本信息| 男，女,新生儿,9-13岁,14-18岁,成年  | 

@panda @tag_setting
Scenario:1 运营人员为分类进行标签配置
	Given yunying登录系统
	When yunying配置标签
		#类目
		"""
		{
		"classify_name":"平板电脑"
		}
		"""
		#标签
		"""
		[{
		"classify":"国家",
		"tag":{
				"美国","法国"
			}
		}]
		"""
	已选择:
	国家:美国法国

	Then yunying查看类目列表
		|classify_name|     creat_time    | business_number |             operate           |
		|   电子数码  |2016-07-21 15:30:08|      0.00       |修改 删除 配置特殊资质 标签配置|
		|     耳机    |2016-07-21 15:30:25|      0.00       |修改 删除 配置特殊资质 标签配置|
		|     手机    |2016-07-21 15:31:25|      0.00       |修改 删除 配置特殊资质 标签配置|
		|   平板电脑  |2016-07-21 15:32:25|      0.00       |修改 删除 配置特殊资质 美国;法国|
		|   生活用品  |2016-07-21 15:31:27|      0.00       |修改 删除 配置特殊资质 标签配置|
		|     零食    |2016-07-21 15:31:25|      0.00       |修改 删除 配置特殊资质 标签配置|
		|     肥皂    |2016-07-21 15:31:25|      0.00       |修改 删除 配置特殊资质 标签配置|
		|   清洗用品  |2016-07-21 15:31:25|      0.00       |修改 删除 配置特殊资质 标签配置|

	When yunying配置标签
		#类目
		"""
		{
		"classify":"零食"
		}
		"""
		#标签
		"""
		[{
		"classify":"省市",
		"tag":{
				"江苏","黑龙江"
			}
		},{
		"classify":"基本信息",
		"tag":{
				"男","女"
			}
		}]
		"""
		已选择:
		省市:江苏,黑龙江
		基本信息:男,女

		Then yunying查看类目列表
		|classify_name|     creat_time    | business_number |             operate           |
		|   电子数码  |2016-07-21 15:30:08|      0.00       |修改 删除 配置特殊资质 标签配置|
		|     耳机    |2016-07-21 15:30:25|      0.00       |修改 删除 配置特殊资质 标签配置|
		|     手机    |2016-07-21 15:31:25|      0.00       |修改 删除 配置特殊资质 标签配置|
		|   平板电脑  |2016-07-21 15:32:25|      0.00       |修改 删除 配置特殊资质 美国;法国|
		|   生活用品  |2016-07-21 15:31:27|      0.00       |修改 删除 配置特殊资质 标签配置|
		|     零食    |2016-07-21 15:31:25|      0.00       |修改 删除 配置特殊资质 江苏;黑龙江;男;女|
		|     肥皂    |2016-07-21 15:31:25|      0.00       |修改 删除 配置特殊资质 标签配置|
		|   清洗用品  |2016-07-21 15:31:25|      0.00       |修改 删除 配置特殊资质 标签配置|

@panda @tag
Scenairo:2 运营人员为商品配置标签
	Given yunying登录系统
	When yunying配置标签
		#类目
		"""
		{
		"classify_name":"零食"
		}
		"""
		#标签
		"""
		[{
		"classify":"国家",
		"tag":"法国"
		},{
		"classify":"基本信息",
		"tag":"男"
		}]
		"""
	已选择:
	国家:美国法国
	Then yunying查看类目列表
		|classify_name|     creat_time    | business_number |             operate           |
		|   电子数码  |2016-07-21 15:30:08|      0.00       |修改 删除 配置特殊资质 标签配置|
		|     耳机    |2016-07-21 15:30:25|      0.00       |修改 删除 配置特殊资质 标签配置|
		|     手机    |2016-07-21 15:31:25|      0.00       |修改 删除 配置特殊资质 标签配置|
		|   平板电脑  |2016-07-21 15:32:25|      0.00       |修改 删除 配置特殊资质 标签配置|
		|   生活用品  |2016-07-21 15:31:27|      0.00       |修改 删除 配置特殊资质 标签配置|
		|     零食    |2016-07-21 15:31:25|      0.00       |修改 删除 配置特殊资质 法国,男 |
		|     肥皂    |2016-07-21 15:31:25|      0.00       |修改 删除 配置特殊资质 标签配置|
		|   清洗用品  |2016-07-21 15:31:25|      0.00       |修改 删除 配置特殊资质 标签配置|
	Then yunying查看商品列表
		|  name   |costumer_name|     classify     | set_price |sale_price| sales |   creat_time   | status |
		|武汉鸭脖 |  爱伲咖啡   |  生活用品-零食   |   10.00   |    8.00  | 0.00  |2016-07-25 16:30| 未上架 |
		|耐克男鞋 |  爱伲咖啡   |  电子数码-耳机   |   14.90   |   29.00  | 0.00  |2016-07-25 16:30| 未上架 |
		|  ipad   |  爱伲咖啡   |电子数码——平板电脑|  3000.00  |  2500.00 | 0.00  |2016-08-22 11:03| 未上架 |
	When yunying为商品'武汉鸭脖'配置标签
		"""
		[{
		"classify":"基本信息",
		"tag":{
				"男","女"
		},{
		"classify":"国家",
		"tag":"中国"	
		}]
		"""
	Then yunying查看商品'武汉鸭脖'的标签
		"""
		{
		"tag":"男","女","中国"	
		}
		"""
	When yunying配置标签
		#类目
		"""
		{
		"classify_name":"零食"
		}
		"""
		#标签
		"""
		[{
		"classify":"国家",
		"tag":"法国"
		},{
		"classify":"基本信息",
		"tag":"成年"
		}]
		"""
	Then yunying查看商品'武汉鸭脖'的标签
		"""
		{
		"tag":"男","女","中国"	
		}
		"""

@panda @tag
Scenario:3 运营人员在商品配置过标签后更换商品标签
	Given yunying登录系统
	When yunying配置标签
		#类目
		"""
		{
		"classify_name":"零食"
		}
		"""
		#标签
		"""
		[{
		"classify":"国家",
		"tag":"法国"
		},{
		"classify":"基本信息",
		"tag":"男"
		}]
		"""
		#类目
		"""
		{
		"classify_name":"耳机"
		}
		"""
		#标签
		"""
		[{
		"classify":"省市",
		"tag":"江苏"
		},{
		"classify":"基本信息",
		"tag":"14-18岁"
		}]
		"""
	已选择:
	国家:美国法国
	Then yunying查看类目列表
		|classify_name|     creat_time    | business_number |             operate           |
		|   电子数码  |2016-07-21 15:30:08|      0.00       |修改 删除 配置特殊资质 标签配置|
		|     耳机    |2016-07-21 15:30:25|      0.00       |修改 删除 配置特殊资质 标签配置|
		|     手机    |2016-07-21 15:31:25|      0.00       |修改 删除 配置特殊资质 标签配置|
		|   平板电脑  |2016-07-21 15:32:25|      0.00       |修改 删除 配置特殊资质 标签配置|
		|   生活用品  |2016-07-21 15:31:27|      0.00       |修改 删除 配置特殊资质 标签配置|
		|     零食    |2016-07-21 15:31:25|      0.00       |修改 删除 配置特殊资质 法国,男 |
		|     肥皂    |2016-07-21 15:31:25|      0.00       |修改 删除 配置特殊资质 标签配置|
		|   清洗用品  |2016-07-21 15:31:25|      0.00       |修改 删除 配置特殊资质 标签配置|
	Then yunying查看商品列表
		|  name   |costumer_name|     classify     | set_price |sale_price| sales |   creat_time   | status |
		|武汉鸭脖 |  爱伲咖啡   |  生活用品-零食   |   10.00   |    8.00  | 0.00  |2016-07-25 16:30| 未上架 |
		|耐克男鞋 |  爱伲咖啡   |  电子数码-耳机   |   14.90   |   29.00  | 0.00  |2016-07-25 16:30| 未上架 |
		|  ipad   |  爱伲咖啡   |电子数码——平板电脑|  3000.00  |  2500.00 | 0.00  |2016-08-22 11:03| 未上架 |
	When yunying为商品'武汉鸭脖'配置标签
		"""
		[{
		"classify":"基本信息",
		"tag":{
				"男","女"
		},{
		"classify":"国家",
		"tag":"中国"	
		}]
		"""
	Then yunying查看商品'武汉鸭脖'的标签
		"""
		{
		"tag":"男","女","中国"	
		}
		"""
	When yunying配置标签
		#类目
		"""
		{
		"classify_name":"零食"
		}
		"""
		#标签
		"""
		{
		"tag":"法国","成年"	
		}
		"""
	Then yunying查看商品'武汉鸭脖'的标签
		"""
		{
		"tag":"男","女","中国"	
		}
		"""
	Given aini登录系统
	When aini编辑商品信息
		"""
		{
		"first_classify":"电子数码",
		"second_classify":"耳机",
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
		}
		"""
	Given yunying登录系统
	Then yunying查看商品列表
		|  name   |costumer_name|     classify     | set_price |sale_price| sales |   creat_time   | status |
		|武汉鸭脖 |  爱伲咖啡   |  电子数码-耳机   |   10.00   |    8.00  | 0.00  |2016-07-25 16:30| 未上架 |
		|耐克男鞋 |  爱伲咖啡   |  电子数码-耳机   |   14.90   |   29.00  | 0.00  |2016-07-25 16:30| 未上架 |
		|  ipad   |  爱伲咖啡   |电子数码——平板电脑|  3000.00  |  2500.00 | 0.00  |2016-08-22 11:03| 未上架 |
	Then yunying查看商品'武汉鸭脖'的标签
		"""
		{
		"tag":{
				"14-18岁,"江苏""
			}
		}
		"""

