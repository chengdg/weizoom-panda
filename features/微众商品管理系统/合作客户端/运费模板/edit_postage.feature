#_author_:张三香 2016.10.18

Feature:修改运费模板
	"""
		客户端用户可以修改运费模板
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

Scenario:1 修改运费模板（非默认模板）
	#修改非默认模板
	Given gddj登录商品管理系统
	When gddj修改运费模板'模板1'
		"""
		{
			"name":"模板1修改",
			"first_weight":1.0,
			"first_weight_price": 1.50,
			"added_weight":1.0,
			"added_weight_price": 1.50,
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
	Then gddj获得运费模板'模板1修改'
		"""
		{
			"name":"模板1修改",
			"first_weight":1.0,
			"first_weight_price": 1.50,
			"added_weight":1.0,
			"added_weight_price": 1.50,
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
			"name": "模板2",
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
			"name": "模板1修改",
			"is_postage_template":false,
			"postage_items":
				[{
					"postage_way":"普通快递",
					"to_the":["其他地区"],
					"first_weight": 1.0,
					"first_weight_price": 1.50,
					"added_weight": 1.0,
					"added_weight_price": 1.50
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

Scenario:2 修改运费模板（默认模板）
	#修改默认模板，模板列表信息变化同时使用该模板的商品详情页中模板名称也随之变化
	Given gddj登录商品管理系统
	When gddj设置默认模板'模板2'
	When gddj添加商品
		"""
		{
			"product_category":"食品-饼干"
			"name":"商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":false,
			"purchase_price": 10.00,
			"weight": 1,
			"stocks": 100,
			"limit_zone_type":"无限制",
			"postage":"模板2",
			"image":["love.png"],
			"detail": "商品1描述信息"
		}
		"""
	When gddj修改运费模板'模板2'
		"""
		{
			"name": "模板2修改",
			"first_weight": 1.0,
			"first_weight_price": 1.10,
			"added_weight": 1.0,
			"added_weight_price": 1.10,
			"special_area": [{
				"to_the": ["北京市"],
				"first_weight": 1.0,
				"first_weight_price": 2.20,
				"added_weight": 2.0,
				"added_weight_price": 2.20
				}]
		}
		"""
	Then gddj获得运费模板'模板2修改'
		"""
		{
			"name": "模板2修改",
			"first_weight": 1.0,
			"first_weight_price": 1.10,
			"added_weight": 1.0,
			"added_weight_price": 1.10,
			"special_area": [{
				"to_the": ["北京市"],
				"first_weight": 1.0,
				"first_weight_price": 2.20,
				"added_weight": 2.0,
				"added_weight_price": 2.20
				}]
		}
		"""
	Then gddj获得运费模板列表
		"""
		[{
			"name": "模板2修改",
			"is_postage_template":true,
			"postage_items":
				[{
					"postage_way":"普通快递",
					"to_the":["其他地区"],
					"first_weight": 1.0,
					"first_weight_price": 1.10,
					"added_weight": 1.0,
					"added_weight_price": 1.10
				},{
					"postage_way":"普通快递",
					"to_the":["北京市"],
					"first_weight": 1.0,
					"first_weight_price": 2.20,
					"added_weight": 2.0,
					"added_weight_price": 2.20
				}]
		},{
			"name": "模板1",
			"is_postage_template":false,
			"postage_items":
				[{
					"postage_way":"普通快递",
					"to_the":["全国"],
					"first_weight": 1.5,
					"first_weight_price": 4.00,
					"added_weight": 2.0,
					"added_weight_price":6.00
				}]
		},{
			"name": "系统默认",
			"is_postage_template":false,
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
	Then gddj获得商品'商品1'
		"""
		{
			"product_category":"食品-饼干"
			"name":"商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":false,
			"purchase_price": 10.00,
			"weight": 1,
			"stocks": 100,
			"limit_zone_type":"无限制",
			"postage":"模板2修改",
			"image":["love.png"],
			"detail": "商品1描述信息"
		}
		"""

Scenario:3 切换默认运费模板
	Given gddj登录系统
	When gddj添加商品
		"""
		{
			"product_category":"食品-饼干"
			"name":"商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":false,
			"purchase_price": 10.00,
			"weight": 1,
			"stocks": 100,
			"limit_zone_type":"无限制",
			"postage":"系统默认",
			"image":["love.png"],
			"detail": "商品1描述信息"
		}
		"""
	Then gddj获得商品'商品1'
		"""
		{
			"product_category":"食品-饼干"
			"name":"商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":false,
			"purchase_price": 10.00,
			"weight": 1,
			"stocks": 100,
			"limit_zone_type":"无限制",
			"postage":"系统默认",
			"image":["love.png"],
			"detail": "商品1描述信息"
		}
		"""
	#切换默认运费模板,验证运费模板列表的变化和使用运费模板商品的变化
	When gddj设置默认模板'模板2'
	Then gddj获得商品'商品1'
		"""
		{
			"product_category":"食品-饼干"
			"name":"商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":false,
			"purchase_price": 10.00,
			"weight": 1,
			"stocks": 100,
			"limit_zone_type":"无限制",
			"postage":"模板2",
			"image":["love.png"],
			"detail": "商品1描述信息"
		}
		"""
	Then gddj获得运费模板列表
		"""
		[{
			"name": "模板2",
			"is_postage_template":true
		},{
			"name": "模板1",
			"is_postage_template":false
		},{
			"name": "系统默认",
			"is_postage_template":false
		}]
		"""