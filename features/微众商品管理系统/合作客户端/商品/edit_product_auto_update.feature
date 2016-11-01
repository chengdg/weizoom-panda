#_author_:张三香 2016.10.25

Feature:客户端编辑商品
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
	#gdgj添加运费模板
		When ggdj添加运费模板
			"""
			{
				"name":"运费模板1",
				"first_weight":1.0,
				"first_weight_price": 1.00,
				"added_weight":1.0,
				"added_weight_price": 1.00
			}
			"""
		When ggdj添加运费模板
			"""
			{
				"name": "运费模板2",
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
	#gddj添加禁售仅售模板
		When gddj添加禁售仅售模板
			"""
			{
				"name": "禁售仅售模板1",
				"limit_area":
					[{
						"province": "河北省",
						"is_select_all":false,
						"city":["秦皇岛市","唐山市","沧州市"]
					},{
						"province": "山西省",
						"is_select_all":true
					}]
			}
			"""
		When gddj添加禁售仅售模板
			"""
			{
				"name": "禁售仅售模板2",
				"limit_area":
					[{
						"province": "河北省",
						"is_select_all":true
					},{
						"province": "北京市",
						"is_select_all":true
					}]
			}
			"""
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

Scenario:1 客户修改未同步（待入库）的商品
	Given gddj登录商品管理系统
	When gddj编辑商品'商品1'
		"""
		{
			"product_category":"食品-泡面",
			"name":"商品1修改",
			"promotion_title":"促销标题1修改",
			"is_enable_model":false,
			"purchase_price": 11.00,
			"weight":1.1,
			"stocks":100,
			"limit_zone_type":"无限制",
			"postage":1.10,
			"image":["love.png"],
			"detail": "商品1描述信息修改"
		}
		"""
	Then gddj获得商品'商品1修改'
		"""
		{
			"product_category":"食品-泡面",
			"name":"商品1修改",
			"promotion_title":"促销标题1修改",
			"is_enable_model":false,
			"purchase_price": 11.00,
			"weight":1.1,
			"stocks":100,
			"limit_zone_type":"无限制",
			"postage":1.10,
			"image":["love.png"],
			"detail": "商品1描述信息修改"
		}
		"""
	#运营端校验-商品更新列表
	Given yunying登录商品管理系统
	Then yunying获得商品更新列表
		"""
		[]
		"""
	#运营端校验-商品列表及商品详情页
	Then yunying获得商品列表
		"""
		[{
			"name":"商品2",
			"shop_name":"固定底价店铺",
			"product_category":"食品-饼干",
			"customer_from":"--",
			"total_sales":0,
			"storage_status":"待入库",
			"product_label":[],
			"actions":["同步商品","驳回修改","删除商品"]
		},{
			"name":"商品1修改",
			"shop_name":"固定底价店铺",
			"product_category":"食品-泡面",
			"customer_from":"--",
			"total_sales":0,
			"storage_status":"待入库",
			"product_label":[],
			"actions":["同步商品","驳回修改","删除商品"]
		}]
		"""
	Then yunying获得商品'商品1修改'
		"""
		{
			"product_category":"食品-泡面",
			"name":"商品1修改",
			"promotion_title":"促销标题1修改",
			"is_enable_model":false,
			"purchase_price": 11.00,
			"weight":1.1,
			"stocks":100,
			"limit_zone_type":"无限制",
			"postage":1.10,
			"image":["love.png"],
			"detail": "商品1描述信息修改"
		}
		"""

Scenario:2 客户端编辑未同步（入库驳回）的商品
	Given yunying登录商品管理系统
	When yunying在'商品'列表批量驳回修改商品
		"""
		{
			"name":["商品1"],
			"reject_reason":"驳回修改原因"
		}
		"""
	#编辑入库驳回状态商品点击详情页的【保存】，只保存修改信息不更改商品状态
	Given gddj登录商品管理系统
	When gddj编辑商品'商品1'
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品1修改",
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
	Then gddj获得商品列表
		"""
		[{
			"product_info":{"name":"商品2"},
			"storage_status":"待入库",
			"sale_status":"未上架"
		},{
			"product_info":{"name":"商品1修改"},
			"storage_status":"入库驳回",
			"sale_status":"未上架"
		}]
		"""
	Given yunying登录商品管理系统
	Then yunying获得商品列表
		"""
		[{
			"name":"商品2",
			"storage_status":"待入库"
		},{
			"name":"商品1修改",
			"storage_status":"入库驳回"
		}]
		"""
	#编辑入库驳回状态商品点击详情页的【重新修改提交】，商品状态由'入库驳回'变为'待入库'
	Given gddj登录商品管理系统
	When gddj重新修改提交商品'商品1修改'
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品1修改",
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
	Then gddj获得商品列表
		"""
		[{
			"product_info":{"name":"商品2"},
			"storage_status":"待入库",
			"sale_status":"未上架"
		},{
			"product_info":{"name":"商品1修改"},
			"storage_status":"待入库",
			"sale_status":"未上架"
		}]
		"""
	Given yunying登录商品管理系统
	Then yunying获得商品列表
		"""
		[{
			"name":"商品2",
			"storage_status":"待入库"
		},{
			"name":"商品1修改",
			"storage_status":"待入库"
		}]
		"""

Scenario:3 客户端编辑已同步的商品（修改信息自动更新）
	Given 添加自营平台账号
		"""
		[{
			"account":"zy1",
			"self_shop_name":"自营平台1"
		}]
		"""
	Given yunying登录商品管理系统
	When yunying同步商品到自营平台
		"""
		{
			"products":["商品1","商品2"],
			"platforms":["自营平台1"]
		}
		"""
	Given zy1登录系统
	When zy1批量上架商品池商品
		"""
		["商品1"]
		"""
	Given gddj登录商品管理系统
	#客户修改已入库/已上架的商品（修改除价格以外的商品信息）
	When 编辑商品'商品1'
		"""
		{
			"product_category":"食品-泡面",
			"name":"商品1修改",
			"promotion_title":"促销标题1修改",
			"is_enable_model":false,
			"purchase_price": 10.00,
			"weight":1.1,
			"stocks":110,
			"limit_zone_type":"仅发货地区",
			"limit_zone_template":"禁售仅售模板1",
			"postage":2.00,
			"image":["aa.png"],
			"detail": "商品1描述信息修改"
		}
		"""
	#客户修改已入库/未上架的商品（修改除价格以外的商品信息）
	When 编辑商品'商品2'
		"""
		{
			"product_category":"食品-泡面",
			"name":"商品2修改",
			"promotion_title":"促销标题2修改",
			"is_enable_model":true,
			"model": {
				"models": {
					"黑色 S": {
						"purchase_price": 21.00,
						"weight":1.1,
						"stocks":110
					},
					"白色 S": {
						"purchase_price": 22.00,
						"weight": 2.2,
						"stocks":220
					}
				}
			},
			"limit_zone_type":"不发货地区",
			"limit_zone_template":"禁售仅售模板2",
			"postage":"运费模板2",
			"image":["aa2.png"],
			"detail": "商品2描述信息修改"
		}
		"""
	Then gddj获得商品列表
		"""
		[{
			"product_info":
				{
					"name":"商品2修改",
					"image":"aa2.png"
				},
			"product_category":"食品-泡面",
			"price":"21.00~22.00",
			"purchase_price":"21.00~22.00",
			"sales":0,
			"stocks":"110~220",
			"create_time":"2016-10-18 08:00",
			"storage_status":"已入库",
			"sale_status":"未上架",
			"actions":["编辑"]
		},{
			"product_info":
				{
					"name":"商品1修改",
					"image":"aa.png"
				},
			"product_category":"食品-泡面",
			"price":"10.00",
			"purchase_price":"10.00",
			"sales":0,
			"stocks":"110",
			"create_time":"2016-10-18 08:00",
			"storage_status":"已入库",
			"sale_status":"已上架",
			"actions":["编辑"]
		}]
		"""
	Given yunying登录商品管理系统
	#运营端'商品更新'列表校验
	Then yunying获得商品更新列表
		"""
		[]
		"""
	#运营端'商品'列表校验
	Then yunying获得商品列表
		"""
		[{
			"name":"商品2修改",
			"product_category":"食品-泡面",
			"storage_status":"已入库,已同步"
		},{
			"name":"商品1修改",
			"product_category":"食品-泡面",
			"storage_status":"已入库,已同步"
		}]
		"""
	Then yunying获得商品'商品2修改'
		"""
		{
			"product_category":"食品-泡面",
			"name":"商品2修改",
			"promotion_title":"促销标题2修改",
			"is_enable_model":true,
			"model": {
				"models": {
					"黑色 S": {
						"purchase_price": 21.00,
						"weight":1.1,
						"stocks":110
					},
					"白色 S": {
						"purchase_price": 22.00,
						"weight": 2.2,
						"stocks":220
					}
				}
			},
			"limit_zone_type":"不发货地区",
			"limit_zone_template":"禁售仅售模板2",
			"postage":"运费模板2",
			"image":["aa2.png"],
			"detail": "商品2描述信息修改"
		}
		"""
	Then yunying获得商品'商品1修改'
		"""
		{
			"product_category":"食品-泡面",
			"name":"商品1修改",
			"promotion_title":"促销标题1修改",
			"is_enable_model":false,
			"purchase_price": 10.00,
			"weight":1.1,
			"stocks":110,
			"limit_zone_type":"仅发货地区",
			"limit_zone_template":"禁售仅售模板1",
			"postage":2.00,
			"image":["aa.png"],
			"detail": "商品1描述信息修改"
		}
		"""
	#weapp端商品的校验
	Given zy1登录系统
	Then zy1获得商品池所有商品列表
		"""
		[{
			"product_info":
				{
					"name": "商品2修改",
					"user_code":""
				},
			"product_category":"食品-泡面",
			"supplier":"固定底价店铺",
			"price":"21.00~22.00",
			"stock": "110~220",
			"product_return":"0.00",
			"purchase_way":"固定底价",
			"is_generalize_product":false,
			"product_label":[]
		}]
		"""
	Then zy1能获得'在售'商品列表
		"""
		[{
			"product_info":
				{
					"name": "商品1修改",
					"user_code":""
				},
			"is_enable_model":false,
			"is_generalize_product":false,
			"supplier":"固定底价店铺",
			"price":"10.00",
			"stock":"110",
			"product_category":"食品-泡面"
		}]
		"""


