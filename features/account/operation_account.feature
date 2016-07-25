#author: 许韦 2016.05.30

Feature:精简版云商通-运营账号权限
"""
	1.运营账号可以查看所有客户添加的商品列表,按照商品创建的时间倒序排列
	2.运营账号点击商品名称可以查看商品的详情页面,不可编辑
	3.运营账号可以给商家创建的商品添加关联,选择自营平台的商家名称,填写商品在自营平台对应的id,即可关联成功
		若id不正确或者不存在,给出错误提示:“请输入正确的商品ID”。
	4.运营账号可以修改商家创建的商品关联,选择自营平台的商家名称,编辑商品在自营平台对应的id,即可关联成功
		若id不正确或者不存在,给出错误提示:“请输入正确的商品ID”。
"""

Background:
	Given jobs登录管理系统
	When jobs添加账号
	"""
		[{
			"account_type":"合作客户",
			"account_name":"土小宝",
			"login_account":"tuxiaobao",
			"password":"123456",
			"ramarks":"土小宝客户体验账号"
		},{
			"account_type":"合作客户",
			"account_name":"爱昵咖啡",
			"login_account":"aini",
			"password":"123456",
			"ramarks":"爱昵咖啡客户体验账号"
		},{
			"account_type":"运营",
			"account_name":"运营部门",
			"login_account":"yunying",
			"password":"123456",
			"ramarks":"运营部门"
		}]
	"""
	When aini使用密码123456登录系统
	When aini添加商品
	"""
		[{
			"name": "商品1",
			"promotion_name":"促销的商品1",
			"price": 12.00,
			"weight": 1.00,
			"stock_type": "无限",
			"settlement_price":10.00,
			"introduction": "商品1的简介"
		}]
	"""
	When tuxiaobao使用密码123456登录系统
	When tuxiaobao添加商品
	"""
		[{
			"name": "商品2",
			"promotion_name":"促销的商品2",
			"settlement_price":10.00,
			"introduction": "商品2的简介",
			"price": 12.00,
			"weight": 1.00,
			"stock_type": "无限",
			"settlement_price":10.00,
			"introduction": "商品2的简介"
		},{
			"name": "商品3",
			"promotion_name":"促销的商品3",
			"price": 12.00,
			"weight": 1.00,
			"stock_type": "无限",
			"settlement_price":10.00,
			"introduction": "商品3的简介"
		}]
	"""

@panda @yunying
Scenario:1 运营账号查看所有商品列表
	When yunying使用密码123456登录系统
	Then yunying能获得所有商品列表
	"""
		[{
			"name":"商品3",
			"account_name":"土小宝",
			"sales":"0",
			"weapp_id":[]
		},{
			"name":"商品2",
			"account_name":"土小宝",
			"sales":"0",
			"weapp_id":[]
		},{
			"name":"商品1",
			"account_name":"爱昵咖啡",
			"sales":"0",
			"weapp_id":[]
		}]
	"""

# @panda @yunying
# Scenario:2 运营账号查看商品详情
# 	When yunying使用密码123456登录系统
# 	Then yunying能获得'商品3'商品详情
# 	"""
# 		[{
# 			"name": "商品3",
# 			"promotion_name":"促销的商品3",
# 			"price": "12.00",
# 			"weight": "1.00",
# 			"stock_type": "无限",
# 			"settlement_price": "10.00",
# 			"introduction": "商品3的简介"		
# 		}]
# 	"""

@panda @yunying
Scenario:3 运营账号添加商品绑定
	When yunying使用密码123456登录系统
	When yunying绑定商品关联的云商通商品
	"""
		[{
			"name":"商品3",
			"weapp_id":[]
		},{
			"name":"商品2",
			"weapp_id":[{"微众家":"1"}]	
		},{
			"name":"商品1",
			"weapp_id":[{"微众家":"1"},{"微众商城":"2"}]
		}]
	"""
	Then yunying能获得所有商品列表
	"""
		[{
			"name":"商品3",
			"account_name":"土小宝",
			"sales":"0",
			"weapp_id":[]
		},{
			"name":"商品2",
			"account_name":"土小宝",
			"sales":"0",
			"weapp_id":[{"微众家":"1"}]	
		},{
			"name":"商品1",
			"account_name":"爱昵咖啡",
			"sales":"0",
			"weapp_id":[{"微众家":"1"},{"微众商城":"2"}]
		}]
	"""

@panda @yunying
Scenario:4 运营账号修改商品绑定
	When yunying使用密码123456登录系统
	When yunying绑定商品关联的云商通商品
	"""
		[{
			"name":"商品3",
			"weapp_id":[{"微众家":1}]
		},{
			"name":"商品2",
			"weapp_id":[{"微众商城":2}]	
		},{
			"name":"商品1",
			"weapp_id":[{"微众家":3}]
		}]
	"""
	Then yunying能获得所有商品列表
	"""
		[{
			"name":"商品3",
			"account_name":"土小宝",
			"sales":"0",
			"weapp_id":[{"微众家":"1"}]
		},{
			"name":"商品2",
			"account_name":"土小宝",
			"sales":"0",
			"weapp_id":[{"微众商城":"2"}]
		},{
			"name":"商品1",
			"account_name":"爱昵咖啡",
			"sales":"0",
			"weapp_id":[{"微众家":"3"}]
		}]
	"""
	When yunying修改商品关联的云商通商品
	"""
		[{
			"name":"商品3",
			"weapp_id":[{"微众家":1},{"微众商城":4}]
		},{
			"name":"商品2",
			"weapp_id":[]	
		},{
			"name":"商品1",
			"weapp_id":[{"微众商城":5}]
		}]
	"""
	Then yunying能获得所有商品列表
	"""
		[{
			"name":"商品3",
			"account_name":"土小宝",
			"sales":"0",
			"weapp_id":[{"微众家":"1"},{"微众商城":"4"}]
		},{
			"name":"商品2",
			"account_name":"土小宝",
			"sales":"0",
			"weapp_id":[]
		},{
			"name":"商品1",
			"account_name":"爱昵咖啡",
			"sales":"0",
			"weapp_id":[{"微众商城":"5"}]
		}]
	"""