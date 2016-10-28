#_author_:张三香 2016.10.25

Feature:运营端商品列表的查询
	"""
		运营端商品列表包含以下查询条件：
			客户名称:支持模糊查询
			商品名称:支持模糊查询
			入库状态:下拉框显示，包含全部、待入库、已入库，已同步、已入库，已停售、入库驳回、修改驳回；默认显示全部
			商品分类:支持一级分类和二级分类的模糊查询
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
	#添加商品
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
		#商品1-待入库
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
		#商品2-已入库,已同步
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
				"postage":2.00
				"image":["love.png"],
				"detail": "商品1描述信息"
			}
			"""
		#商品3-已入库,已停售
		When gddj添加商品
			"""
			{
				"product_category":"食品-饼干",
				"name":"商品3",
				"promotion_title":"促销标题3",
				"is_enable_model":false,
				"purchase_price": 30.00,
				"weight": 1,
				"stocks": 100,
				"limit_zone_type":"无限制",
				"postage":3.00,
				"image":["love.png"],
				"detail": "商品1描述信息"
			}
			"""
		Given lsjfd登录商品管理系统
		#商品4-入库驳回
		When lsjfd添加商品
			"""
			{
				"product_category":"食品-泡面",
				"name":"商品4",
				"promotion_title":"促销标题4",
				"is_enable_model":false,
				"purchase_price": 40.00,
				"weight": 1,
				"stocks": 100,
				"limit_zone_type":"无限制",
				"postage":4.00,
				"image":["love.png"],
				"detail": "商品4描述信息"
			}
			"""
		#商品5-修改驳回
		When lsjfd添加商品
			"""
			{
				"product_category":"食品-泡面",
				"name":"商品5",
				"promotion_title":"促销标题5",
				"is_enable_model":false,
				"purchase_price": 50.00,
				"weight": 1,
				"stocks": 100,
				"limit_zone_type":"无限制",
				"postage":5.00,
				"image":["love.png"],
				"detail": "商品5描述信息"
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
			"products":["商品2","商品3","商品5"],
			"platforms":["自营平台1"]
		}
		"""
	When yunying同步商品到自营平台
		"""
		{
			"products":["商品3"],
			"platforms":[],
			"not_sale_reason":"已过季"
		}
		"""
	When yunying在'商品'列表批量驳回修改商品
		"""
		{
			"name":["商品4"],
			"reject_reason":"驳回修改原因"
		}
		"""
	Given lsjfd登录商品管理系统
	When lsjfd编辑商品'商品5'
		"""
		{
			"product_category":"食品--泡面",
			"name":"商品5",
			"promotion_title":"促销标题5",
			"is_enable_model":false,
			"purchase_price": 55.00,
			"weight": 1,
			"stocks": 100,
			"limit_zone_type":"无限制",
			"postage":5.00,
			"image":["love.png"],
			"detail": "商品5描述信息"
		}
		"""
	Given yunying登录商品管理系统
	When yunying在'商品更新'列表驳回修改商品
		"""
		{
			"name":"商品5",
			"reject_reason":"驳回修改原因"
		}
		"""

Scenario:1 运营端商品列表默认查询
	Given yunying登录商品管理系统
	When yunying设置商品管理列表查询条件
		"""
		{
			"shop_name":"",
			"name":"",
			"storage_status":"全部",
			"product_category":""
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品5",
			"shop_name":"零售价返点店铺",
			"product_category":"食品-泡面",
			"customer_from":"--",
			"total_sales":0,
			"storage_status":"修改驳回",
			"product_label":[],
			"actions":["同步商品"]
		},{
			"name":"商品4",
			"shop_name":"零售价返点店铺",
			"product_category":"食品-泡面",
			"customer_from":"--",
			"total_sales":0,
			"storage_status":"入库驳回",
			"product_label":[],
			"actions":["删除商品"]
		},{
			"name":"商品3",
			"shop_name":"固定底价店铺",
			"product_category":"食品-饼干",
			"customer_from":"--",
			"total_sales":0,
			"storage_status":"已入库,已停售",
			"product_label":[],
			"actions":["同步商品","删除商品"]
		},{
			"name":"商品2",
			"shop_name":"固定底价店铺",
			"product_category":"食品-饼干",
			"customer_from":"--",
			"total_sales":0,
			"storage_status":"已入库,已同步",
			"product_label":[],
			"actions":["同步商品"]
		},{
			"name":"商品1",
			"shop_name":"固定底价店铺",
			"product_category":"食品-饼干",
			"customer_from":"--",
			"total_sales":0,
			"storage_status":"待入库",
			"product_label":[],
			"actions":["同步商品","驳回修改","删除商品"]
		}]
		"""

