#author: 张雪 2016-5-6

Feature:精简版云商通-创建体验客户、代理商、运营账号
"""
	1.管理员创建体验客户账号
	2.管理员创建代理商账号
	3.管理员创建运营账号

"""
#account_type   账号类型
#account_name   账号名称
#login_account  登录账号
#password       密码
#remarks        备注

@panda @kuki
Scenario:1  管理员创建体验客户账号
	Given jobs登录管理系统
	When jobs添加账号
	"""
		[{
			"account_type":"体验客户",
			"account_name":"爱昵咖啡",
			"login_account":"aini",
			"password":"123456",
			"ramarks":"爱昵咖啡客户体验账号"
		},{
			"account_type":"体验客户",
			"account_name":"土小宝",
			"login_account":"tuxiaobao",
			"password":"123456",
			"ramarks":"土小宝客户体验账号"
		}]
	"""
	Then jobs能获得账号管理列表
	"""
		[{
			"account_name":"土小宝",
			"login_account":"tuxiaobao",
			"actions": ["编辑","开启"]
		},{
			"account_name":"爱昵咖啡",
			"login_account":"aini",
			"actions": ["编辑","开启"]
		}]
	"""

@panda
Scenario:2  管理员创建代理商账号
	Given jobs登录管理系统
	When jobs添加账号
	"""
		[{
			"account_type":"代理商",
			"account_name":"代理商公司",
			"login_account":"daili",
			"password":"123456",
			"ramarks":"代理商有限公司"
		}]
	"""
	Then jobs能获得账号管理列表
	"""
		[{
			"account_name":"代理商公司",
			"login_account":"daili",
			"actions": ["编辑","开启"]
		}]
	"""


@panda
Scenario:3  管理员创建运营账号
	Given jobs登录系统
	When jobs添加账号
	"""
		[{
			"account_type":"运营",
			"account_name":"运营部门",
			"login_account":"yunying",
			"password":"123456",
			"ramarks":"运营部门"
		},{
			"account_type":"代理商",
			"account_name":"代理商公司",
			"login_account":"daili",
			"password":"123456",
			"ramarks":"代理商有限公司"
		},{
			"account_type":"体验客户",
			"account_name":"爱昵咖啡",
			"login_account":"aini",
			"password":"123456",
			"ramarks":"爱昵咖啡客户体验账号"
		}]
	"""
	Then jobs能获得账号管理列表
	"""
		[{
			"account_name":"爱昵咖啡",
			"login_account":"aini",
			"actions": ["编辑","开启"]
		},{
			"account_name":"代理商公司",
			"login_account":"daili",
			"actions": ["编辑","开启"]
		},{
			"account_name":"运营部门",
			"login_account":"yunying",
			"actions": ["编辑","开启"]
		}]
	"""
