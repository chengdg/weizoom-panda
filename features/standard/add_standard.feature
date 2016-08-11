#author:徐梓豪 2016-07-18
Feature:运营人员新增规格样式
"""
	1.新增显示样式为'文字'的规格样式
	2.新增显示样式为'图片'的规格样式
	3.删除规格值的中一个规格
	4.删除一整个规格样式
	5.编辑规格名称
"""

Background:
	Given manager 登录系统
	When manager新增账号
	"""
		[{
			"account_type":"体验客户",
			"company_name":"爱昵咖啡有限责任公司",
			"shop_name":"爱昵咖啡",
			"manage_type":"休闲食品",
			"purchase_type":"固定底价",
			"connect_man":"aini",
			"mobile_number":"13813985506",
			"login_account":"aini",
			"password":"123456",
			"valid_time":"2016-07-15"至"2017-07-15",
			"ramarks":"爱昵咖啡客户体验账号"
		}]
	"""	

@penda @hj
Scenario:1 新增显示样式为'文字'的规格样式
	Given aini登录系统
	When aini新增规格样式
	"""
		[{
			"standard_name":"尺码",
			"show_type":"文字",
			"standard":{
						"M","X","XL","XXL","XXXL"
					   }
		}]
	"""

	Then aini查看规格列表
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
	Given aini登录系统
	When aini新增规格样式
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
Scenario:3 删除规格值的中一个规格
	Given aini登录系统
	When aini删除规格样式'尺码'中的规格'XL'
	Then aini查看规格列表
		|standard_name| show_type |  standard |
		|    尺码     |    文字   |M,X,XXL,XXL|
		|    颜色     |    图像   |           |

@penda @hj
Scenario:4 删除一整个规格样式
	Given aini登录系统
	When aini删除规格样式'颜色'
	Then aini查看规格列表
		|standard_name| show_type |  standard |
		|    尺码     |    文字   |M,X,XXL,XXL|

@penda @hj
Scenario:5 编辑规格名称
	Given aini登录系统
	When aini编辑规格'颜色'
	[{
			"standard_name":"颜色234",
			"show_type":"文字",
			"standard":{
						"红","黄","蓝","绿","紫"
					   }
		}]
	"""

	Then aini获得规格列表
		|standard_name| show_type |   standard   |
		|    颜色     |    文字   |红,黄,蓝,绿,紫|