Scenario:2 运营端商品列表按'客户名称'查询
	#模糊匹配
	Given yunying登录商品管理系统
	When yunying设置商品管理列表查询条件
		"""
		{
			"shop_name":"零售"
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品5",
			"shop_name":"零售价返点店铺"
		},{
			"name":"商品4",
			"shop_name":"零售价返点店铺"
		}]
		"""
	#精确匹配
	When yunying设置商品管理列表查询条件
		"""
		{
			"shop_name":"零售价返点店铺"
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品5",
			"shop_name":"零售价返点店铺"
		},{
			"name":"商品4",
			"shop_name":"零售价返点店铺"
		}]
		"""
	#查询结果为空
	When yunying设置商品管理列表查询条件
		"""
		{
			"shop_name":"其他"
		}
		"""
	Then yunying获得商品列表
		"""
		[]
		"""

Scenario:3 运营端商品列表按'商品名称'查询
	#模糊匹配
	Given yunying登录商品管理系统
	When yunying设置商品管理列表查询条件
		"""
		{
			"name":"商品",
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品5"
		},{
			"name":"商品4"
		},{
			"name":"商品3"
		},{
			"name":"商品2"
		},{
			"name":"商品1"
		}]
		"""
	#精确匹配
	Given yunying登录商品管理系统
	When yunying设置商品管理列表查询条件
		"""
		{
			"name":"商品5",
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品5"
		}]
		"""
	#查询结果为空
	Given yunying登录商品管理系统
	When yunying设置商品管理列表查询条件
		"""
		{
			"name":"家电",
		}
		"""
	Then yunying获得商品列表
		"""
		[]
		"""

Scenario:4 运营端商品列表按'入库状态'查询
	#'待入库'状态
	Given yunying登录商品管理系统
	When yunying设置商品管理列表查询条件
		"""
		{
			"storage_status":"待入库"
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品1",
			"storage_status":"待入库"
		}]
		"""
	#'已入库,已同步'状态
	When yunying设置商品管理列表查询条件
		"""
		{
			"storage_status":"已入库,已同步"
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品2",
			"storage_status":"已入库,已同步"
		}]
		"""
	#'已入库,已停售'状态
	When yunying设置商品管理列表查询条件
		"""
		{
			"storage_status":"已入库,已停售"
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品3",
			"storage_status":"已入库,已停售"
		}]
		"""
	#'入库驳回'状态
	When yunying设置商品管理列表查询条件
		"""
		{
			"storage_status":"入库驳回"
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品4",
			"storage_status":"入库驳回"
		}]
		"""
	#'驳回修改'状态
	When yunying设置商品管理列表查询条件
		"""
		{
			"storage_status":"驳回修改"
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品5",
			"storage_status":"驳回修改"
		}]
		"""

Scenario:5 运营端商品列表按'商品分类'查询
	Given yunying登录商品管理系统
	#一级分类模糊查询
	When yunying设置商品管理列表查询条件
		"""
		{
			"product_category":"食"
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品5",
			"product_category":"食品-泡面"
		},{
			"name":"商品4",
			"product_category":"食品-泡面"
		},{
			"name":"商品3",
			"product_category":"食品-饼干"
		},{
			"name":"商品2",
			"product_category":"食品-饼干"
		},{
			"name":"商品1",
			"product_category":"食品-饼干"
		}]
		"""
	#一级分类精确查询
	When yunying设置商品管理列表查询条件
		"""
		{
			"product_category":"食品"
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品5",
			"product_category":"食品-泡面"
		},{
			"name":"商品4",
			"product_category":"食品-泡面"
		},{
			"name":"商品3",
			"product_category":"食品-饼干"
		},{
			"name":"商品2",
			"product_category":"食品-饼干"
		},{
			"name":"商品1",
			"product_category":"食品-饼干"
		}]
		"""
	#二级分类模糊查询
	When yunying设置商品管理列表查询条件
		"""
		{
			"product_category":"饼"
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品3",
			"product_category":"食品-饼干"
		},{
			"name":"商品2",
			"product_category":"食品-饼干"
		},{
			"name":"商品1",
			"product_category":"食品-饼干"
		}]
		"""
	#二级分类精确查询
	When yunying设置商品管理列表查询条件
		"""
		{
			"product_category":"泡面"
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品5",
			"product_category":"食品-泡面"
		},{
			"name":"商品4",
			"product_category":"食品-泡面"
		}]
		"""
	#查询结果为空
	When yunying设置商品管理列表查询条件
		"""
		{
			"product_category":"数码"
		}
		"""
	Then yunying获得商品列表
		"""
		[]
		"""

Scenario:6 运营端商品列表组合条件查询
	Given yunying登录商品管理系统
	When yunying设置商品管理列表查询条件
		"""
		{
			"shop_name":"固定底价店铺",
			"name":"商品1",
			"storage_status":"全部",
			"product_category":"食品"
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品1",
			"shop_name":"固定底价店铺",
			"product_category":"食品-饼干",
			"customer_from":"--",
			"total_sales":0,
			"storage_status":"待入库",
			"product_label":[],
			"actions":["同步商品","驳回修改","删除商品"]
		}]
		"""