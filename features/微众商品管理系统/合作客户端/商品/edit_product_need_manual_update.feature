#_author_:张三香 2016.10.25

Feature:客户端端编辑商品触发更新
	"""
		1.客户修改未同步的商品时，不会提示更新，修改保存后会直接更新到运营端
		2.客户修改未同步的'入库驳回'状态商品时，点击商品详情页中的【保存】按钮，只保存修改的信息不更改商品的状态，点击【重新修改提交】按钮，商品状态会由'入库驳回'变为'待入库'
		3.客户修改已同步的商品时，若修改以下情况会进入更新列表，需进行审核后人工更新
			a.修改商品的价格
			b.将无规格商品修改成多规格商品
			c.将多规格商品修改成无规格商品
			d.多规格商品删除其中的部分规格
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
			"remark":"账号备注信息"
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
	#客户添加商品
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
	When gddj添加商品
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":false,
			"purchase_price": 10.00,
			"weight": 1,
			"stocks": 100,
			"limit_zone_type":"无限制",
			"postage":1.00,
			"image":["love.png"],
			"detail": "商品1描述信息"
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
						"purchase_price": 21.00,
						"weight":1.0,
						"stocks":100
					},
					"白色 S": {
						"purchase_price": 22.00,
						"weight": 2.0,
						"stocks":200
					}
				}
			},
			"limit_zone_type":"无限制",
			"postage":2.00,
			"image":["love.png"],
			"detail": "商品2描述信息"
		}
		"""
	Given 添加自营平台账号
		"""
		[{
			"account":"zy1",
			"self_shop_name":"自营平台1"
		},{
			"account":"zy2",
			"self_shop_name":"自营平台2"
		}]
		"""
	Given yunying登录商品管理系统
	When yunying同步商品到自营平台
		"""
		{
			"products":["商品1","商品2"],
			"platforms":["自营平台1","自营平台2"]
		}
		"""
	Given zy1登录系统
	When zy1批量上架商品池商品
		"""
		["商品1","商品2"]
		"""

Scenario:1 客户端编辑已同步的商品（修改商品价格）
	Given gddj登录商品管理系统
	#固定底价客户修改商品的结算价
	When gddj编辑商品'商品1'
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":false,
			"purchase_price": 10.99,
			"weight": 1,
			"stocks": 100,
			"limit_zone_type":"无限制",
			"postage":1.00,
			"image":["love.png"],
			"detail": "商品1描述信息"
		}
		"""
	Then gddj获得商品列表
		"""
		[{
			"product_info":{"name":"商品2"},
			"product_category":"食品-饼干",
			"price":"21.00~2.00",
			"purchase_price":"21.00~22.00"
		},{
			"product_info":{"name":"商品1"},
			"product_category":"食品-饼干",
			"price":"10.99",
			"purchase_price":"10.99"
		}]
		"""
	Then gddj获得商品'商品1'
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":false,
			"purchase_price": 10.99,
			"weight": 1,
			"stocks": 100,
			"limit_zone_type":"无限制",
			"postage":1.00,
			"image":["love.png"],
			"detail": "商品1描述信息"
		}
		"""
	Given yunying登录商品管理系统
	Then yunying获得商品列表
		"""
		[{
			"name":"商品2"
		},{
			"name":"商品1"
		}]
		"""
	Then yunying获得商品'商品1'
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":false,
			"price": 10.99,
			"purchase_price": 10.99,
			"weight": 1,
			"stocks": 100,
			"limit_zone_type":"无限制",
			"postage":1.00,
			"image":["love.png"],
			"detail": "商品1描述信息"
		}
		"""
	Then yunying获得商品更新列表
		"""
		[{
			"product_info":
				{
					"name":"商品1",
					"image":"love.png"
				},
			"product_category":"食品-饼干",
			"shop_name":"固定底价店铺",
			"purchase_price":"10.99",
			"price":"10.99",
			"stocks":"100",
			"sale_status":"已上架",
			"actions":["商品更新","驳回修改"]
		}]
		"""

Scenario:2 客户端编辑已同步的商品（商品从无规格修改成多规格）
	Given gddj登录商品管理系统
	When gddj编辑商品'商品1'
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":true,
			"model": {
				"models": {
					"黑色": {
						"purchase_price": 11.00,
						"weight":1.0,
						"stocks":100
					},
					"白色": {
						"purchase_price": 12.00,
						"weight": 1.0,
						"stocks":200
					}
				}
			},
			"limit_zone_type":"无限制",
			"postage":1.00,
			"image":["love.png"],
			"detail": "商品1描述信息"
		}
		"""
	Then gddj获得商品列表
		"""
		[{
			"product_info":{"name":"商品2"},
			"product_category":"食品-饼干",
			"price":"21.00~22.00",
			"purchase_price":"21.00~22.00"
		},{
			"product_info":{"name":"商品1"},
			"product_category":"食品-饼干",
			"price":"11.00~12.00",
			"purchase_price":"11.00~12.00"
		}]
		"""
	Then gddj获得商品'商品1'
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":true,
			"model": {
				"models": {
					"黑色": {
						"purchase_price": 11.00,
						"weight":1.0,
						"stocks":100
					},
					"白色": {
						"purchase_price": 12.00,
						"weight": 1.0,
						"stocks":200
					}
				}
			},
			"limit_zone_type":"无限制",
			"postage":1.00,
			"image":["love.png"],
			"detail": "商品1描述信息"
		}
		"""
	Given yunying登录商品管理系统
	Then yunying获得商品列表
		"""
		[{
			"name":"商品2"
		},{
			"name":"商品1"
		}]
		"""
	Then yunying获得商品'商品1'
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":true,
			"model": {
				"models": {
					"黑色": {
						"purchase_price": 11.00,
						"weight":1.0,
						"stocks":100
					},
					"白色": {
						"purchase_price": 12.00,
						"weight": 1.0,
						"stocks":200
					}
				}
			},
			"limit_zone_type":"无限制",
			"postage":1.00,
			"image":["love.png"],
			"detail": "商品1描述信息"
		}
		"""
	Then yunying获得商品更新列表
		"""
		[{
			"product_info":
				{
					"name":"商品1",
					"image":"love.png"
				},
			"product_category":"食品-饼干",
			"shop_name":"固定底价店铺",
			"purchase_price":"11.00~12.00",
			"price":"11.00~12.00",
			"stocks":"100~200",
			"sale_status":"已上架",
			"actions":["商品更新","驳回修改"]
		}]
		"""

