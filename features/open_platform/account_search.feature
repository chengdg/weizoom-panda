author:徐梓豪 2016-09-14
feature:管理员通过登录名或主体名查询帐号 
"""
1.管理员通过登录名查询账号
2.管理员通过主题名查询账号
"""
Background:
	Given manager登录开放平台系统
	When manager创建开放平台账号
	"""
	[{
	"acoount_name":"aini",
	"password":"123456",
	"account_main":"爱伲咖啡",
	"isopen":"是"
	},{
	"acoount_name":"naike",
	"password":"123456",
	"account_main":"耐克男鞋",
	"isopen":"是"
	},{
	"acoount_name":"zhouheiya",
	"password":"123456",
	"account_main":"周黑鸭",
	"isopen":"是"
	}]
	"""
	Then manager查看账号列表
	| ID | account_name |  main_name  |   creat_time   |   statute   |   operation  |
	| 01 |     aini     |  爱伲咖啡   |2016-09-14 12:20|    已启用   |   编辑/关闭  |
	| 02 |    naike     |  耐克男鞋   |2016-09-14 12:21|    已启用   |   编辑/关闭  |
	| 03 |   zhouheiya  |   周黑鸭    |2016-09-14 12:23|    已启用   |   编辑/关闭  |

@poseidon @search
Scenario:1 管理员通过登录名查询账号
	Given manager登录系统
	When manager通过登录名查询账号
	"""
	{
	"account_name":"aini"
	}
	"""
	Then manager查看账号列表
	| ID | account_name |  main_name  |   creat_time   |   statute   |   operation  |
	| 01 |     aini     |  爱伲咖啡   |2016-09-14 12:20|    已启用   |   编辑/关闭  |
	When manager通过登录名查询账号
	"""
	{
	"account_name":"ai"
	}
	"""
	Then manager查看账号列表
	| ID | account_name |  main_name  |   creat_time   |   statute   |   operation  |
	| 01 |     aini     |  爱伲咖啡   |2016-09-14 12:20|    已启用   |   编辑/关闭  |
	| 02 |    naike     |  耐克男鞋   |2016-09-14 12:21|    已启用   |   编辑/关闭  |
	When manager通过登录名查询账号
	"""
	{
	"account_name":"hs"
	}
	"""
	Then manager查看账号列表
	| ID | account_name |  main_name  |   creat_time   |   statute   |   operation  |

@poseidon @search
Scenario:2 管理员通过主题名查询账号
	Given manager登录系统
	When manager通过主体名查询账号
	"""
	{
	"main_name":"爱伲咖啡"
	}
	"""
	Then manager查看账号列表
	| ID | account_name |  main_name  |   creat_time   |   statute   |   operation  |
	| 01 |     aini     |  爱伲咖啡   |2016-09-14 12:20|    已启用   |   编辑/关闭  |
	When manager通过主体名查询账号
	"""
	{
	"main_name":"鸭"
	}
	"""
	Then manager查看账号列表
	| ID | account_name |  main_name  |   creat_time   |   statute   |   operation  |
	| 03 |   zhouheiya  |   周黑鸭    |2016-09-14 12:23|    已启用   |   编辑/关闭  |
	When manager通过主体名查询账号
	"""
	{
	"main_name":"土小宝"
	}
	"""
	Then manager查看账号列表
	| ID | account_name |  main_name  |   creat_time   |   statute   |   operation  |
