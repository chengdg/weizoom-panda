#_author_:张三香 2016.10.21

Feature:给商品分类配置标签
	"""
		1.商品分类中可以通过二级分类中的【配置标签】给每个二级分类配置标签
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
			"分类1":
				[{
					"name":"a"
				},{
					"name":"b"
				}]
		}
		"""
	When yunying添加商品分类
		"""
		{
			"分类2":
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

Scenario:1 给商品分类配置标签（商品分类未被商品使用）
	Given yunying登录商品管理系统
	When yunying给商品分类配置标签
		"""
		{
			"product_category":"分类1-a"
			"label_info":
				{
					"label_category":"省份",
					"select_label_values":["山东","山西"]
				}
		}
		"""
	Then yunying获得商品分类'分类1'
		"""
		{
			"分类1":
				[{
					"name":"a",
					"label":["山东","山西"],
					"actions":["修改","删除","配置特殊资质","已配置标签"]
				},{
					"name":"b",
					"label":[],
					"actions":["修改","删除","配置特殊资质","配置标签"]
				}]
		}
		"""

Scenario:2 给商品分类配置标签（商品分类在被商品使用）
	#添加'固定底价'类型客户
	Given manager登录商品管理系统
	When manager添加账号
		"""
		{
			"type":"合作客户",
			"business_name":"北京大公司1",
			"shop_name":"固定底价店铺",
			"purchase_way":"固定底价",
			"payment_type":"自然月",
			"product_category":["分类2"],
			"products_limit":30,
			"start_time":"2016-10-20 10:00",
			"end_time":"2026-10-20 10:00",
			"login_name":"gddj",
			"login_password":"test"
		}
		"""
	#准备商品数据（商品1-待入库；商品2-已入库，已同步）
	Given gddj登录商品管理系统
	When gddj添加商品
		"""
		{
			"product_category":"分类2-饼干",
			"name":"商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":false,
			"purchase_price": 10.00,
			"weight": 1,
			"stocks": 100,
			"limit_zone_type":"无限制",
			"postage":1.00,
			"image": "love.png",
			"detail": "商品1描述信息"
		}
		"""
	When gddj添加商品
		"""
		{
			"product_category":"分类2-饼干",
			"name":"商品2",
			"promotion_title":"促销标题2",
			"is_enable_model":false,
			"purchase_price": 20.00,
			"weight": 1,
			"stocks": 100,
			"limit_zone_type":"无限制",
			"postage":1.00,
			"image": "love.png",
			"detail": "商品2描述信息"
		}
		"""
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
				"products":["商品2"],
				"platforms":["自营平台1"]
			}
			"""
	#给分类配置标签
	When yunying给商品分类配置标签
		"""
		{
			"product_category":"分类2-饼干"
			"label_info":
				{
					"label_category":"省份",
					"select_label_values":["山东","山西"]
				}
		}
		"""
	#运营端商品分类的校验
	Then yunying获得商品分类'分类2'
		"""
		{
			"分类2":
				[{
					"name":"饼干",
					"label":["山东","山西"],
					"actions":["修改","删除","配置特殊资质","已配置标签"]
				},{
					"name":"泡面",
					"label":[],
					"actions":["修改","删除","配置特殊资质","配置标签"]
				}]
		}
		"""
	#运营端商品列表的校验
	Then yunying获得商品列表
		"""
		[{
			"name":"商品2",
			"product_category":"分类2-饼干",
			"storage_status":"已入库,已同步",
			"product_label":["山东","山西"]
		},{
			"name":"商品1",
			"product_category":"分类2-饼干",
			"storage_status":"待入库",
			"product_label":["山东","山西"]
		}]
		"""
	#weapp端商品池的校验
	Given zy1登录系统
	Then zy1获得商品池所有商品列表
		"""
		[{
			"product_info":{"name":"商品2"},
			"product_category":"分类2-饼干",
			"product_label":["山东","山西"]
		}]
		"""
