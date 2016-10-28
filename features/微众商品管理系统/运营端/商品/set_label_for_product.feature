#_author_:张三香 2016.10.24

Feature:给商品配置标签
	"""
		1.商品列表中可以通过【配置标签】给商品配置单个或多个标签
		2.商品标签的变更逻辑
			一个根据商品分类自动携带标签的商品，只要人工将标签修改或增减了，都不会再根据商品分类标签配置的变化再变化了
			如果人工没有自定义修改过，是会根据分类配置的调整自动更新的
		3.商品同步后若再通过【配置标签】按钮修改商品的标签，会自动同步到weapp中
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
	When yunying添加商品标签
		"""
		{
			"label_category":"省份",
			"label_values":["山东","山西","湖南","湖北"]
		}
		"""
	When yunying添加商品标签
		"""
		{
			"label_category":"其他",
			"label_values":["哈哈","呵呵"]
		}
		"""
	Given manager登录商品管理系统
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
			"product_category":"食品-泡面",
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

Scenario:1 给商品配置标签（待入库）
	Given yunying登录商品管理系统
	Then yunying获得商品列表
		"""
		[{
			"name":"商品2",
			"product_category":"食品-泡面",
			"storage_status":"待入库",
			"product_label":[]
		},{
			"name":"商品1",
			"product_category":"食品-饼干",
			"storage_status":"待入库",
			"product_label":[]
		}]
		"""
	When yunying给商品'商品1'配置标签
		"""
		{
			"label_category":"省份",
			"selected_label_values":["山西"]
		}
		"""
	When yunying给商品'商品1'配置标签
		"""
		{
			"label_category":"其他",
			"selected_label_values":["哈哈","呵呵"]
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品2",
			"product_category":"食品-泡面",
			"storage_status":"待入库",
			"product_label":[]
		},{
			"name":"商品1",
			"product_category":"食品-饼干",
			"storage_status":"待入库",
			"product_label":["山西","哈哈","呵呵"]
		}]
		"""

Scenario:2 给商品配置标签（已入库,已同步）
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
	#先同步后配置标签（商品2-山西+哈哈）
		When yunying同步商品到自营平台
			"""
			{
				"products":["商品2"],
				"platforms":["自营平台1","自营平台2"]
			}
			"""
		When yunying给商品'商品2'配置标签
			"""
			{
				"label_category":"省份",
				"selected_label_values":["山西"]
			}
			"""
		#运营端商品列表的校验
		Then yunying获得商品列表
			"""
			[{
				"name":"商品2",
				"product_category":"食品-泡面",
				"storage_status":"已入库,已同步",
				"product_label":["山西"]
			},{
				"name":"商品1",
				"product_category":"食品-饼干",
				"storage_status":"待入库",
				"product_label":[]
			}]
			"""
		#weapp端商品池的校验
		Given zy1登录系统
		Then zy1获得商品池所有商品列表
			"""
			[{
				"product_info":{"name":"商品2"},
				"product_category":"食品-泡面",
				"product_label":["山西"]
			}]
			"""
		Given zy2登录系统
		Then zy2获得商品池所有商品列表
			"""
			[{
				"product_info":{"name":"商品2"},
				"product_category":"食品-泡面",
				"product_label":["山西"]
			}]
			"""

		#同步后若再修改（增加）商品标签配置，会自动同步到weapp
			Given yunying登录商品管理系统
			When yunying给商品'商品2'配置标签
				"""
				{
					"label_category":"其他",
					"selected_label_values":["哈哈"]
				}
				"""
			#运营端商品列表的校验
			Then yunying获得商品列表
				"""
				[{
					"name":"商品2",
					"product_category":"食品-泡面",
					"storage_status":"已入库,已同步",
					"product_label":["山西","哈哈"]
				},{
					"name":"商品1",
					"product_category":"食品-饼干",
					"storage_status":"待入库",
					"product_label":[]
				}]
				"""
			#weapp端商品池的校验
			Given zy1登录系统
			Then zy1获得商品池所有商品列表
				"""
				[{
					"product_info":{"name":"商品2"},
					"product_category":"食品-泡面",
					"product_label":["山西","哈哈"]
				}]
				"""
			Given zy2登录系统
			Then zy2获得商品池所有商品列表
				"""
				[{
					"product_info":{"name":"商品2"},
					"product_category":"食品-泡面",
					"product_label":["山西","哈哈"]
				}]
				"""

	#先配置标签再同步（'商品1-山东，湖北'变成'商品1-山东'）
		When yunying给商品'商品1'配置标签
			"""
			{
				"label_category":"省份",
				"selected_label_values":["山东","湖北"]
			}
			"""
		When yunying同步商品到自营平台
			"""
			{
				"products":["商品1"],
				"platforms":["自营平台1","自营平台2"]
			}
			"""
		#运营端商品列表的校验
		Then yunying获得商品列表
			"""
			[{
				"name":"商品2",
				"product_category":"食品-泡面",
				"storage_status":"已入库,已同步",
				"product_label":["山西","哈哈"]
			},{
				"name":"商品1",
				"product_category":"食品-饼干",
				"storage_status":"已入库,已同步",
				"product_label":["山东","湖北"]
			}]
			"""
		#weapp端商品池的校验
		Given zy1登录系统
		Then zy1获得商品池所有商品列表
			"""
			[{
				"product_info":{"name":"商品2"},
				"product_category":"食品-泡面",
				"product_label":["山西","哈哈"]
			},{
				"product_info":{"name":"商品1"},
				"product_category":"食品-饼干",
				"product_label":["山东","湖北"]
			}]
			"""
		Given zy2登录系统
		Then zy2获得商品池所有商品列表
			"""
			[{
				"product_info":{"name":"商品2"},
				"product_category":"食品-泡面",
				"product_label":["山西","哈哈"]
			},{
				"product_info":{"name":"商品1"},
				"product_category":"食品-饼干",
				"product_label":["山东","湖北"]
			}]
			"""
		#同步后若再修改（减少）商品标签配置，会自动同步到weapp
			Given yunying登录商品管理系统
			When yunying给商品'商品1'配置标签
				"""
				{
					"label_category":"省份",
					"selected_label_values":["山东"]
				}
				"""
			#运营端商品列表的校验
			Then yunying获得商品列表
				"""
				[{
					"name":"商品2",
					"product_category":"食品-泡面",
					"storage_status":"已入库,已同步",
					"product_label":["山西","哈哈"]
				},{
					"name":"商品1",
					"product_category":"食品-饼干",
					"storage_status":"已入库,已同步",
					"product_label":["山东"]
				}]
				"""
			#weapp端商品池的校验
			Given zy1登录系统
			Then zy1获得商品池所有商品列表
				"""
				[{
					"product_info":{"name":"商品2"},
					"product_category":"食品-泡面",
					"product_label":["山西","哈哈"]
				},{
					"product_info":{"name":"商品1"},
					"product_category":"食品-饼干",
					"product_label":["山东"]
				}]
				"""
			Given zy2登录系统
			Then zy2获得商品池所有商品列表
				"""
				[{
					"product_info":{"name":"商品2"},
					"product_category":"食品-泡面",
					"product_label":["山西","哈哈"]
				},{
					"product_info":{"name":"商品1"},
					"product_category":"食品-饼干",
					"product_label":["山东"]
				}]
				"""

Scenario:3 人工自定义修改过标签的商品不再根据商品分类标签配置的变化而变化
	Given yunying登录商品管理系统
	#人工给商品配置标签后，再修改商品分类的标签
		When yunying给商品'商品1'配置标签
			"""
			{
				"label_category":"省份",
				"selected_label_values":["山东"]
			}
			"""
		Then yunying获得商品列表
			"""
			[{
				"name":"商品2",
				"product_category":"食品-泡面",
				"storage_status":"待入库",
				"product_label":["山西"]
			},{
				"name":"商品1",
				"product_category":"食品-饼干",
				"storage_status":"待入库",
				"product_label":["山东"]
			}]
			"""
		When yunying给商品分类'食品-饼干'配置标签
			"""
			{
				"label_category":"省份",
				"selected_label_values":["山西"]
			}
			"""
		Then yunying获得商品列表
			"""
			[{
				"name":"商品2",
				"product_category":"食品-泡面",
				"storage_status":"待入库",
				"product_label":["山西"]
			},{
				"name":"商品1",
				"product_category":"食品-饼干",
				"storage_status":"待入库",
				"product_label":["山东"]
			}]
			"""
	#给商品分类配置标签，再人工修改商品标签，再修改商品分类的标签
			When yunying给商品分类'食品-泡面'配置标签
				"""
				{
					"label_category":"省份",
					"selected_label_values":["山东","山西"]
				}
				"""
			Then yunying获得商品列表
				"""
				[{
					"name":"商品2",
					"product_category":"食品-泡面",
					"storage_status":"待入库",
					"product_label":["山东","山西"]
				},{
					"name":"商品1",
					"product_category":"食品-饼干",
					"storage_status":"待入库",
					"product_label":["山东"]
				}]
				"""
			#人工修改商品标签
			When yunying给商品'商品2'配置标签
				"""
				{
					"label_category":"其他",
					"selected_label_values":["哈哈"]
				}
				"""
			Then yunying获得商品列表
				"""
				[{
					"name":"商品2",
					"product_category":"食品-泡面",
					"storage_status":"待入库",
					"product_label":["山东","山西","哈哈"]
				},{
					"name":"商品1",
					"product_category":"食品-饼干",
					"storage_status":"待入库",
					"product_label":["山东"]
				}]
				"""
			#人工修改过商品2的标签后，再修改商品分类的标签
			#商品分类中减少商品标签
			When yunying给商品分类'食品-泡面'配置标签
				"""
				{
					"label_category":"省份",
					"selected_label_values":["山东"]
				}
				"""
			Then yunying获得商品列表
				"""
				[{
					"name":"商品2",
					"product_category":"食品-泡面",
					"storage_status":"待入库",
					"product_label":["山东","山西","哈哈"]
				},{
					"name":"商品1",
					"product_category":"食品-饼干",
					"storage_status":"待入库",
					"product_label":["山东"]
				}]
				"""
			#商品分类中增加商品标签
			When yunying给商品分类'食品-泡面'配置标签
				"""
				{
					"label_category":"其他",
					"selected_label_values":["呵呵"]
				}
				"""
			Then yunying获得商品列表
				"""
				[{
					"name":"商品2",
					"product_category":"食品-泡面",
					"storage_status":"待入库",
					"product_label":["山东","山西","哈哈"]
				},{
					"name":"商品1",
					"product_category":"食品-饼干",
					"storage_status":"待入库",
					"product_label":["山东"]
				}]
				"""

Scenario:4 人工没自定义修改过标签的商品会根据商品分类标签配置的变化而变化
	Given yunying登录商品管理系统
	When yunying给商品分类'食品-泡面'配置标签
		"""
		{
			"label_category":"省份",
			"selected_label_values":["山东","山西"]
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品2",
			"product_category":"食品-泡面",
			"storage_status":"待入库",
			"product_label":["山东","山西"]
		},{
			"name":"商品1",
			"product_category":"食品-饼干",
			"storage_status":"待入库",
			"product_label":[]
		}]
		"""
	#商品分类中减少标签，商品会随之变化
		When yunying给商品分类'食品-泡面'配置标签
			"""
			{
				"label_category":"省份",
				"selected_label_values":["山东"]
			}
			"""
		Then yunying获得商品列表
			"""
			[{
				"name":"商品2",
				"product_category":"食品-泡面",
				"storage_status":"待入库",
				"product_label":["山东"]
			},{
				"name":"商品1",
				"product_category":"食品-饼干",
				"storage_status":"待入库",
				"product_label":[]
			}]
			"""
	#商品分类中增加标签，商品会随之变化
		When yunying给商品分类'食品-泡面'配置标签
			"""
			{
				"label_category":"其他",
				"selected_label_values":["哈哈"]
			}
			"""
		Then yunying获得商品列表
			"""
			[{
				"name":"商品2",
				"product_category":"食品-泡面",
				"storage_status":"待入库",
				"product_label":["山东","哈哈"]
			},{
				"name":"商品1",
				"product_category":"食品-饼干",
				"storage_status":"待入库",
				"product_label":[]
			}]
			"""