#author: 徐梓豪 2016-06-24
Feature:创建客户时，关联生成weapp的供货商 
"""
1.创建客户时，自动传到weapp系统中
"""

Background:
	When manager登录系统:penda
	Then manager添加账号
		"""
		{
		"account_type":"代理商",
		"account_name":"代理",
		"login_account":"daili",
		"login_password":"123456",
		"remarks":"123456"
		}
		"""
		Then manager查看账号列表
		| account_name | login_account | 
		|     代理     |     daili     |
@penda @hj
Scenario:1 创建客户时，自动传到weapp系统中
	When jobs登录系统:weapp
	Then jobs查看供应商列表
		|supp;ier_name|     add+time    |  principal  |  comments  |
		|    p-代理   |2016-06-27 13:32 |             |   123456   |    
  