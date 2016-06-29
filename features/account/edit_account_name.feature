auther:徐梓豪 2016-06-29
Feature:管理人员可以编辑账号名称
"""
	1.管理人员变更账号名称
"""
Background:
	Given manager登录管理系统
	When manager添加账号
	"""
		[{
			"account_type":"体验客户",
			"account_name":"土小宝",
			"login_account":"tuxiaobao",
			"password":123456,
			"ramarks":"土小宝客户体验账号"
		},{
			"account_type":"运营",
			"account_name":"运营部门",
			"login_account":"yunying",
			"password":123456,
			"ramarks":"运营部门"
		}]
	"""

	Then manager查看账号列表
		|account_name|login_account|
		|   土小宝   |  tuxiaobao  |
		|    运营    |   yunying   |

@penda @xzh
Scenario:1 管理人员变更账号名称
	Given manager登录管理系统
	When manager编辑'土小宝'的账号信息
	"""
		{
		"account_type":"体验客户",
			"account_name":"土小宝23",
			"login_account":"tuxiaobao",
			"password":123456,
			"ramarks":"土小宝客户体验账号"
		}
	"""
	Then manager查看账号列表
		|account_name|login_account|
		|  土小宝23  |  tuxiaobao  |
		|    运营    |   yunying   |
	When manager编辑'运营部门'的账号信息
	"""
		{
		"account_type":"运营",
		"account_name":"运营部门45",
		"login_account":"yunying",
		"password":123456,
		"ramarks":"运营部门"
		}
	"""
	Then manager查看账号列表
		|account_name|login_account|
		|  土小宝23  |  tuxiaobao  |
		|   运营45   |   yunying   |



