auther:徐梓豪 2016-08-23
Feature:客户修改已上架的商品信息，运营进行更新商品
"""
1.运营更新商品信息
2.运营驳回商品更新请求
"""
Background:
Given manager登录管理系统
	When manager添加账号
	"""
	[{
	"account_type":"体验客户",
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
	},{
	"account_type":"运营",
	"account_name":"运营部门",
	"login_account":"yunying",
	"password":123456,
	"ramarks":"运营部门"
	}]
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
	When manager为账号'爱伲咖啡'编辑分类权限
	"""
	{
	"account_type":"体验客户",
	'product_style':{
					"电子数码"，
					"生活用品"
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
	| goods_name | costumer_name |  product_style   |sales  |  status  |synchronous_platform|
	|  武汉鸭脖  |   爱伲咖啡    |  生活用品--零食  | 0.00  |  已同步  |微众商城,微众家,微众白富美|
	|  耐克男鞋  |   爱伲咖啡    |  电子数码--耳机  | 0.00  |  已同步  |微众家,微众白富美   |
	|    ipad    |   爱伲咖啡    |电子数码--平板电脑| 0.00  |  未同步  |					|
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
	|武汉鸭脖 |   8.00    |   10.00  | 0.00  |2016-07-25 16:30| 已上架 |
	|耐克男鞋 |   14.90   |   29.00  | 0.00  |2016-07-25 16:30| 已上架 |
	|  ipad   |  3000.00  |  2500.00 | 0.00  |2016-08-22 11:03| 未上架 |

@panda @update
Scenario:1 运营更新商品信息
	Given aini登录系统:panda
	When aini编辑商品信息
	"""
	[{
	"first_classify":"生活用品",
	"second_classify":"零食",
	"product_name": "武汉鸭脖",
	"title":"武汉鸭脖",
	"introduction": "这是一种很好吃的鸭脖"
	"standard_promotion":"否",
	"price":20.00,
	"setlement_price":10.00,
	"weight":1.00,
	"repertory":"100.00",
	"picture":"",
	"description":"周黑鸭 鲜卤鸭脖 230g/袋 办公室休闲零食 肉干小食"
	},{
	"first_classify":"电子数码",
	"second_classify":"平板电脑",
	"shop_name": "ipad",
	"title":"苹果平板",
	"standard_promotion":"否",
	"price":3100.00,
	"setlement_price":2400.00,
	"weight":2.00,
	"repertory":"500.00",
	"picture":"",
	"description":"苹果平板，大屏看电视"
	}]
	"""
	Then aini查看商品列表
	|  name   | set_price |sale_price| sales |   creat_time   | status |
	|武汉鸭脖 |   10.00   |   20.00  | 0.00  |2016-07-25 16:30| 已上架 |
	|耐克男鞋 |   14.90   |   29.00  | 0.00  |2016-07-25 16:30| 已上架 |
	|  ipad   |  2400.00  |  3100.00 | 0.00  |2016-08-22 11:03| 未上架 |
	Given yunying登录系统:panda
	When yunying查看商品列表
	| goods_name | costumer_name |  product_style   |sales  |  status  |synchronous_platform|
	|  武汉鸭脖  |   爱伲咖啡    |  生活用品--零食  | 0.00  |  已同步  |微众商城,微众家,微众白富美|
	|  耐克男鞋  |   爱伲咖啡    |  电子数码--耳机  | 0.00  |  已同步  |微众家,微众白富美   |
	|    ipad    |   爱伲咖啡    |电子数码--平板电脑| 0.00  |  未同步  |					|
	Then yunying查看商品更新列表
	| goods_name | product_style | supplier | sale_price | set_price | stocks | statute |operate|
	|  武汉鸭脖  | 生活用品--零食| 爱伲咖啡 |    20.00   |    10.00  | 100.00 | 已上架  |更新 驳回|
	Then yunying更新商品
	"""
	{
	"goods_name":"武汉鸭脖"
	}
	"""
	Then yunying查看商品更新列表
	| goods_name | product_style | supplier | sale_price | set_price | stocks | statute |operate|

	Given jobs登录系统:weapp
	When jobs查看商品池
	|  information  | supplier   | group | price | stocks | synchronous_time |
	Then jobs查看在售商品列表
	|  information  | supplier   | group | price |     stocks      | sales |  putaway_time  |
	|    武汉鸭脖   | p-爱伲咖啡 |       | 20.00 |     100.00      |  0.00 |2016-08-23 10:06|              
	|    耐克男鞋   | p-爱伲咖啡 |       | 29.00 | 1000.00-2500.00 |  0.00 |2016-08-23 10:06|

@panda @update
Scenario:2 运营驳回商品更新请求
	Given aini登录系统:panda
	When aini编辑商品信息
	"""
	[{
	"first_classify":"生活用品",
	"second_classify":"零食",
	"product_name": "武汉鸭脖",
	"title":"武汉鸭脖",
	"introduction": "这是一种很好吃的鸭脖"
	"standard_promotion":"否",
	"price":20.00,
	"setlement_price":10.00,
	"weight":1.00,
	"repertory":"100.00",
	"picture":"",
	"description":"周黑鸭 鲜卤鸭脖 230g/袋 办公室休闲零食 肉干小食"
	},{
	"first_classify":"电子数码",
	"second_classify":"平板电脑",
	"shop_name": "ipad",
	"title":"苹果平板",
	"standard_promotion":"否",
	"price":3100.00,
	"setlement_price":2400.00,
	"weight":2.00,
	"repertory":"500.00",
	"picture":"",
	"description":"苹果平板，大屏看电视"
	}]
	"""
	Then aini查看商品列表
	|  name   | set_price |sale_price| sales |   creat_time   | status |
	|武汉鸭脖 |   10.00   |   20.00  | 0.00  |2016-07-25 16:30| 已上架 |
	|耐克男鞋 |   14.90   |   29.00  | 0.00  |2016-07-25 16:30| 已上架 |
	|  ipad   |  2400.00  |  3100.00 | 0.00  |2016-08-22 11:03| 未上架 |
	Given yunying登录系统:panda
	When yunying查看商品列表
	| goods_name | costumer_name |  product_style   |sales  |  status  |synchronous_platform|
	|  武汉鸭脖  |   爱伲咖啡    |  生活用品--零食  | 0.00  |  已同步  |微众商城,微众家,微众白富美|
	|  耐克男鞋  |   爱伲咖啡    |  电子数码--耳机  | 0.00  |  已同步  |微众家,微众白富美   |
	|    ipad    |   爱伲咖啡    |电子数码--平板电脑| 0.00  |  未同步  |					|
	Then yunying查看商品更新列表
	| goods_name | product_style | supplier | sale_price | set_price | stocks | statute |operate|
	|  武汉鸭脖  | 生活用品--零食| 爱伲咖啡 |    20.00   |    10.00  | 100.00 | 已上架  |更新 驳回|
	Then yunying驳回商品
	"""
	{
	"goods_name":"武汉鸭脖"
	}
	"""
	Then yunying填写驳回原因
	"""
	{
	"reason":"投诉率过高",
	"comment":"315投诉率较高，无法上架出售"
	}
	"""
	Then yunying查看商品更新列表
	| goods_name | product_style | supplier | sale_price | set_price | stocks | statute |operate|


