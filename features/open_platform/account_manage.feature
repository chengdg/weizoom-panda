author:徐梓豪 2016-09-13
feature:管理员管理开放平台
"""
1.管理员创建开放平台账号
2.管理员编辑开放平台账号
3.管理员关闭开放平台账号
"""
Background:
	Given manager登录开放平台系统

@poseidon	
Scenario:1 管理员创建开放平台账号
	Given manager登录开放平台系统
	When manager创建账号
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

@poseidon
Scenario:2 管理员编辑开放平台账号
	Given manager登录管理系统
	When manager创建账号
		"""
		{
		"acoount_name":"aini",
		"password":"123456",
		"account_main":"爱伲咖啡",
		"isopen":"是"
		}
		"""
	Then manager查看账号列表
		| ID | account_name |  main_name  |   creat_time   |   statute   |   operation  |
		| 01 |     aini     |   爱伲咖啡  |2016-09-13 15:20|    已启用   |   编辑/关闭  |
	Then manager编辑账号'爱伲咖啡'
		"""
		{
		"acoount_name":"aini",
		"password":"123456",
		"account_main":"爱伲coffee",
		"isopen":"是"
		}
		"""
	Then manager查看账号列表
		| ID | account_name |  main_name  |   creat_time   |   statute   |   operation  |
		| 01 |     aini     |  爱伲coffee |2016-09-13 15:20|    已启用   |   编辑/关闭  |
	
@poseidon
Scenario:3 管理员关闭平台账号
	Given manager登录管理系统
	When manager创建账号
		"""
		{
		"acoount_name":"aini",
		"password":"123456",
		"account_main":"爱伲咖啡",
		"isopen":"是"
		}
		"""
	Then manager查看账号列表
		| ID | account_name |  main_name  |   creat_time   |   statute   |   operation  |
		| 01 |     aini     |   爱伲咖啡  |2016-09-13 15:20|    已启用   |   编辑/关闭  |

	Then manager关闭账号
		"""
		{
		"account_name":"aini"
		}
		"""
	Then manager查看账号列表
		| ID | account_name |  main_name  |   creat_time   |   statute   |   operation  |
		| 01 |     aini     |   爱伲咖啡  |2016-09-13 15:20|    未激活   |   编辑/关闭  |

