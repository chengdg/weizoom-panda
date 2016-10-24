#author: 徐梓豪 2016-10-18
Feature:电子面单列表
"""
1.编辑信息
2.删除面单后查看列表
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
	When aini新增电子账单
		"""
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
		"monthcode":'P2016k30%ef213dl',
		"sendsite":"玄武网点"
		"comment":"备注"
		},{
		"express_company":"韵达快递",
		"CustomerName:'Yd00421',
		"CustomerPwd":,
		"monthcode":'P2016k26%sp001at',
		"sendsite":"秦淮网点"
		"comment":"备注"
		}]
		"""
	Then aini查看面单列表
		|shipper|mobile_number|    local_space   |   address   | postcode |
		|测试01 | 13813984402 |江苏省南京市玄武区| 中央门223号 |  210026  |
		|测试02 | 13813984403 |江苏省南京市秦淮区|   国创园47  |  210036  |

		|express_company|CustomerName|CustomerPwd|    monthcode   | SendSite |
		|   申通快递    |  93005812  |20161018001|   2016100005   | 下关网点 |
		|   圆通快递    |  YT00369   |    --     |P2016k30%ef213dl| 玄武网点 |
		|   秦淮网点    |  Yd00421   |    --     |P2016k26%sp001at| 秦淮网点 |

@panda @code
Scenario:1 编辑信息
	When aini编辑面单'测试01'
		"""
		[{
		"shipper":"测试XZH",
		"local_space":"江苏省南京市玄武区",
		"address":"中央门223号",
		"postcode":"210026",
		"mobile_number":13813984402,
		"company_name":"爱伲咖啡",
		"comment":"123"
		}]
		"""
	When aini编辑快递公司为'申通快递'的面单
		"""
		[{
		"express_company":"申通快递",
		"CustomerName:93005814,
		"CustomerPwd":20161018001,
		"monthcode":2016100005,
		"comment":"备注"
		}]
		"""
	Then aini查看面单列表
		|shipper|mobile_number|    local_space   |   address   | postcode |
		|测试XZH| 13813984402 |江苏省南京市玄武区| 中央门223号 |  210026  |
		|测试02 | 13813984403 |江苏省南京市秦淮区|   国创园47  |  210036  |

		|express_company|CustomerName|CustomerPwd|monthcode |
		|    申通快递   |  93005814  |20161018001|2016100005|

@panda @code
Scenario:2 删除面单后查看列表
	When aini删除联系人是'测试01'的面单
	Then aini查看面单列表
		|shipper|mobile_number|    local_space   |   address   | postcode |
		|测试02 | 13813984403 |江苏省南京市秦淮区|   国创园47  |  210036  |

		|express_company|CustomerName|CustomerPwd|monthcode |
		|    申通快递   |  93005812  |20161018001|2016100005|