#_author_:张三香 2016.10.25

Feature:运营添加站内信
	"""
		1.运营通过"站内消息-系统消息"可以进行【+添加站内信】
		2.运营添加成功的站内消息会展示在运营端的'站内消息'列表和客户端的'站内消息'列表
	"""

Background:
	Given manager登录商品管理系统
	When manager添加账号
		"""
		{
			"type":"运营",
			"account_name":"运营账号1",
			"login_name":"yunying",
			"login_password":"test"
		}
		"""
	Given yunying登录商品管理系统
	When yunying添加商品分类
		"""
		{
			"食品":
			[{
				"name":"饼干"
			},{
				"name":"泡面"
			}]
		}
		"""

	Given manager登录商品管理系统
	#添加'固定底价'类型客户
	When manager添加账号
		"""
		{
			"type":"合作客户",
			"business_name":"北京大公司1",
			"shop_name":"固定底价店铺",
			"purchase_way":"固定底价",
			"payment_type":"自然月",
			"product_category":["食品"],
			"products_limit":300,
			"contact_name":"",
			"mobile":"",
			"start_time":"2016-10-10 10:00",
			"end_time":"2026-10-10 10:00",
			"login_name":"gddj",
			"login_password":"test",
			"remark":"固定底价客户备注信息"
		}
		"""
	#添加'零售价返点'类型客户
	When manager添加账号
		"""
		{
			"type":"合作客户",
			"business_name":"北京大公司2",
			"shop_name":"零售价返点店铺",
			"purchase_way":"零售价返点",
			"points":"20",
			"payment_type":"15天",
			"product_category":["食品"],
			"products_limit":30,
			"contact_name":"张小小",
			"mobile":"13511223344",
			"start_time":"2016-10-11 10:00",
			"end_time":"2026-10-10 11:00",
			"login_name":"lsjfd",
			"login_password":"test",
			"remark":"零售价返点客户备注信息"
		}
		"""

Scenario:1 运营添加站内信
	Given yunying登录商品管理系统
	When yunying添加站内信
		"""
		{
			"title":"站内消息1",
			"details":"添加商品时要注意图片的格式",
			"attachment":"",
			"create_time":"2016-10-10 08:00:00"
		}
		"""
	When yunying添加站内信
		"""
		{
			"title":"站内消息2",
			"details":"站内消息2详情信息",
			"attachment":"abc.gif",
			"create_time":"2016-10-10 08:10:00"
		}
		"""
	#运营端站内消息列表校验
	Then yunying获得站内消息列表
		"""
		[{
			"title":"站内消息2",
			"create_time":"2016-10-10 08:10:00",
			"actions":["修改","删除"]
		},{
			"title":"站内消息1",
			"create_time":"2016-10-10 08:00:00",
			"actions":["修改","删除"]
		}]
		"""
	#客户端站内消息列表校验
	Given gddj登录商品管理系统
	Then gddj获得站内消息列表
		"""
		[{
			"title":"站内消息2",
			"create_time":"2016-10-10 08:10:00"
		},{
			"title":"站内消息1",
			"create_time":"2016-10-10 08:00:00"
		}]
		"""
	Given lsjfd登录商品管理系统
	Then lsjfd获得站内消息列表
		"""
		[{
			"title":"站内消息2",
			"create_time":"2016-10-10 08:10:00"
		},{
			"title":"站内消息1",
			"create_time":"2016-10-10 08:00:00"
		}]
		"""