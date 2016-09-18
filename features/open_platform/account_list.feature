author:徐梓豪 2016-09-14
feature:管理员浏览账号列表

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
@poseidon
Scenario:1 管理员浏览账号列表
	Given manager登录开放平台系统
	Then manager查看账号列表
	| ID | account_name |  main_name  |   creat_time   |   statute   |   operation  |
	| 01 |     aini     |  爱伲咖啡   |2016-09-14 12:20|    已启用   |   编辑/关闭  |
	| 02 |    naike     |  耐克男鞋   |2016-09-14 12:21|    已启用   |   编辑/关闭  |
	| 03 |   zhouheiya  |   周黑鸭    |2016-09-14 12:23|    已启用   |   编辑/关闭  |

