#_author_:张三香 2016.10.27

Feature:客户端查看订单列表
	"""
		1.客户端订单列表中显示从自营平台购买该客户商品的支付完成的所有订单（待支付的订单不会显示）
		2.客户端订单列表包含以下字段信息:
			订单编号:显示订单编号
			商品:显示商品名称和商品图片
			单价/数量:
				固定底价客户-显示商品的结算价/商品数量
				零售价返点客户-限时商品的售价/商品数量
			收货人:显示收货人名称
			订单金额:单价（结算价/售价）*数量,保留两位小数
			运费:显示运费,保留两位小数
			订单状态:显示订单的状态
			下单时间:显示下单时间，格式为xxxx-xx-xx xx:xx:xx
			操作（panda客户端不允许进行【取消订单】和【申请退款】操作）:
				待发货:【发货】
				已发货:【标记完成】【修改物流】
				已完成:无任何操作按钮
				退款中:无任何操作按钮
				退款完成:无任何操作按钮
				已取消:无任何操作按钮
		3.订单列表排序:下单时间倒序显示（每页显示10条数据）
		4.订单列表查询条件
			订单编号:精确查询
			商品名称:支持部分查询
			订单状态:下拉框形式显示，默认显示全部，下拉框中包含全部、待发货、已发货、已完成、退款中、退款完成、已取消
			下单时间:必须输入开始时间和结束时间（目前没有控制开始时间小于结束时间这种情况，只是查询时结果为空）
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
	#固定底价客户添加商品
		Given gddj登录商品管理系统
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
				"detail": "商品1描述信息"
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
				"postage":"运费模板1",
				"image":["love.png"],
				"detail": "商品2描述信息"
			}
			"""
	#零售价返点客户添加商品
		Given lsjfd登录商品管理系统
		When lsjfd添加运费模板
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
				"detail": "商品1描述信息"
			}
			"""
		When lsjfd添加商品
			"""
			{
				"product_category":"食品-泡面",
				"name":"零售商品2",
				"promotion_title":"促销标题2",
				"is_enable_model":true,
				"model": {
					"models": {
						"黑色": {
							"price":21.00,
							"weight":1.0,
							"stocks":100
						},
						"白色": {
							"price": 22.00,
							"weight":2.0,
							"stocks":200
						}
					}
				},
				"limit_zone_type":"无限制",
				"postage":"运费模板1",
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
			"products":["固定商品1","固定商品2"],
			"platforms":["自营平台1","自营平台2"]
		}
		"""
	When yunying同步商品到自营平台
		"""
		{
			"products":["零售商品1","零售商品2"],
			"platforms":["自营平台1"]
		}
		"""
	Given zy1登录系统
	When zy1添加支付方式
		"""
		{
			"type": "微信支付",
			"is_active": "启用"
		}
		"""
	When zy1批量上架商品池商品
		"""
		["固定商品1","固定商品1","零售商品1","零售商品2"]
		"""
	Given zy2登录系统
	When zy2添加支付方式
		"""
		{
			"type": "微信支付",
			"is_active": "启用"
		}
		"""
	When zy2批量上架商品池商品
		"""
		["固定商品1","固定商品1"]
		"""

	Given bill关注zy1的公众号
	Given bill关注zy2的公众号
	#订单数据
		#101（zy1）-待支付-固定商品1,1
			When bill访问zy1的webapp::apiserver
			When bill购买zy1的商品::apiserver
			"""
			{
				"order_id":"101",
				"date":"2016-10-11",
				"ship_name": "bill",
				"ship_tel": "13811223344",
				"ship_area": "北京市 北京市 海淀区",
				"ship_address": "泰兴大厦",
				"pay_type": "微信支付",
				"products":[{
					"name":"固定商品1",
					"price":10.00,
					"count":1
				}],
				"postage": 1.00,
				"customer_message": "bill的订单备注1"
			}
			"""
		#102（zy1）-待发货-固定商品1,2
			When bill购买zy1的商品::apiserver
				"""
				{
					"order_id":"102",
					"date":"2016-10-12",
					"ship_name": "bill2",
					"ship_tel": "13811223344",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "泰兴大厦",
					"pay_type": "微信支付",
					"products":[{
						"name":"固定商品1",
						"price":10.00,
						"count":2
					}],
					"postage":1.00,
					"customer_message": "bill的订单备注2"
				}
				"""
			And bill使用支付方式'微信支付'进行支付::apiserver
		#103（zy1）-待发货-固定商品1,1+固定商品2,2
			When bill购买zy1的商品::apiserver
				"""
				{
					"order_id":"103",
					"date":"2016-10-13",
					"ship_name": "bill3",
					"ship_tel": "13811223344",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "泰兴大厦",
					"pay_type": "微信支付",
					"products":[{
						"name":"固定商品1",
						"price":10.00,
						"count":1
					},{
						"name":"固定商品2",
						"model":"黑色 S",
						"price":21.00,
						"count":1
					},{
						"name":"固定商品2",
						"model":"白色 S"
						"price":22.00,
						"count":1
					}],
					"postage":4.00,
					"customer_message": "bill的订单备注3"
				}
				"""
			And bill使用支付方式'微信支付'进行支付::apiserver
		#104（zy1）-待发货-固定商品1,1+零售商品1,1
			When bill购买zy1的商品::apiserver
				"""
				{
					"order_id":"104",
					"date":"2016-10-14",
					"ship_name": "bill4",
					"ship_tel": "13811223344",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "泰兴大厦",
					"pay_type": "微信支付",
					"products":[{
						"name":"固定商品1",
						"price":10.00,
						"count":1
					},{
						"name":"零售商品1",
						"price":10.00,
						"count":1
					}],
					"postage":2.00,
					"customer_message": "bill的订单备注4"
				}
				"""
			And bill使用支付方式'微信支付'进行支付::apiserver
		#105（zy1）-待发货-零售商品1,1+零售商品2,2
			When bill购买zy1的商品::apiserver
				"""
				{
					"order_id":"105",
					"date":"2016-10-15",
					"ship_name": "bill5",
					"ship_tel": "13811223344",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "泰兴大厦",
					"pay_type": "微信支付",
					"products":[{
						"name":"零售商品1",
						"price":10.00,
						"count":1
					},{
						"name":"零售商品2",
						"model":"黑色",
						"price":21.00,
						"count":1
					},{
						"name":"零售商品2",
						"model":"白色",
						"price":22.00,
						"count":1
					}],
					"postage":7.00,
					"customer_message": "bill的订单备注4"
				}
				"""
			And bill使用支付方式'微信支付'进行支付::apiserver
		#201（zy2）-待发货-固定商品1,2+固定商品2,2
			When bill访问zy2的webapp::apiserver
			When bill购买zy2的商品::apiserver
				"""
				{
					"order_id":"201",
					"date":"2016-10-16",
					"ship_name": "bill6",
					"ship_tel": "13811223344",
					"ship_area": "北京市 北京市 海淀区",
					"ship_address": "泰兴大厦",
					"pay_type": "微信支付",
					"products":[{
						"name":"固定商品1",
						"price":10.00,
						"count":2
					},{
						"name":"固定商品2",
						"model":"黑色 S",
						"price":21.00,
						"count":1
					},{
						"name":"固定商品2",
						"model":"白色 S",
						"price":22.00,
						"count":1
					}],
					"postage":7.00,
					"customer_message":"bill的订单备注6"
				}
				"""
			And bill使用支付方式'微信支付'进行支付::apiserver

Scenario:1 固定底价客户查看订单列表（运营不修改商品售价即售价和结算价相等）
	Given gddj登录商品管理系统
	Then gddj获得订单列表
		"""
		[{
			"order_id":"201-固定底价店铺",
			"products":
				[{
					"name":"固定商品1",
					"price":10.00,
					"count":2
				},{
					"name":"固定商品2",
					"model":"黑色 S",
					"price":21.00,
					"count":1
				},{
					"name":"固定商品2",
					"model":"白色 S",
					"price":22.00,
					"count":1
				}],
			"ship_name": "bill6",
			"order_money":63.00,
			"postage":7.00,
			"order_status":"待发货",
			"order_time":"2016-10-16 00:00:00",
			"actions":["发货"]
		},{
			"order_id":"104-固定底价店铺",
			"products":
				[{
					"name":"固定商品1",
					"price":10.00,
					"count":1
				}],
			"ship_name": "bill4",
			"order_money":10.00,
			"postage":1.00,
			"order_status":"待发货",
			"order_time":"2016-10-14 00:00:00",
			"actions":["发货"]
		},{
			"order_id":"103-固定底价店铺",
			"products":
				[{
					"name":"固定商品1",
					"price":10.00,
					"count":1
				},{
					"name":"固定商品2",
					"model":"黑色 S",
					"price":21.00,
					"count":1
				},{
					"name":"固定商品2",
					"model":"白色 S"
					"price":22.00,
					"count":1
				}],
			"ship_name": "bill3",
			"order_money":53.00,
			"postage":4.00,
			"order_status":"待发货",
			"order_time":"2016-10-13 00:00:00",
			"actions":["发货"]
		},{
			"order_id":"102-固定底价店铺",
			"products":
				[{
					"name":"固定商品1",
					"price":10.00,
					"count":2
				}],
			"ship_name": "bill2",
			"order_money":20.00,
			"postage":1.00,
			"order_status":"待发货",
			"order_time":"2016-10-12 00:00:00",
			"actions":["发货"]
		}]
		"""

Scenario:2 固定底价客户查看订单列表（运营修改商品售价即售价不等于结算价）
	Given yunying登录商品管理系统
	When yunying修改商品'固定商品1'的售价为
		"""
		{
			"price":10.99
		}
		"""
	When bill访问zy1的webapp::apiserver
	When bill购买zy1的商品::apiserver
		"""
		{
			"order_id":"106",
			"date":"2016-10-17",
			"ship_name": "bill7",
			"ship_tel": "13811223344",
			"ship_area": "北京市 北京市 海淀区",
			"ship_address": "泰兴大厦",
			"pay_type": "微信支付",
			"products":[{
				"name":"固定商品1",
				"price":10.99,
				"count":1
			}],
			"postage":1.00,
			"customer_message": "bill的订单备注7"
		}
		"""
	And bill使用支付方式'微信支付'进行支付::apiserver
	#运营修改商品售价后，客户端订单列表的单价显示的仍是结算价
	Given gddj登录商品管理系统
	Then gddj获得订单列表
		"""
		[{
			"order_id":"106-固定底价店铺",
			"products":
				[{
					"name":"固定商品1",
					"price":10.00,
					"count":1
				}],
			"ship_name": "bill7",
			"order_money":10.00,
			"postage":1.00,
			"order_status":"待发货",
			"order_time":"2016-10-17 00:00:00",
			"actions":["发货"]
		},{
			"order_id":"201-固定底价店铺",
			"products":
				[{
					"name":"固定商品1",
					"price":10.00,
					"count":2
				},{
					"name":"固定商品2",
					"model":"黑色 S",
					"price":21.00,
					"count":1
				},{
					"name":"固定商品2",
					"model":"白色 S",
					"price":22.00,
					"count":1
				}],
			"ship_name": "bill6",
			"order_money":63.00,
			"postage":7.00,
			"order_status":"待发货",
			"order_time":"2016-10-16 00:00:00",
			"actions":["发货"]
		},{
			"order_id":"104-固定底价店铺",
			"products":
				[{
					"name":"固定商品1",
					"price":10.00,
					"count":1
				}],
			"ship_name": "bill4",
			"order_money":10.00,
			"postage":1.00,
			"order_status":"待发货",
			"order_time":"2016-10-14 00:00:00",
			"actions":["发货"]
		},{
			"order_id":"103-固定底价店铺",
			"products":
				[{
					"name":"固定商品1",
					"price":10.00,
					"count":1
				},{
					"name":"固定商品2",
					"model":"黑色 S",
					"price":21.00,
					"count":1
				},{
					"name":"固定商品2",
					"model":"白色 S"
					"price":22.00,
					"count":1
				}],
			"ship_name": "bill3",
			"order_money":53.00,
			"postage":4.00,
			"order_status":"待发货",
			"order_time":"2016-10-13 00:00:00",
			"actions":["发货"]
		},{
			"order_id":"102-固定底价店铺",
			"products":
				[{
					"name":"固定商品1",
					"price":10.00,
					"count":2
				}],
			"ship_name": "bill2",
			"order_money":20.00,
			"postage":1.00,
			"order_status":"待发货",
			"order_time":"2016-10-12 00:00:00",
			"actions":["发货"]
		}]
		"""

Scenario:3 零售价返点客户查看订单列表
	Given lsjfd登录商品管理系统
	Then lsjfd获得订单列表
		"""
		[{
			"order_id":"105-零售价返点店铺",
			"products":
				[{
					"name":"零售商品1",
					"price":10.00,
					"count":1
				},{
					"name":"零售商品2",
					"model":"黑色",
					"price":21.00,
					"count":1
				},{
					"name":"零售商品2",
					"model":"白色",
					"price":22.00,
					"count":1
				}],
			"ship_name": "bill5",
			"order_money":53.00,
			"postage":7.00,
			"order_status":"待发货",
			"order_time":"2016-10-15 00:00:00",
			"actions":["发货"]
		},{
			"order_id":"104-零售价返点店铺",
			"products":
				[{
					"name":"零售商品1",
					"price":10.00,
					"count":1
				}],
			"ship_name": "bill4",
			"order_money":10.00,
			"postage":1.00,
			"order_status":"待发货",
			"order_time":"2016-10-14 00:00:00",
			"actions":["发货"]
		}]
		"""