Scenario:3 客户端编辑已同步的商品（商品从多规格修改成无规格）
	Given gddj登录商品管理系统
	When gddj编辑商品'商品2'
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品2",
			"promotion_title":"促销标题2",
			"is_enable_model":false,
			"purchase_price": 20.00,
			"weight":1.0,
			"stocks":100
			"limit_zone_type":"无限制",
			"postage":2.00,
			"image":["love.png"],
			"detail": "商品2描述信息"
		}
		"""
	Then gddj获得商品列表
		"""
		[{
			"product_info":{"name":"商品2"},
			"product_category":"食品-饼干",
			"price":"20.00",
			"purchase_price":"20.00"
		},{
			"product_info":{"name":"商品1"},
			"product_category":"食品-饼干",
			"price":"10.00",
			"purchase_price":"10.00"
		}]
		"""
	Then gddj获得商品'商品2'
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品2",
			"promotion_title":"促销标题2",
			"is_enable_model":false,
			"purchase_price": 20.00,
			"weight":1.0,
			"stocks":100
			"limit_zone_type":"无限制",
			"postage":2.00,
			"image":["love.png"],
			"detail": "商品2描述信息"
		}
		"""
	Given yunying登录商品管理系统
	Then yunying获得商品列表
		"""
		[{
			"name":"商品2"
		},{
			"name":"商品1"
		}]
		"""
	Then yunging获得商品'商品2'
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品2",
			"promotion_title":"促销标题2",
			"is_enable_model":false,
			"price":20.00,
			"purchase_price": 20.00,
			"weight":1.0,
			"stocks":100
			"limit_zone_type":"无限制",
			"postage":2.00,
			"image":["love.png"],
			"detail": "商品2描述信息"
		}
		"""
	Then yunying获得商品更新列表
		"""
		[{
			"product_info":
				{
					"name":"商品2",
					"image":"love.png"
				},
			"product_category":"食品-饼干",
			"shop_name":"固定底价店铺",
			"purchase_price":"20.00",
			"price":"20.00",
			"stocks":"100",
			"sale_status":"已上架",
			"actions":["商品更新","驳回修改"]
		}]
		"""

Scenario:4 客户端编辑已同步的商品（多规格商品中增加或减少商品规格）
	Given gddj登录商品管理系统
	When gddj编辑商品'商品2'
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品2",
			"promotion_title":"促销标题2",
			"is_enable_model":true,
			"model": {
				"models": {
					"黑色 S": {
						"purchase_price": 21.00,
						"weight":1.0,
						"stocks":100
					}
				}
			},
			"limit_zone_type":"无限制",
			"postage":2.00,
			"image":["love.png"],
			"detail": "商品2描述信息"
		}
		"""
	Then gddj获得商品列表
		"""
		[{
			"product_info":{"name":"商品2"},
			"product_category":"食品-饼干",
			"price":"21.00",
			"purchase_price":"21.00"
		},{
			"product_info":{"name":"商品1"},
			"product_category":"食品-饼干",
			"price":"10.00",
			"purchase_price":"10.00"
		}]
		"""
	Given yunying登录商品管理系统
	Then yunying获得商品列表
		"""
		[{
			"name":"商品2"
		},{
			"name":"商品1"
		}]
		"""
	Then yunging获得商品'商品2'
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品2",
			"promotion_title":"促销标题2",
			"is_enable_model":true,
			"model": {
				"models": {
					"黑色 S": {
						"purchase_price": 21.00,
						"weight":1.0,
						"stocks":100
					}
				}
			},
			"limit_zone_type":"无限制",
			"postage":2.00,
			"image":["love.png"],
			"detail": "商品2描述信息"
		}
		"""
	Then yunying获得商品更新列表
		"""
		[{
			"product_info":
				{
					"name":"商品2",
					"image":"love.png"
				},
			"product_category":"食品-饼干",
			"shop_name":"固定底价店铺",
			"purchase_price":"21.00",
			"price":"21.00",
			"stocks":"100",
			"sale_status":"已上架",
			"actions":["商品更新","驳回修改"]
		}]
		"""