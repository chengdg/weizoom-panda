#_author_:张三香 2016.10.18

Feature:删除运费模板
	"""
		客户端用户可以删除非默认的运费模板，删除默认的运费模板时会提示'操作失败，默认模板无法删除，请先将其他模板设为默认！'
	"""
Background:
	Given manager登录商品管理系统
	When manager添加账号
		"""
		{
			"type":"运营",
			"account_name":"运营账号1",
			"login_name":"yunying",
			"login_password":"test",
			"remark":"账号备注信息",
			"create_time":"2016-10-10 09:00:00"
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

	#添加'固定底价'类型客户
	Given manager登录商品管理系统
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
			"remark":"固定底价客户备注信息",
			"create_time":"2016-10-10 09:00:00"
		}
		"""

	Given gddj登录商品管理系统
	When ggdj添加运费模板
		"""
		{
			"name":"模板1",
			"first_weight":1.5,
			"first_weight_price": 4.00,
			"added_weight":2.0,
			"added_weight_price": 6.00
		}
		"""
	When ggdj添加运费模板
		"""
		{
			"name": "模板2",
			"first_weight": 1.0,
			"first_weight_price": 1.00,
			"added_weight": 1.0,
			"added_weight_price": 1.00,
			"special_area": [{
				"to_the": ["北京市"],
				"first_weight": 1.0,
				"first_weight_price": 2.00,
				"added_weight": 1.0,
				"added_weight_price": 2.00
				}],
			"free_postages": [{
				"to_the": ["上海市"],
				"condition":"count",
				"value": 1
			},{
				"to_the": ["北京市","重庆市","江苏省"],
				"condition":"money",
				"value": 20.0
			}]
		}
		"""

Scenario:1 删除运费模板
	Given gddj登录商品管理系统
	Then gddj获得运费模板列表
		"""
		[{
			"name": "模板2",
			"is_postage_template":false
		},{
			"name": "模板1",
			"is_postage_template":false
		},{
			"name": "系统默认",
			"is_postage_template":true
		}]
		"""
	#删除非默认模板
	When gddj删除运费模板'模板1'
	Then gddj获得运费模板列表
		"""
		[{
			"name": "模板2",
			"is_postage_template":false
		},{
			"name": "系统默认",
			"is_postage_template":true
		}]
		"""
	#删除默认模板
	When gddj删除运费模板'系统默认'
	Then gddj获得提示信息'操作失败，默认模板无法删除，请先将其他模板设为默认！'

	#将默认模板修改成非默认模板，再删除
	When gddj设置默认模板'模板2'
	When gddj删除运费模板'系统默认'
	Then gddj获得运费模板列表
		"""
		[{
			"name": "模板2",
			"is_postage_template":true
		}]
		"""