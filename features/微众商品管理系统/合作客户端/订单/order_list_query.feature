#_author_:张三香 2016.10.28

Feature:客户端订单列表查询
	"""
		1.订单列表查询条件
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
				"postage":"运费模板2",
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

	Given bill关注zy1的公众号::apiserver
	Given bill关注zy2的公众号::apiserver
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

Scenario:1 客户端订单列表默认查询
	Given gddj登录商品管理系统
	When gddj设置客户端订单列表查询条件
		"""
		{
			"order_id":"",
			"product_name":"",
			"order_status":"全部",
			"order_time_start":"",
			"order_time_end":""
		}
		"""
	Then gddj获得客户端订单列表
		"""
		[{
			"order_id":"201-固定底价店铺"
		},{
			"order_id":"104-固定底价店铺"
		},{
			"order_id":"103-固定底价店铺"
		},{
			"order_id":"102-固定底价店铺"
		}]
		"""

Scenario:2 客户端订单列表按'订单编号'查询
	Given gddj登录商品管理系统
	When gddj设置客户端订单列表查询条件
		"""
		{
			"order_id":"103-固定底价店铺",
			"product_name":"",
			"order_status":"全部",
			"order_time_start":"",
			"order_time_end":""
		}
		"""
	Then gddj获得客户端订单列表
		"""
		[{
			"order_id":"103-固定底价店铺"
		}]
		"""
	#查询结果为空
	Given gddj登录商品管理系统
	When gddj设置客户端订单列表查询条件
		"""
		{
			"order_id":"111-固定底价店铺",
			"product_name":"",
			"order_status":"全部",
			"order_time_start":"",
			"order_time_end":""
		}
		"""
	Then gddj获得客户端订单列表
		"""
		[]
		"""

Scenario:3 客户端订单列表按'商品名称'查询
	Given gddj登录商品管理系统
	#模糊查询
	When gddj设置客户端订单列表查询条件
		"""
		{
			"order_id":"",
			"product_name":"商品2",
			"order_status":"全部",
			"order_time_start":"",
			"order_time_end":""
		}
		"""
	Then gddj获得客户端订单列表
		"""
		[{
			"order_id":"201-固定底价店铺",
			"products":
				[{
					"name":"固定商品1"
				},{
					"name":"固定商品2"
				},{
					"name":"固定商品2"
				}]
		},{
			"order_id":"103-固定底价店铺",
			"products":
				[{
					"name":"固定商品1"
				},{
					"name":"固定商品2"
				},{
					"name":"固定商品2"
				}]
		}]
		"""
	#精确查询
	When gddj设置客户端订单列表查询条件
		"""
		{
			"order_id":"",
			"product_name":"固定商品1",
			"order_status":"全部",
			"order_time_start":"",
			"order_time_end":""
		}
		"""
	Then gddj获得客户端订单列表
		"""
		[{
			"order_id":"201-固定底价店铺",
			"products":
				[{
					"name":"固定商品1"
				},{
					"name":"固定商品2"
				},{
					"name":"固定商品2"
				}]
		},{
			"order_id":"104-固定底价店铺",
			"products":
				[{
					"name":"固定商品1"
				}]
		},{
			"order_id":"103-固定底价店铺",
			"products":
				[{
					"name":"固定商品1"
				},{
					"name":"固定商品2"
				},{
					"name":"固定商品2"
				}]
		},{
			"order_id":"102-固定底价店铺",
			"products":
				[{
					"name":"固定商品1"
				}]
		}]
		"""
	#查询结果为空
	When gddj设置客户端订单列表查询条件
		"""
		{
			"order_id":"",
			"product_name":"哈哈",
			"order_status":"全部",
			"order_time_start":"",
			"order_time_end":""
		}
		"""
	Then gddj获得客户端订单列表
		"""
		[]
		"""

Scenario:4 客户端订单列表按'订单状态'查询
	Given gddj登录商品管理系统
	#待发货状态
	When gddj设置客户端订单列表查询条件
		"""
		{
			"order_id":"",
			"product_name":"",
			"order_status":"待发货",
			"order_time_start":"",
			"order_time_end":""
		}
		"""
	Then gddj获得客户端订单列表
		"""
		[{
			"order_id":"201-固定底价店铺",
			"order_status":"待发货"
		},{
			"order_id":"104-固定底价店铺",
			"order_status":"待发货"
		},{
			"order_id":"103-固定底价店铺",
			"order_status":"待发货"
		},{
			"order_id":"102-固定底价店铺",
			"order_status":"待发货"
		}]
		"""
	#已发货状态
	When gddj对订单进行发货
		"""
		{
			"order_no": "102-固定底价店铺",
			"logistics": "申通快递",
			"number": "10201",
			"shipper": "gddj"
		}
		"""
	When gddj设置客户端订单列表查询条件
		"""
		{
			"order_id":"",
			"product_name":"",
			"order_status":"已发货",
			"order_time_start":"",
			"order_time_end":""
		}
		"""
	Then gddj获得客户端订单列表
		"""
		[{
			"order_id":"102-固定底价店铺",
			"order_status":"已发货"
		}]
		"""

Scenario:5 客户端订单列表按'下单时间'查询
	Given gddj登录商品管理系统
	#开始时间等于结束时间
	When gddj设置客户端订单列表查询条件
		"""
		{
			"order_id":"",
			"product_name":"",
			"order_status":"全部",
			"order_time_start":"2016-10-12 00:00",
			"order_time_end":"2016-10-12 00:00"
		}
		"""
	Then gddj获得客户端订单列表
		"""
		[{
			"order_id":"102-固定底价店铺",
			"order_time":"2016-10-12 00:00:00"
		}]
		"""
	#开始时间小于结束时间
	When gddj设置客户端订单列表查询条件
		"""
		{
			"order_id":"",
			"product_name":"",
			"order_status":"全部",
			"order_time_start":"2016-10-12 00:00",
			"order_time_end":"2016-10-15 23:59"
		}
		"""
	Then gddj获得客户端订单列表
		"""
		[{
			"order_id":"105-固定底价店铺",
			"order_time":"2016-10-15 00:00:00"
		},{
			"order_id":"104-固定底价店铺",
			"order_time":"2016-10-14 00:00:00"
		},{
			"order_id":"103-固定底价店铺",
			"order_time":"2016-10-13 00:00:00"
		},{
			"order_id":"102-固定底价店铺",
			"order_time":"2016-10-12 00:00:00"
		}]
		"""
	#开始时间大于结束时间（系统没做控制，查询结果为空）
	When gddj设置客户端订单列表查询条件
		"""
		{
			"order_id":"",
			"product_name":"",
			"order_status":"全部",
			"order_time_start":"2016-10-14 00:00",
			"order_time_end":"2016-10-12 00:00"
		}
		"""
	Then gddj获得客户端订单列表
		"""
		[]
		"""

Scenario:6 客户端订单列表组合查询查询
	Given gddj登录商品管理系统
	When gddj设置客户端订单列表查询条件
		"""
		{
			"order_id":"102-固定底价店铺",
			"product_name":"固定商品",
			"order_status":"待发货",
			"order_time_start":"2016-10-12 00:00",
			"order_time_end":"2016-10-15 00:00"
		}
		"""
	Then gddj获得客户端订单列表
		"""
		[{
			"order_id":"102-固定底价店铺"
		}]
		"""