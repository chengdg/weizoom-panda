#_author_:张三香 2016.10.19

Feature:固定底价客户商品列表的查询
	"""
		备注：固定底价客户添加商品页面隐藏'售价'字段，商品列表页中显示售价，其值默认和结算价相等
		1、商品列表查询条件
			商品名称:模糊查询
			商品分类：输入框显示，支持一级和二级分类的模糊查询
			入库状态：下拉框显示全部、待入库、已入库、入库驳回，默认显示全部
		2、商品列表字段信息
			商品信息：显示商品图片和名称
			分类：显示商品的分类
			售价（元）：显示商品的售价，默认和结算价相同（保留2位小数）
			销量：商品的销量
			创建时间：商品的创建时间（格式为xxxx-xx-xx xx:xx）
			入库状态：待入库（运营未同步）/已入库（运营已同步）/已驳回（红字显示并且鼠标悬停?时，显示驳回记录详情）
			销售状态：未上架/已上架
			操作:【编辑】
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

	Given gddj登录商品管理系统
	#添加商品规格
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
	#添加商品
		When gddj添加商品
			"""
			{
				"product_category":"食品-饼干",
				"name":"无规格商品1",
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
				"product_category":"食品-饼干",
				"name":"多规格商品2",
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
				"product_category":"服装-男装",
				"name":"多规格商品3",
				"promotion_title":"促销标题3",
				"is_enable_model":true,
				"model": {
					"models": {
						"黑色": {
							"purchase_price": 30.00,
							"weight":1.0,
							"stocks":300
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
			"products":["无规格商品1"],
			"platforms":["自营平台1"]
		}
		"""
	When yunying批量驳回修改商品
		"""
		{
			"products":["多规格商品2"],
			"reasons":"商品描述不合格"
		}
		"""

Scenario:1 固定底价客户商品列表-默认查询
	Given gddj登录商品管理系统
	When gddj设置商品列表查询条件
		"""
		{
			"product_name":"",
			"product_category":"",
			"storage_status":"全部"
		}
		"""
	Then gddj获得商品列表
		"""
		[{
			"product_info":
				{
					"name":"多规格商品3",
					"image":"love.png"
				},
			"product_category":"服装-男装",
			"price":"30.00",
			"purchase_price":"30.00",
			"sales":0,
			"stocks":"300",
			"create_time":"2016-10-18 10:00",
			"storage_status":"待入库",
			"sale_status":"未上架",
			"actions":["编辑"]
		},{
				"product_info":
				{
					"name":"多规格商品2",
					"image":"love.png"
				},
			"product_category":"食品-饼干",
			"price":"10.00-20.00",
			"purchase_price":"10.00~20.00",
			"sales":0,
			"stocks":"100~200",
			"create_time":"2016-10-18 09:00",
			"storage_status":"已驳回",
			"sale_status":"未上架",
			"actions":["编辑"]
		},{
				"product_info":
				{
					"name":"无规格商品1",
					"image":"love.png"
				},
			"product_category":"食品-饼干",
			"price":"10.00",
			"purchase_price":"10.00",
			"sales":0,
			"stocks":"100",
			"create_time":"2016-10-18 08:00",
			"storage_status":"已入库",
			"sale_status":"未上架",
			"actions":["编辑"]
		}]
		"""

Scenario:2 固定底价客户商品列表-商品名称查询
	Given gddj登录商品管理系统
	#模糊查询
	When gddj设置商品列表查询条件
		"""
		{
			"product_name":"多规格"
		}
		"""
	Then gddj获得商品列表
		"""
		[{
			"product_info":{"name":"多规格商品3"}
		},{
			"product_info":{"name":"多规格商品2"}
		}]
		"""
	#精确查询
	When gddj设置商品列表查询条件
		"""
		{
			"product_name":"无规格商品1"
		}
		"""
	Then gddj获得商品列表
		"""
		[{
			"product_info":{"name":"无规格商品1"}
		}]
		"""
	#查询结果为空
	When gddj设置商品列表查询条件
		"""
		{
			"product_name":"哈哈"
		}
		"""
	Then gddj获得商品列表
		"""
		[]
		"""

Scenario:3 固定底价客户商品列表-入库状态查询
	Given gddj登录商品管理系统
	#待入库
	When gddj设置商品列表查询条件
		"""
		{
			"storage_status":"待入库"
		}
		"""
	Then gddj获得商品列表
		"""
		[{
			"product_info":{"name":"多规格商品3"},
			"storage_status":"待入库"
		}]
		"""
	#已驳回
	When gddj设置商品列表查询条件
		"""
		{
			"storage_status":"已驳回"
		}
		"""
	Then gddj获得商品列表
		"""
		[{
			"product_info":{"name":"多规格商品2"},
			"storage_status":"已驳回"
		}]
		"""
	#已入库
	When gddj设置商品列表查询条件
		"""
		{
			"storage_status":"已入库"
		}
		"""
	Then gddj获得商品列表
		"""
		[{
			"product_info":{"name":"无规格商品1"},
			"storage_status":"已入库"
		}]
		"""

Scenario:4 固定底价客户商品列表-商品分类查询
	Given gddj登录商品管理系统
	#一级分类模糊查询
		When gddj设置商品列表查询条件
			"""
			{
				"product_category":"食"
			}
			"""
		Then gddj获得商品列表
			"""
			[{
				"product_info":{"name":"多规格商品2"},
				"product_category":"食品-饼干"
			},{
				"product_info":{"name":"无规格商品1"},
				"product_category":"食品-饼干"
			}]
			"""
	#一级分类精确查询
		When gddj设置商品列表查询条件
			"""
			{
				"product_category":"服装"
			}
			"""
		Then gddj获得商品列表
			"""
			[{
				"product_info":{"name":"多规格商品3"},
				"product_category":"服装-男装"
			}]
			"""
	#二级分类模糊查询
		When gddj设置商品列表查询条件
			"""
			{
				"product_category":"饼"
			}
			"""
		Then gddj获得商品列表
			"""
			[{
				"product_info":{"name":"多规格商品2"},
				"product_category":"食品-饼干"
			},{
				"product_info":{"name":"无规格商品1"},
				"product_category":"食品-饼干"
			}]
			"""
	#二级分类精确查询
		When gddj设置商品列表查询条件
			"""
			{
				"product_category":"男装"
			}
			"""
		Then gddj获得商品列表
			"""
			[{
				"product_info":{"name":"多规格商品3"},
				"product_category":"服装-男装"
			}]
			"""
	#查询结果为空
		When gddj设置商品列表查询条件
			"""
			{
				"product_category":"品牌"
			}
			"""
		Then gddj获得商品列表
			"""
			[]
			"""

Scenario:5 固定底价客户商品列表-组合查询
	Given gddj登录商品管理系统
	#查询结果非空
		When gddj设置商品列表查询条件
			"""
			{
				"product_name":"无规格",
				"product_category":"食品",
				"storage_status":"全部"
			}
			"""
		Then gddj获得商品列表
			"""
			[{
				"product_info":
					{
						"name":"无规格商品1",
						"image":"love.png"
					},
				"product_category":"食品-饼干",
				"storage_status":"已入库"
			}]
			"""
	#查询结果为空
		When gddj设置商品列表查询条件
			"""
			{
				"product_name":"无规格",
				"product_category":"服装",
				"storage_status":"全部"
			}
			"""
		Then gddj获得商品列表
			"""
			[]
			"""