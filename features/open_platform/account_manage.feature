auther:徐梓豪 2016-09-13
feature:
"""
1.运营创建开放平台账号
2.运营编辑开放平台账号
3.运营关闭开放平台账号
"""
Background:
	Given manager登录管理系统
	When manager创建运营账号
	"""
	{
	"account_type":"运营",
	"account_name":"运营部门",
	"login_account":"yunying",
	"password":123456,
	"ramarks":"运营部门"
	} 
	"""
Scenario:1 运营创建开放平台账号
	Given yunying登录管理系统
	When yunying创建账号
	"""
	{
	"acoount_name":"aini",
	"password":"123456",
	"account_main":"爱伲咖啡",
	"isopen":"是"
	}
	"""
	Then yunying查看账号列表
	| ID | account_name |  main_name  |   creat_time   |   statute   |   operation  |
	| 01 |     aini     |   爱伲咖啡  |2016-09-13 15:20|    已启用   |   编辑/关闭  |

Scenario:2 运营编辑开放平台账号
	Given yunying登录管理系统
	When yunying创建账号
	"""
	{
	"acoount_name":"aini",
	"password":"123456",
	"account_main":"爱伲咖啡",
	"isopen":"是"
	}
	"""
	Then yunying查看账号列表
	| ID | account_name |  main_name  |   creat_time   |   statute   |   operation  |
	| 01 |     aini     |   爱伲咖啡  |2016-09-13 15:20|    已启用   |   编辑/关闭  |
	Then yunying编辑账号'爱伲咖啡'
	"""
	{
	"acoount_name":"aini",
	"password":"123456",
	"account_main":"爱伲coffee",
	"isopen":"是"
	}
	Then yunying查看账号列表
	| ID | account_name |  main_name  |   creat_time   |   statute   |   operation  |
	| 01 |     aini     |  爱伲coffee |2016-09-13 15:20|    已启用   |   编辑/关闭  |

Scenario:3 运营关闭平台账号
	Given yunying登录管理系统
	When yunying创建账号
	"""
	{
	"acoount_name":"aini",
	"password":"123456",
	"account_main":"爱伲咖啡",
	"isopen":"是"
	}
	"""
	Then yunying查看账号列表
	| ID | account_name |  main_name  |   creat_time   |   statute   |   operation  |
	| 01 |     aini     |   爱伲咖啡  |2016-09-13 15:20|    已启用   |   编辑/关闭  |

	Then yunying关闭账号
	"""
	{
	"account_name":"aini"
	}
	"""
	Then yunying查看账号列表
	| ID | account_name |  main_name  |   creat_time   |   statute   |   operation  |
	| 01 |     aini     |   爱伲咖啡  |2016-09-13 15:20|    未激活   |   编辑/关闭  |

