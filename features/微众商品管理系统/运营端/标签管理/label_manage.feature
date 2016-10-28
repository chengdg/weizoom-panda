#_author_:张三香 2016.10.20

Feature:运营端标签管理
	"""
		1.标签管理列表字段
			分类:商品标签分类名称
			标签:显示标签分类下的所有标签值，点击【+】可以添加标签值，标签值可以删除不能修改
			操作:【删除】，点击【删除】是删除整个标签分类；删除使用中的标签后，商品和商品分类的标签随之消失
		2.标签管理列表顺序：添加时间的正序
		3.删除整个标签分类和单个标签值时，都会有确认提示"确认删除么？ 确定/取消"
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
			"remark":"固定底价客户备注信息",
			"create_time":"2016-10-10 09:00:00"
		}
		"""
	Given gddj登录商品管理系统
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
			"is_enable_model":false,
			"purchase_price":20.00,
			"weight": 1,
			"stocks": 100,
			"limit_zone_type":"无限制",
			"postage":1.00,
			"image":["love.png"],
			"detail": "商品2描述信息",
			"create_time":"2016-10-18 09:00"
		}
		"""

	Given 添加自营平台账号
		"""
		[{
			"account":"zy1",
			"self_shop_name":"自营平台1"
		}]
		"""

Scenario:1 运营端添加商品标签
	Given yunying登录商品管理系统
	Then yunying获得标签管理列表
		"""
		[]
		"""
	When yunying添加商品标签
		"""
		{
			"label_category":"品牌",
			"label_values":[]
		}
		"""
	When yunying添加商品标签
		"""
		{
			"label_category":"省份",
			"label_values":["山东","山西","湖南","湖北"]
		}
		"""
	Then yunying获得标签管理列表
		"""
		[{
			"label_category":"品牌",
			"label_values":[]
		},{
			"label_category":"省份",
			"label_values":["山东","山西","湖南","湖北"]
		}]
		"""

Scenario:2 运营向标签分类中添加标签值
	Given yunying登录商品管理系统
	When yunying添加商品标签
		"""
		{
			"label_category":"品牌",
			"label_values":[]
		}
		"""
	When yunying添加商品标签
		"""
		{
			"label_category":"省份",
			"label_values":["山东","山西"]
		}
		"""
	When yunying向商品标签'省份'中添加标签值
		"""
		{
			"value":"国际品牌"
		}
		"""
	When yunying向商品标签'省份'中添加标签值
		"""
		{
			"value":"湖北"
		}
		"""
	Then yunying获得标签管理列表
		"""
		[{
			"label_category":"品牌",
			"label_values":["国际品牌"]
		},{
			"label_category":"省份",
			"label_values":["山东","山西","湖北"]
		}]
		"""

Scenario:3 运营从标签分类中删除标签值
	Given yunying登录商品管理系统
	When yunying添加商品标签
		"""
		{
			"label_category":"省份",
			"label_values":["山东","山西","湖北"]
		}
		"""
	When yunying给商品分类'服装-泡面'配置标签
		"""
		[{
			"label_category":"省份",
			"selected_label_values":["山西"]
		}]
		"""
	When yunying给商品'商品1'配置标签
		"""
		[{
			"label_category":"省份",
			"selected_label_values":["山西"]
		}]
		"""
	When yunying给商品'商品2'配置标签
		"""
		[{
			"label_category":"省份",
			"selected_label_values":["湖北"]
		}]
		"""
	When yunying同步商品到自营平台
		"""
		{
			"products":["商品2"],
			"platforms":["自营平台1"]
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品2",
			"product_label":["湖北"],
			"storage_status":"已入库,已同步"
		},{
			"name":"商品1",
			"product_label":["山西"],
			"storage_status":"待入库"
		}]
		"""
	Then yuyning获得商品分类'食品'
		"""
		{
			"食品":
				[{
					"name":"饼干",
					"label":[]
				},{
					"name":"泡面",
					"label":["山西"]
				}]
		}
		"""
	Given zy1登录系统
	Then zy1获得商品池所有商品列表
		"""
		[{
			"product_info":{"name":"商品2"},
			"product_label":["湖北"]
		}]
		"""

	#删除未使用的标签值
	When yunying删除商品标签'省份'的标签值'山东'
	Then yunying获得标签管理列表
		"""
		[{
			"label_category":"省份",
			"label_values":["山西"]
		}]
		"""

	#删除使用中的标签值（使用标签的商品状态为'待入库'或'已入库,已同步'）
	When yunying删除商品标签'省份'的标签值'山西'
	Then yunying获得标签管理列表
		"""
		[{
			"label_category":"省份",
			"label_values":["湖北"]
		}]
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品2",
			"product_label":["湖北"],
			"storage_status":"已入库,已同步"
		},{
			"name":"商品1",
			"product_label":[],
			"storage_status":"待入库"
		}]
		"""
	Then yunying获得商品分类'食品'
		"""
		{
			"食品":
				[{
					"name":"饼干",
					"label":[]
				},{
					"name":"泡面",
					"label":[]
				}]
		}
		"""
	#使用该标签的商品已同步到自营平台
	When yunying删除商品标签'省份'的标签值'湖北'
	Then yunying获得商品列表
		"""
		[{
			"name":"商品2",
			"product_label":[],
			"storage_status":"已入库,已同步"
		},{
			"name":"商品1",
			"product_label":[],
			"storage_status":"待入库"
		}]
		"""
	#校验weapp商品池中商品的变化
	Given zy1登录系统
	Then zy1获得商品池所有商品列表
		"""
		[{
			"product_info":{"name":"商品2"},
			"product_label":[]
		}]
		"""

Scenario:4 运营删除整个商品标签分类
	Given yunying登录商品管理系统
	When yunying添加商品标签
		"""
		{
			"label_category":"省份",
			"label_values":["山东","山西"]
		}
		"""
	When yunying添加商品标签
		"""
		{
			"label_category":"年龄",
			"label_values":["中年","老年"]
		}
		"""
	When yunying添加商品标签
		"""
		{
			"label_category":"水果",
			"label_values":["进口","国内"]
		}
		"""
	Then yunying获得标签管理列表
		"""
		[{
			"label_category":"省份",
			"label_values":["山东","山西"]
		},{
			"label_category":"年龄",
			"label_values":["中年","老年"]
		},{
			"label_category":"水果",
			"label_values":["进口","国内"]
		}]
		"""
	When yunying给商品分类'服装-泡面'配置标签
		"""
		[{
			"label_category":"省份",
			"selected_label_values":["山西"]
		}]
		"""
	When yunying给商品'商品1'配置标签
		"""
		[{
			"label_category":"省份",
			"selected_label_values":["山东","山西"]
		}]
		"""
	When yunying给商品'商品2'配置标签
		"""
		[{
			"label_category":"年龄",
			"selected_label_values":["中年"]
		}]
		"""
	When yunying同步商品到自营平台
		"""
		{
			"products":["商品2"],
			"platforms":["自营平台1"]
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品2",
			"product_label":["中年"],
			"storage_status":"已入库,已同步"
		},{
			"name":"商品1",
			"product_label":["山东","山西"],
			"storage_status":"待入库"
		}]
		"""
	Then yunying获得商品分类'食品'
		"""
		{
			"食品":
				[{
					"name":"饼干",
					"label":[]
				},{
					"name":"泡面",
					"label":["山西"]
				}]
		}
		"""

	#删除未使用的标签分类
		When yunying删除商品标签'水果'
		Then yunying获得标签管理列表
			"""
			[{
				"label_category":"省份",
				"label_values":["山东","山西"]
			},{
				"label_category":"年龄",
				"label_values":["中年","老年"]
			}]
			"""
	#删除使用中的标签分类
		When yunying删除商品标签'省份'
		Then yunying获得标签管理列表
			"""
			[{
				"label_category":"年龄",
				"label_values":["中年","老年"]
			}]
			"""
		Then yunying获得商品列表
			"""
			[{
				"name":"商品2",
				"product_label":["中年"],
				"storage_status":"已入库,已同步"
			},{
				"name":"商品1",
				"product_label":[],
				"storage_status":"待入库"
			}]
			"""
		Then yuyning获得商品分类'食品'
			"""
			{
				"食品":
					[{
						"name":"饼干",
						"label":[]
					},{
						"name":"泡面",
						"label":[]
					}]
			}
			"""
		When yunying删除商品标签'年龄'
		Then yunying获得标签管理列表
			"""
			[]
			"""
		Then yunying获得商品列表
			"""
			[{
				"name":"商品2",
				"product_label":[],
				"storage_status":"已入库,已同步"
			},{
				"name":"商品1",
				"product_label":[],
				"storage_status":"待入库"
			}]
			"""
		#校验weapp商品池中商品的变化
		Given zy1登录系统
		Then zy1获得商品池所有商品列表
			"""
			[{
				"product_info":{"name":"商品2"},
				"product_label":[]
			}]
			"""