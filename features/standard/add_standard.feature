#author:徐梓豪 2016-07-18
Feature:运营人员新增规格样式
"""
	1.新增显示样式为'文字'的规格样式
	2.新增显示样式为'图片'的规格样式
	3.删除规格值的中一个规格
	4.
"""

Background:
	Given manager 登录系统
	When manager新增账号
	"""
		[{
			"account_type":"运营",
			"account_name":"运营",
			"login_account":"yunying",
			"password":"123456"
		}]
	"""	

@penda @hj
Scenario:1 新增显示样式为'文字'的规格样式
	Given yunying登录系统
	When yunying新增规格样式
	"""
		[{
			"standard_name":"尺码",
			"show_type":"文字",
			"standard":{
						"M","X","XL","XXL","XXXL"
					   }
		}]
	"""

	Then yunying查看订单列表
	"""
		[{
			"standard_name":"尺码",
			"show_type":"文字",
			"standard":{
						"M","X","XL","XXL","XXXL"
					   }
		}]
	"""

@penda @hj
Scenrio:2 新增显示样式为'图片'的规格样式
	Given yunying登录系统
	When yunying新增规格样式
	"""
		[{
			"standard_name":"颜色",
			"show_type":"图片",
			"standard":{
						"","","","",""
					   }
		}]
	"""
	Then yunying查看规格列表
		|standard_name| show_type |   standard   |
		|    尺码     |    文字   |M,X,XL,XXL,XXL|
		|    颜色     |    图像   |              |

@penda @hj
Scenario:3删除规格值的中一个规格
	Given yunying登录系统
	When yunying删除规格样式'尺码'中的规格'XL'
	Then yunying查看规格列表
		|standard_name| show_type |  standard |
		|    尺码     |    文字   |M,X,XXL,XXL|
		|    颜色     |    图像   |           |