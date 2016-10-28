#_author_:张三香 2016.10.18

Feature:添加运费模板
	"""
		1、客户端用户可以添加运费模板
		2、运费模板列表会存在一个'系统默认'模板
		3、运费模板列表顺序：添加时间的倒序显示
		4、运费模板名称显示在对应模板字段表的上方，若设置为默认则名称后面红字显示'（默认）',若未设置默认则名称后面显示【设为默认】按钮
		5、当运费模板设置了包邮条件后，模板列表中运费模板名称后面显示'（已设置包邮条件）'
		6、当模板既设置了默认又设置了包邮条件，显示格式：xxx（已设置包邮条件）（默认）
		7、运费模板列表字段信息如下:
			运送方式:均显示'普通快递'
			运送到:显示选择的地区信息（全国或其他地区/北京市/天津市;上海市;河北省）
			首重（kg）:设置的首重数量
			运费（元）:设置的首重运费
			续重（kg）:设置的续重数量
			续费（元）:设置的续重运费
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

Scenario:1 添加运费模板（无特殊地区运费设置、无包邮条件设置）
	Given gddj登录商品管理系统
	Then gddj获得运费模板列表
		"""
		[{
			"name":"系统默认",
			"is_postage_template":true,
			"postage_items":
				[{
					"postage_way":"普通快递",
					"to_the":["全国"],
					"first_weight":1.0,
					"first_weight_price":0.00,
					"added_weight":1.0,
					"added_weight_price":0.00
				}]
		}]
		"""
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
	Then ggdj获得运费模板'模板1'
		"""
		{
			"name":"模板1",
			"first_weight":1.5,
			"first_weight_price": 4.00,
			"added_weight":2.0,
			"added_weight_price": 6.00
		}
		"""
	Then gddj获得运费模板列表
		"""
		[{
			"name":"模板1",
			"is_postage_template":false,
			"postage_items":
				[{
					"postage_way":"普通快递",
					"to_the":["全国"],
					"first_weight": 1.5,
					"first_weight_price": 4.00,
					"added_weight": 2.0,
					"added_weight_price": 6.00
				}]
		},{
			"name":"系统默认",
			"is_postage_template":true,
			"postage_items":
				[{
					"postage_way":"普通快递",
					"to_the":["全国"],
					"first_weight": 1.0,
					"first_weight_price": 0.00,
					"added_weight": 1.0,
					"added_weight_price": 0.00
				}]
		}]
		"""

Scenario:2 添加运费模板（有特殊地区运费设置、无包邮条件设置）
	Given gddj登录商品管理系统
	When ggdj添加运费模板
		"""
		{
			"name": "模板1",
			"first_weight": 1.0,
			"first_weight_price": 1.00,
			"added_weight": 1.0,
			"added_weight_price": 1.00,
			"special_area": [{
				"to_the":["北京市"],
				"first_weight":1.0,
				"first_weight_price":2.00,
				"added_weight":1.0,
				"added_weight_price":2.00
			},{
				"to_the":["上海市","重庆市","江苏省"],
				"first_weight": 1.0,
				"first_weight_price": 3.00,
				"added_weight": 1.0,
				"added_weight_price": 3.00
			}]
		}
		"""
	Then ggdj获得运费模板'模板1'
		"""
		{
			"name": "模板1",
			"first_weight": 1.0,
			"first_weight_price": 1.00,
			"added_weight": 1.0,
			"added_weight_price": 1.00,
			"special_area": [{
				"to_the":["北京市"],
				"first_weight":1.0,
				"first_weight_price":2.00,
				"added_weight":1.0,
				"added_weight_price":2.00
			},{
				"to_the":["上海市","重庆市","江苏省"],
				"first_weight": 1.0,
				"first_weight_price": 3.00,
				"added_weight": 1.0,
				"added_weight_price": 3.00
			}]
		}
		"""
	Then gddj获得运费模板列表
		"""
		[{
			"name": "模板1",
			"is_postage_template":false,
			"postage_items":
				[{
					"postage_way":"普通快递",
					"to_the":["其他地区"],
					"first_weight": 1.0,
					"first_weight_price": 1.00,
					"added_weight": 1.0,
					"added_weight_price": 1.00
				},{
					"postage_way":"普通快递",
					"to_the":["北京市"],
					"first_weight": 1.0,
					"first_weight_price": 2.00,
					"added_weight": 1.0,
					"added_weight_price": 2.00
				},{
					"postage_way":"普通快递",
					"to_the":["上海市","重庆市","江苏省"],
					"first_weight": 1.0,
					"first_weight_price": 3.00,
					"added_weight": 1.0,
					"added_weight_price":3.00
				}]
		},{
			"name": "系统默认",
			"is_postage_template":true,
			"postage_items":
				[{
					"postage_way":"普通快递",
					"to_the":["全国"],
					"first_weight": 1.0,
					"first_weight_price": 0.00,
					"added_weight": 1.0,
					"added_weight_price": 0.00
				}]
		}]
		"""

Scenario:3 添加运费模板（无特殊地区运费设置、有包邮条件设置）
	Given gddj登录商品管理系统
	When ggdj添加运费模板
		"""
		{
			"name": "模板1",
			"first_weight": 1.0,
			"first_weight_price": 1.00,
			"added_weight": 1.0,
			"added_weight_price": 1.00,
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
	Then ggdj获得运费模板'模板1'
		"""
		{
			"name": "模板1",
			"first_weight": 1.0,
			"first_weight_price": 1.00,
			"added_weight": 1.0,
			"added_weight_price": 1.00,
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
	Then gddj获得运费模板列表
		"""
		[{
			"name": "模板1",
			"is_postage_template":false,
			"postage_items":
				[{
					"postage_way":"普通快递",
					"to_the":["全国"],
					"first_weight": 1.0,
					"first_weight_price": 1.00,
					"added_weight": 1.0,
					"added_weight_price": 1.00
				}]
		},{
			"name": "系统默认",
			"is_postage_template":true,
			"postage_items":
				[{
					"postage_way":"普通快递",
					"to_the":["全国"],
					"first_weight": 1.0,
					"first_weight_price": 0.00,
					"added_weight": 1.0,
					"added_weight_price": 0.00
				}]
		}]
		"""

Scenario:4 添加运费模板（有特殊地区运费设置、有包邮条件设置）
	Given gddj登录商品管理系统
	When ggdj添加运费模板
		"""
		{
			"name": "模板1",
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
	Then ggdj获得运费模板'模板1'
		"""
		{
			"name": "模板1",
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
	Then gddj获得运费模板列表
		"""
		[{
			"name": "模板1",
			"is_postage_template":false,
			"postage_items":
				[{
					"postage_way":"普通快递",
					"to_the":["其他地区"],
					"first_weight": 1.0,
					"first_weight_price": 1.00,
					"added_weight": 1.0,
					"added_weight_price": 1.00
				},{
					"postage_way":"普通快递",
					"to_the":["北京市"],
					"first_weight": 1.0,
					"first_weight_price": 2.00,
					"added_weight": 1.0,
					"added_weight_price": 2.00
				}]
		},{
			"name": "系统默认",
			"is_postage_template":true,
			"postage_items":
				[{
					"postage_way":"普通快递",
					"to_the":["全国"],
					"first_weight": 1.0,
					"first_weight_price": 0.00,
					"added_weight": 1.0,
					"added_weight_price": 0.00
				}]
		}]
		"""