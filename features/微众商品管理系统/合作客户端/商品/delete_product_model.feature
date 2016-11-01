#_author_:张三香 2016.10.19

Feature:删除商品规格
	"""
		客户端允许客户删除整个商品规格
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
	When gddj添加商品规格
		"""
		{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "黑色",
				"image": "/standard_static/test_resource_img/hangzhou1.jpg"
			},{
				"name": "白色",
				"image": ""
			}]
		}
		"""
	When gddj添加商品规格
		"""
		{
			"name": "尺寸",
			"type": "文本",
			"values": [{
				"name": "M",
				"image":""
			},{
				"name": "S",
				"image": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]
		}
		"""

Scenario:1 删除商品规格（未被使用）
	Given gddj登录商品管理系统
	Then gddj能获取商品规格列表
		"""
		[{
			"name":"颜色"
		},{
			"name":"尺寸"
		}]
		"""
	When gddj删除商品规格'颜色'
	Then gddj能获取商品规格列表
		"""
		[{
			"name":"尺寸"
		}]
		"""
	When gddj删除商品规格'尺寸'
	Then gddj能获取商品规格列表
		"""
		[]
		"""

Scenario:2 删除商品规格（在被使用）
	1.创建如下多规格商品:
		商品1-黑色
		商品2-黑色 S  白色 S
		商品3-黑色 M  黑色 S
	2.当删除规格'颜色'后，校验商品的变化
		商品1-商品详情页规格为空
		商品2-商品详情页规格为空
		商品3-商品详情页规格为空
		备注:目前panda商品列表中对此种情况没有做处理（列表中显示的仍然是规格值未被删除时的信息）

	Given gddj登录商品管理系统
	When gddj添加商品
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":true,
			"model": {
				"models": {
					"黑色": {
						"purchase_price": 10.00,
						"weight":1.0,
						"stocks":100
					}
				}
			},
			"limit_zone_type":"无限制",
			"postage":1.00,
			"image":["love.png"],
			"detail": "商品1描述信息",
			"create_time":"2016-10-18 08:00"
		}
		"""
	When gddj添加商品
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品2",
			"promotion_title":"促销标题2",
			"is_enable_model":true,
			"model": {
				"models": {
					"黑色 S": {
						"purchase_price": 10.00,
						"weight":1.0,
						"stocks":100
					},
					"白色 S": {
						"purchase_price": 20.00,
						"weight": 2.0,
						"stocks":200
					}
				}
			},
			"limit_zone_type":"无限制",
			"postage":2.00,
			"image":["love.png"],
			"detail": "商品2描述信息",
			"create_time":"2016-10-18 09:00"
		}
		"""
	When gddj添加商品
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品3",
			"promotion_title":"促销标题3",
			"is_enable_model":true,
			"model": {
				"models": {
					"黑色 M": {
						"purchase_price": 10.00,
						"weight":1.0,
						"stocks":100
					},
					"黑色 S": {
						"purchase_price": 20.00,
						"weight": 2.0,
						"stocks":200
					}
				}
			},
			"limit_zone_type":"无限制",
			"postage":3.00,
			"image":["love.png"],
			"detail": "商品3描述信息",
			"create_time":"2016-10-18 10:00"
		}
		"""
	When gddj删除商品规格'颜色'
	#校验商品规格类别
	Then gddj能获取商品规格列表
		"""
		[{
			"name":"尺寸"
		}]
		"""
	#校验使用该规格的商品详情页
	Then gddj获得商品'商品1'
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":true,
			"model": {
				"models": {}
				},
			"limit_zone_type":"无限制",
			"postage":1.00,
			"image":["love.png"],
			"detail": "商品1描述信息",
			"create_time":"2016-10-18 08:00"
		}
		"""
	Then gddj获得商品'商品2'
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品2",
			"promotion_title":"促销标题2",
			"is_enable_model":true,
			"model": {
				"models": {}
				},
			"limit_zone_type":"无限制",
			"postage":2.00,
			"image":["love.png"],
			"detail": "商品2描述信息",
			"create_time":"2016-10-18 09:00"
		}
		"""
	Then gddj获得商品'商品3'
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品3",
			"promotion_title":"促销标题3",
			"is_enable_model":true,
			"model": {
				"models": {}
				},
			"limit_zone_type":"无限制",
			"postage":3.00,
			"image":["love.png"],
			"detail": "商品3描述信息",
			"create_time":"2016-10-18 10:00"
		}
		"""