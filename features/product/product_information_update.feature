auther:徐梓豪 2016-06-24
Feature:商品信息更新并同步至weapp系统
"""
1.修改商品信息后,客户点击更新按钮，运营审批通过后同步点击'更新'，同步至weapp系统
2.修改商品信息后,客户点击更新按钮，运营驳回
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
	When manager添加合作客户账号
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
	When yunying查看商品列表
	|goods_name| costumer_name |sales|              synchronous_goods           |
	|  周黑鸭  |     土小宝    | 0.00|weizoom_shop,weizoom_yijiaren,weizoom_home|
	|耐克男鞋  |     土小宝    | 0.00|                                          |
	When yunying同步商品'耐克男鞋'
	"""
	[{
	"synchronous_goods":{
					"weizoom_baifumei"
	}]
	"""
	Then yunying查看商品列表
	|goods_name| costumer_name |sales|              synchronous_goods           |
	|  周黑鸭  |     土小宝    | 0.00|weizoom_shop,weizoom_yijiaren,weizoom_home|
	|耐克男鞋  |     土小宝    | 0.00|            weizoom_baifumei              |

	Given tuxiaobao使用密码123456登录管理系统
	When tuxiaobao查看商品列表
	|  name   | set_price |sale_price| sales |   creat_time   | status |
	|武汉鸭脖 |   10.00   |   10.90  | 0.00  |2016-07-25 16:30| 未上架 |
	|耐克男鞋 |   198.00  |  322.00  | 0.00  |2016-07-25 16:30| 未上架 |

	Given jobs登录系统:weapp
	When jobs查看商品池
	|product_infomation|supplier|  price  | stock |operation|
	|     武汉鸭脖     |p-土小宝|  10.00  | 500.00|  上架   |
	|     耐克男鞋     |p-土小宝| 298.00  | 600.00|  上架   |
	When jobs上架商品'武汉鸭脖'
	Then jobs查看商品池
	|product_infomation|supplier|  price  | stock |operation|
	|     耐克男鞋     |p-土小宝| 298.00  | 600.00|  上架   |
	Then jobs查看在售商品列表
	|product_infomation|supplier|group|price| stock |sales|   creat_time   |sequence|
	|     武汉鸭脖     |p-土小宝|     |10.00| 500.00| 0.00|2016-06-29 18:50|        |

	Given tuxiaobao登录系统:panda
	When tuxiaobao查看商品列表
	|  name   | set_price |sale_price| sales |   creat_time   | status |
	|武汉鸭脖 |    9.90   |   9.90   | 0.00  |2016-07-25 16:30| 已上架 |
	|耐克男鞋 |   198.00  |  322.00  | 0.00  |2016-07-25 16:30| 未上架 |
 

@panda @update
Scenario:1 修改商品信息后,客户点击更新按钮，运营审批通过后同步点击'更新'，同步至weapp系统
	Given tuxiaobao登录系统:panda
	When tuxiaobao编辑商品'武汉鸭脖'
	"""
	{
	"name":"武汉鸭脖1",
	"title"："周黑鸭 鲜卤鸭脖 230g/袋 办公室休闲零食 肉干小食",
	"price":15.00,
	"setlement_price":12.00,
	"weight":1.50,
	"repertory":"700.00",
	"picture":"",
	"description":"周黑鸭 鲜卤鸭脖 230g/袋 办公室休闲零食 肉干小食"
	}
	"""	
	Then tuxiaobao查看商品列表
	|  name   | set_price |sale_price| sales |   creat_time   | status |
	|武汉鸭脖1|   12.00   |   15.00  | 0.00  |2016-07-25 16:30| 已上架 |
	|耐克男鞋 |   198.00  |  322.00  | 0.00  |2016-07-25 16:30| 未上架 |
	When tuxiaobao更新'武汉鸭脖1'的商品信息
	Given yunying登录系统:panda
	When yunying查看商品列表
	|goods_name| costumer_name |sales|              synchronous_goods           |
	|  周黑鸭  |     土小宝    | 0.00|weizoom_shop,weizoom_yijiaren,weizoom_home|
	|耐克男鞋  |     土小宝    | 0.00|                                          |
	Then yunying更新'武汉鸭脖1'的商品信息

	Given jobs登录系统
	When jobs查看在售商品列表
	|product_infomation|supplier|group|price| stock |sales|   creat_time   |sequence|
	|     武汉鸭脖     |p-土小宝|     |15.00| 700.00| 0.00|2016-06-29 18:50|        |

@panda @update
Scenario:2 修改商品信息后,客户点击更新按钮，运营驳回
	Given tuxiaobao登录系统:panda
	When tuxiaobao编辑商品'武汉鸭脖'
	"""
	{
	"name":"武汉鸭脖1",
	"title"："周黑鸭 鲜卤鸭脖 230g/袋 办公室休闲零食 肉干小食",
	"price":15.00,
	"setlement_price":12.00,
	"weight":1.50,
	"repertory":"700.00",
	"picture":"",
	"description":"周黑鸭 鲜卤鸭脖 230g/袋 办公室休闲零食 肉干小食"
	}
	"""	
	Then tuxiaobao查看商品列表
	|  name   | set_price |sale_price| sales |   creat_time   | status |
	|武汉鸭脖1|   12.00   |   15.00  | 0.00  |2016-07-25 16:30| 已上架 |
	|耐克男鞋 |   198.00  |  322.00  | 0.00  |2016-07-25 16:30| 未上架 |
	When tuxiaobao更新'武汉鸭脖1'的商品信息
	Given yunying登录系统:panda
	When yunying查看商品列表
	|goods_name| costumer_name |sales|              synchronous_goods           |
	|  周黑鸭  |     土小宝    | 0.00|weizoom_shop,weizoom_yijiaren,weizoom_home|
	|耐克男鞋  |     土小宝    | 0.00|                                          |
	Then yunying驳回商品'武汉鸭脖1'的更新申请
	"""
	{
	"reason":"投诉率较高",
	"comment":"商品315上投诉率较高"
	}
	"""





