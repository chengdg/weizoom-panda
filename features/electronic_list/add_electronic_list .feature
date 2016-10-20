#author: 徐梓豪 2016-07-14
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