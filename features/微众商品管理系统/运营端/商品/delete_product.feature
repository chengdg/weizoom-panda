#_author_:张三香 2016.10.20

Feature:运营端商品列表删除商品
	"""
		1.运营端以下状态的商品可以进行删除操作
			待入库:【同步商品】【驳回修改】【删除商品】
			已入库,已停售:【同步商品】【删除商品】
			入库驳回:【删除商品】
		2.删除商品后，商品从运营端商品列表消失，对应客户端的商品也会随之消失
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
	When yunying添加商品分类
		"""
		{
			"服装":
			[{
				"name":"男装"
			},{
				"name":"女装"
			}]
		}
		"""
	#manager添加合作客户账号
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
				"product_category":["食品","服装"],
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
				"product_category":["食品","服装"],
				"products_limit":30,
				"contact_name":"张小小",
				"mobile":"13511223344",
				"start_time":"2016-10-11 10:00",
				"end_time":"2026-10-10 11:00",
				"login_name":"lsjfd",
				"login_password":"test",
				"remark":"零售价返点客户备注信息",
				"create_time":"2016-10-11 09:00:00"
			}
			"""
	#'固定底价'客户添加商品
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
				"name":"固定商品1",
				"promotion_title":"促销标题1",
				"is_enable_model":false,
				"purchase_price": 10.00,
				"weight": 1,
				"stocks": 100,
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
				"product_category":"食品-泡面",
				"name":"固定商品2",
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
	#'零售价返点'客户添加商品
		Given lsjfd登录商品管理系统
		When lsjfd添加商品规格
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
		When lsjfd添加商品
			"""
			{
				"product_category":"食品-饼干",
				"name":"零售商品1",
				"promotion_title":"促销标题1",
				"is_enable_model":false,
				"price": 10.00,
				"weight": 1,
				"stocks": 100,
				"limit_zone_type":"无限制",
				"postage":1.00,
				"image":["love.png"],
				"detail": "商品1描述信息",
				"create_time":"2016-10-19 08:00"
			}
			"""
		When lsjfd添加商品
			"""
			{
				"product_category":"服装-男装",
				"name":"零售商品2",
				"promotion_title":"促销标题2",
				"is_enable_model":true,
				"model": {
					"models": {
						"黑色": {
							"price": 20.00,
							"weight":2.0,
							"stocks":200
							}
						}
					},
				"limit_zone_type":"无限制",
				"postage":2.00,
				"image":["love.png"],
				"detail": "商品2描述信息",
				"create_time":"2016-10-19 09:00"
			}
			"""
	#创建自营平台
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

Scenario:1 运营端删除'待入库'状态的商品
	Given yunying登录商品管理系统
	When yunying删除商品'零售商品2'
	When yunying删除商品'固定商品1'
	#校验运营端商品列表
	Then yunying获得商品列表
		"""
		[{
			"name":"零售商品1"
		},{
			"name":"固定商品2"
		}]
		"""
	#校验对应客户端商品列表
	Given gddj登录商品管理系统
	Then gddj获得商品列表
		"""
		[{
			"product_info":{"name":"固定商品2"},
			"storage_status":"待入库",
			"sale_status":"未上架"
		}]
		"""
	Given lsjfd登录商品管理系统
	Then lsjfd获得商品列表
		"""
		[{
			"product_info":{"name":"零售商品1"},
			"storage_status":"待入库",
			"sale_status":"未上架"
		}]
		"""

Scenario:2 运营端删除'已入库,已停售'状态的商品
	Given yunying登录商品管理系统
	When yunying同步商品到自营平台
		"""
		{
			"products":["固定商品1"],
			"platforms":["自营平台1","自营平台2"]
		}
		"""
	When yunying同步商品到自营平台
		"""
		{
			"products":["固定商品1"],
			"platforms":[],
			"not_sale_reason":"已过季"
		}
		"""
	When yunying删除商品'固定商品1'
	#校验运营端商品列表变化
	Then yunying获得商品列表
		"""
		[{
			"name":"零售商品2"
		},{
			"name":"零售商品1"
		},{
			"name":"固定商品2"
		}]
		"""
	#校验对应客户端商品列表变化
	Given gddj登录商品管理系统
	Then gddj获得商品列表
		"""
		[{
			"product_info":{"name":"固定商品2"},
			"storage_status":"待入库",
			"sale_status":"未上架"
		}]
		"""

Scenario:3 运营端删除'入库驳回'状态的商品
	Given yunying登录商品管理系统
	When yunying在'商品'列表批量驳回修改商品
		"""
		{
			"name":["固定商品1"],
			"reject_reason":"驳回修改原因"
		}
		"""
	When yunying删除商品'固定商品1'
	#校验运营端商品列表变化
	Then yunying获得商品列表
		"""
		[{
			"name":"零售商品2"
		},{
			"name":"零售商品1"
		},{
			"name":"固定商品2"
		}]
		"""
	#校验对应客户端商品列表变化
	Given gddj登录商品管理系统
	Then gddj获得商品列表
		"""
		[{
			"product_info":{"name":"固定商品2"},
			"storage_status":"待入库",
			"sale_status":"未上架"
		}]
		"""