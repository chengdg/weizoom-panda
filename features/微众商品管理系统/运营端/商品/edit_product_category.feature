#_author_:张三香 2016.10.28 

Feature:运营端商品列表修改商品分类
	"""
		1.商品列表右侧操作列中增加【修改分类】按钮；
		2.修改分类支持批量修改操作，在批量同步右侧增加【修改分类】按钮；
		3.点击【修改分类】按钮，弹框内显示系统所有的一级和二级分类，分类仅支持单选。选择后，确定后，弹框关闭，提示：修改分类成功；
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
			"product_category":["食品","服装"],
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
		Given lsjfd登录商品管理系统
		#商品3-已入库,已同步
		When lsjfd添加商品
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
				"detail": "商品3描述信息"
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
			"products":["商品2","商品3"],
			"platforms":["自营平台1","自营平台2"]
		}
		"""
	Given zy1登录系统
	When zy1批量上架商品池商品
		"""
		["商品3"]
		"""

Scenario:1 运营端商品列表修改商品分类
	Given yunying登录商品管理系统
	#修改'待入库'商品的商品分类
	When yunying在商品列表批量修改商品分类
		"""
		{
			"procucts":["商品1"],
			"product_category":"食品-泡面"
		}
		"""
	#修改'已入库,已同步'商品的商品分类
	When yunying在商品列表批量修改商品分类
		"""
		{
			"procucts":["商品2","商品3"],
			"product_category":"服装-男装"
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品3",
			"product_category":"服装-男装",
			"storage_status":"已同步,已入库"
		},{
			"name":"商品2",
			"product_category":"服装-男装",
			"storage_status":"已同步,已入库"
		},{
			"name":"商品1",
			"product_category":"食品-泡面",
			"storage_status":"待入库"
		}]
		"""

	#客户单商品列表的校验
	Given gddj登录商品管理系统
	Then gddj获得商品列表
		"""
		[{
			"product_info":{"name":"商品2"},
			"product_category":"服装-男装",
			"storage_status":"已入库",
			"sale_status":"未上架"
		},{
			"product_info":{"name":"商品1"},
			"product_category":"食品-泡面",
			"storage_status":"待入库",
			"sale_status":"未上架"
		}]
		"""

	Given lsjfd登录商品管理系统
	Then lsjfd获得商品列表
		"""
		[{
			"product_info":{"name":"商品3"},
			"product_category":"服装-男装",
			"storage_status":"已入库",
			"sale_status":"已上架"
		}]
		"""

	#weapp端商品池列表和在售商品列表的校验
	Given zy1登录系统
	Then zy1获得商品池所有商品列表
		"""
		[{
			"product_info":{"name":"商品2"},
			"product_category":"服装-男装"
		}]
		"""
	Then zy1能获得'在售'商品列表
		"""
		[{
			"product_info":{"name":"商品3"},
			"product_category":"服装-男装"
		}]
		"""

	Given zy2登录系统
	Then zy1获得商品池所有商品列表
		"""
		[{
			"product_info":{"name":"商品3"},
			"product_category":"服装-男装"
		},{
			"product_info":{"name":"商品2"},
			"product_category":"服装-男装"
		}]
		"""