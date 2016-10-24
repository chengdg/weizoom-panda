#author: 徐梓豪 2016-10-18
Feature:新增电子面单
"""
1.新增快递发货人
2.新增快递公司电子面单账号
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
@panda @electronic
Scenario:1 新增快递发货人
	Given yunying登录系统
	When yunying新增电子账单
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
		}]
		"""

@panda @electronic
Scenario:2 新增快递公司电子面单账号
	Given yunying登录系统
	When yunying新增电子账单
		"""
		[{
		"express_company":"申通快递",
		"CustomerName:93005812,
		"CustomerPwd":20161018001,
		"monthcode":2016100005,
		"comment":"备注"
		}]
		"""