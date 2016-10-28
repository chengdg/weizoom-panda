#_author_:张三香 2016.10.19

Feature:运营端'同步商品'到自营平台
	"""
		1.商品列表中展示所有客户创建的商品
		2.商品列表显示顺序：商品创建时间的倒序
		3.商品列表字段信息:
			商品名称：链接形式显示，点其跳转到商品预览界面
			客户名称：显示创建客户时填写的店铺名称
			分类：商品的分类
			来源：显示客户的来源，无则显示"--"
			总销量：显示该商品的总销量
			入库状态：待入库/已入库，已同步/已入库，已停售/入库驳回/修改驳回
			操作：不同状态对应的操作不同
				待入库:【同步商品】【驳回修改】【删除商品】
				已入库,已同步:【同步商品】
				已入库,已停售:【同步商品】【删除商品】
				入库驳回:【删除商品】
				修改驳回:【同步商品】
		4.商品状态由'待入库'变为'入库驳回'
			a.对'待入库'商品点击【驳回修改】，显示'商品驳回'弹框
			b.弹框中显示一个可直接勾选的驳回原因'商品名称不规格，标准格式:品牌名+商品名+包装规格'和自定义输入框，下方显示【确定】、【取消】
			c.选择或填写驳回原因后，弹框关闭，商品状态由'待入库'变为'入库驳回'
		5.商品状态由'已入库,已同步'变为'已入库,已停售'
			a.将'已入库,已同步'状态的商品的自营平台全部取消时，会显示'全部停售'弹窗
			b.'全部停售'弹窗中显示3个定义好的原因（已过季/供应商停止合作/315黑名单商品）和自定义输入框（输入框显示'自定义,10字以内'）
			c.选择停售原因或填写自定义原因后，商品状态变为'已入库,已同步'变为'已入库,已停售'
		6.商品列表上方显示按钮：【批量同步】【导出商品】【批量驳回】
		7.每条商品下方显示该商品的标签信息，若无则只显示按钮【配置标签】
		8.商品同步后会进入自营平台的商品池中
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

Scenario:1 运营对'待入库'商品进行【同步商品】操作
	Given yunying登录商品管理系统
	Then yunying获得商品列表
		"""
		[{
			"name":"零售商品2",
			"shop_name":"零售价返点店铺",
			"product_category":"服装-男装",
			"customer_from":"--",
			"total_sales":0,
			"storage_status":"待入库",
			"product_label":[],
			"actions":["同步商品","驳回修改","删除商品"]
		},{
			"name":"零售商品1",
			"shop_name":"零售价返点店铺",
			"product_category":"食品-饼干",
			"customer_from":"--",
			"total_sales":0,
			"storage_status":"待入库",
			"product_label":[],
			"actions":["同步商品","驳回修改","删除商品"]
		},{
			"name":"固定商品2",
			"shop_name":"固定底价店铺",
			"product_category":"食品-泡面",
			"customer_from":"--",
			"total_sales":0,
			"storage_status":"待入库",
			"product_label":[],
			"actions":["同步商品","驳回修改","删除商品"]
		},{
			"name":"固定商品1",
			"shop_name":"固定底价店铺",
			"product_category":"食品-饼干",
			"customer_from":"--",
			"total_sales":0,
			"storage_status":"待入库",
			"product_label":[],
			"actions":["同步商品","驳回修改","删除商品"]
		}]
		"""
	#同步单个商品（待入库-已入库，已同步）
		When yunying同步商品到自营平台
			"""
			{
				"products":["固定商品1"],
				"platforms":["自营平台1","自营平台2"]
			}
			"""
	#批量同步多个商品（待入库-已入库，已同步）
		When yunying同步商品到自营平台
			"""
			{
				"products":["固定商品2","零售商品1"],
				"platforms":["自营平台1"]
			}
			"""
	#同步商品后校验yunying商品列表中状态和操作列的变化
	Then yunying获得商品列表
		"""
		[{
			"name":"零售商品2",
			"storage_status":"待入库",
			"actions":["同步商品","驳回修改","删除商品"]
		},{
			"name":"零售商品1",
			"storage_status":"已入库,已同步",
			"actions":["同步商品"]
		},{
			"name":"固定商品2",
			"storage_status":"已入库,已同步",
			"actions":["同步商品"]
		},{
			"name":"固定商品1",
			"storage_status":"已入库,已同步",
			"actions":["同步商品"]
		}]
		"""
	#同步商品后校验客户端商品列表的变化
	Given gddj登录商品管理系统
	Then gddj获得商品列表
		"""
		[{
			"product_info":{"name":"固定商品2"},
			"storage_status":"已入库",
			"sale_status":"未上架"
		},{
			"product_info":{"name":"固定商品1"},
			"storage_status":"已入库",
			"sale_status":"未上架"
		}]
		"""
	Given lsjfd登录商品管理系统
	Then lsjfd获得商品列表
		"""
		[{
			"product_info":{"name":"零售商品2"},
			"storage_status":"待入库",
			"sale_status":"未上架"
		},{
			"product_info":{"name":"零售商品1"},
			"storage_status":"已入库",
			"sale_status":"未上架"
		}]
		"""
	#同步商品后校验自营平台商品池的变化
	Given zy1登录系统
	Then zy1获得商品池所有商品列表
		"""
		[{
			"product_info":{"name": "固定商品1"},
			"supplier":"固定底价店铺"
		},{
			"product_info":{"name": "零售商品1"},
			"supplier":"零售价返点店铺"
		},{
			"product_info":{"name": "固定商品2"},
			"supplier":"固定底价店铺"
		}]
		"""
	Given zy2登录系统
	Then zy2获得商品池所有商品列表
		"""
		[{
			"product_info":{"name": "固定商品1"},
			"supplier":"固定底价店铺"
		}]
		"""

Scenario:2 运营对'已入库,已同步'商品进行【同步商品】操作
	1.'固定商品1'-待入库
	2.'固定商品1'同步到'自营平台1'-已入库，已同步
	3.再将'固定商品1'同步到'自营平台2'-已入库,已同步

	Given yunying登录商品管理系统
	When yunying同步商品到自营平台
		"""
		{
			"products":["固定商品1"],
			"platforms":["自营平台1"]
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"零售商品2",
			"storage_status":"待入库",
			"actions":["同步商品","驳回修改","删除商品"]
		},{
			"name":"零售商品1",
			"storage_status":"待入库",
			"actions":["同步商品","驳回修改","删除商品"]
		},{
			"name":"固定商品2",
			"storage_status":"待入库",
			"actions":["同步商品","驳回修改","删除商品"]
		},{
			"name":"固定商品1",
			"storage_status":"已入库,已同步",
			"actions":["同步商品"]
		}]
		"""
	#对'已入库，已同步'商品进行【同步商品】
	When yunying同步商品到自营平台
		"""
		{
			"products":["固定商品1"],
			"platforms":["自营平台1","自营平台2"]
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"零售商品2",
			"storage_status":"待入库",
			"actions":["同步商品","驳回修改","删除商品"]
		},{
			"name":"零售商品1",
			"storage_status":"待入库",
			"actions":["同步商品","驳回修改","删除商品"]
		},{
			"name":"固定商品2",
			"storage_status":"待入库",
			"actions":["同步商品","驳回修改","删除商品"]
		},{
			"name":"固定商品1",
			"storage_status":"已入库,已同步",
			"actions":["同步商品"]
		}]
		"""

	Given zy1登录系统
	Then zy1获得商品池所有商品列表
		"""
		[{
			"product_info":{"name": "固定商品1"},
			"supplier":"固定底价店铺"
		}]
		"""
	Given zy2登录系统
	Then zy2获得商品池所有商品列表
		"""
		[{
			"product_info":{"name": "固定商品1"},
			"supplier":"固定底价店铺"
		}]
		"""

Scenario:3 运营对'已入库,已停售'商品进行【同步商品】操作
	1.'固定商品1'-待入库
	2.'固定商品1'同步到'自营平台1'-已入库，已同步
	3.'固定商品1'再同步到'自营平台2'-已入库，已同步
	4.将'固定商品1'取消同步'自营平台1'-已入库，已同步
	5.将'固定商品1'取消同步'自营平台2'-会显示'全部停售'弹窗，标记或填写停售原因后状态变为'已入库，已停售'

	Given yunying登录商品管理系统
	#将'固定商品1'同步到'自营平台1'
	When yunying同步商品到自营平台
		"""
		{
			"products":["固定商品1"],
			"platforms":["自营平台1"]
		}
		"""
	#再将'固定商品1'同步到'自营平台2'
	When yunying同步商品到自营平台
		"""
		{
			"products":["固定商品1"],
			"platforms":["自营平台1","自营平台2"]
		}
		"""
	#将'固定商品1'取消同步到'自营平台1'
	When yunying同步商品到自营平台
		"""
		{
			"products":["固定商品1"],
			"platforms":["自营平台2"]
		}
		"""
	#再将'固定商品1'同步到'自营平台2'-会显示全部停售弹窗
	When yunying同步商品到自营平台
		"""
		{
			"products":["固定商品1"],
			"platforms":[],
			"not_sale_reason":"已过季"
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"零售商品2",
			"storage_status":"待入库",
			"actions":["同步商品","驳回修改","删除商品"]
		},{
			"name":"零售商品1",
			"storage_status":"待入库",
			"actions":["同步商品","驳回修改","删除商品"]
		},{
			"name":"固定商品2",
			"storage_status":"待入库",
			"actions":["同步商品","驳回修改","删除商品"]
		},{
			"name":"固定商品1",
			"storage_status":"已入库,已停售",
			"not_sale_reason":"已过季",
			"actions":["同步商品","删除商品"]
		}]
		"""
	Given gddj登录商品管理系统
	Then gddj获得商品列表
		"""
		[{
			"product_info":{"name":"固定商品2"},
			"storage_status":"待入库",
			"sale_status":"未上架"
		},{
			"product_info":{"name":"固定商品1"},
			"storage_status":"待入库",
			"sale_status":"未上架"
		}]
		"""
	#对'已入库，已停售'的'固定商品1'进行【同步商品】
	When yunying同步商品到自营平台
		"""
		{
			"products":["固定商品1"],
			"platforms":["自营平台1","自营平台2"]
		}
		"""
	#校验运营商品列表商品状态的变化
	Then yunying获得商品列表
		"""
		[{
			"name":"零售商品2",
			"storage_status":"待入库",
			"actions":["同步商品","驳回修改","删除商品"]
		},{
			"name":"零售商品1",
			"storage_status":"待入库",
			"actions":["同步商品","驳回修改","删除商品"]
		},{
			"name":"固定商品2",
			"storage_status":"待入库",
			"actions":["同步商品","驳回修改","删除商品"]
		},{
			"name":"固定商品1",
			"storage_status":"已入库,已同步",
			"actions":["同步商品"]
		}]
		"""

Scenario:4 运营对'修改驳回'商品进行【同步商品】操作（暂未写,待需求确定后再完成）
	Given yunying登录商品管理系统
	When yunying同步商品到自营平台
		"""
		{
			"products":["固定商品1"],
			"platforms":["自营平台1","自营平台2"]
		}
		"""
	Given zy1登录系统
	When zy1批量上架商品池商品
		"""
		["固定商品1"]
		"""
	Given gddj登录商品管理系统
	Then gddj获得商品列表
		"""
		[{
			"product_info":{"name":"固定商品2"},
			"storage_status":"待入库",
			"sale_status":"未上架"
		},{
			"product_info":{"name":"固定商品1"},
			"storage_status":"已入库",
			"sale_status":"已上架"
		}]
		"""
	#修改商品的采购价
	When gddj编辑商品'固定商品1'
		"""
		{
			"product_category":"食品-饼干",
			"name":"固定商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":false,
			"purchase_price": 20.00,
			"weight": 1,
			"stocks": 100,
			"limit_zone_type":"无限制",
			"postage":1.00,
			"image":["love.png"],
			"detail": "商品1描述信息",
			"create_time":"2016-10-18 08:00"
		}
		"""
	Given yunying登录商品管理系统
	When yunying在'商品更新'列表驳回修改商品
		"""
		{
			"name":"固定商品1",
			"reject_reason":"驳回修改原因"
		}
		"""