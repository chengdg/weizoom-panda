#_author_:张三香 2016.10.21

Feature:运营端更新商品分类
	"""
		1.点击一级分类操作列中的【修改】按钮，可以修改一级分类的名称
		2.点击二级分类对应的【修改】按钮，显示的弹窗中可以修改二级分类的名称
		3.点击【+添加分类】按钮，弹框中'上级分类'选择已存在的一级分类，可以向该一级分类中添加二级分类
		4.删除一级和二级分类
			a.删除一级分类（无二级分类且未开放给客户）,提示"确认删除该商品分类吗？ 确定/取消"，点击【确定】可删除商品分类，提示'删除分类成功'
			b.删除一级分类（无二级分类且已开放给客户）,提示"确认删除该商品分类吗？ 确定/取消"，点击【确定】会提示'分类已被使用，删除失败，请先修改客户账户'
			c.删除一级分类（有二级分类）,提示"确认删除该商品分类吗？ 确定/取消"，点击【确定】会提示'该分类下还存在额二级分类，请先删除二级分类'
			d.删除二级分类（未被使用）,提示"确认删除该商品分类吗？ 确定/取消"，点击【确定】可删除商品分类，提示'删除分类成功'
			e.删除二级分类（在被使用）,提示"确认删除该商品分类吗？ 确定/取消"，点击【确定】会提示'该分类正在被使用，请先将商品调整分类后再删除分类'
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
			"分类1":[]
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
	#准备商品数据（商品1-待入库；商品2-已同步，已入库/商品池中；商品3-已同步，已入库/已上架）
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
			"image":["love.png"],
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
			"image":["love.png"],
			"detail": "商品2描述信息"
		}
		"""
	When gddj添加商品
		"""
		{
			"product_category":"分类2-饼干",
			"name":"商品3",
			"promotion_title":"促销标题3",
			"is_enable_model":false,
			"purchase_price": 30.00,
			"weight": 1,
			"stocks": 100,
			"limit_zone_type":"无限制",
			"postage":1.00,
			"image":["love.png"],
			"detail": "商品3描述信息"
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
			"products":["商品2","商品3"],
			"platforms":["自营平台1"]
		}
		"""
	Given zy1登录系统
	When zy1批量上架商品池商品
		"""
		["商品3"]
		"""

Scenario:1 修改一级分类的名称
	#该分类没有开放给客户
		Given yunying登录商品管理系统
		When yunying修改商品分类'分类1'的名称为'分类1修改'
		Then yunying获得商品分类列表
			"""
			[{
				"categroy_name":"分类2"
			},{
				"categroy_name":"分类1修改"
			}]
			"""

	#该分类开放给客户，且有商品在使用
		When yunying修改商品分类'分类2'的名称为'分类2修改'
		#运营端商品分类列表的校验
			Then yunying获得商品分类列表
				"""
				[{
					"categroy_name":"分类2修改"
				},{
					"categroy_name":"分类1修改"
				}]
				"""
			Then yunying获得商品分类'分类2修改'
				"""
				{
					"分类2修改":
						[{
							"name":"饼干"
						},{
							"name":"泡面"
						}]
				}
				"""
		#运营端商品列表的校验
			Then yunying获得商品列表
				"""
				[{
					"name":"商品3",
					"product_category":"分类2修改-饼干",
					"storage_status":"已入库,已同步"
				},{
					"name":"商品2",
					"product_category":"分类2修改-饼干",
					"storage_status":"已入库,已同步"
				},{
					"name":"商品1",
					"product_category":"分类2修改-饼干",
					"storage_status":"待入库"
				}]
				"""
		#客户端商品列表的校验
			Given gddj登录商品管理系统
			Then gddj获得商品列表
				"""
				[{
					"product_info":{"name":"商品3"},
					"product_category":"分类2修改-饼干",
					"storage_status":"已入库",
					"sale_status":"已上架"
				},{
					"product_info":{"name":"商品2"},
					"product_category":"分类2修改-饼干",
					"storage_status":"已入库",
					"sale_status":"未上架"
				},{
					"product_info":{"name":"商品1"},
					"product_category":"分类2修改-饼干",
					"storage_status":"待入库",
					"sale_status":"未上架"
				}]
				"""
		#weapp端商品池及在售商品列表的校验
			Given zy1登录系统
			Then zy1获得商品池所有商品列表
				"""
				[{
					"product_info":{"name": "商品2"},
					"product_category":"分类2修改-饼干"
				}]
				"""
			Then zy1能获得'在售'商品列表
				"""
				[{
					"product_info":{"name": "商品3"},
					"product_category":"分类2修改-饼干"
				}]
				"""
		#账号管理列表中的校验
			Given manager登录商品管理系统
			Then manager获得账号管理列表
				"""
				[{
					"shop_name":"固定底价店铺",
					"business_name":"北京大公司1",
					"login_name":"gddj",
					"product_category":["分类2修改"]
				}]
				"""

Scenario:2 修改二级分类的名称
	#修改没有商品使用的二级分类
		Given yunying登录商品管理系统
		When yunying修改商品分类'分类2'的二级分类'泡面'的名称为'泡面修改'
		Then yunying获得商品分类'分类2'
			"""
			{
				"分类2修改":
					[{
						"name":"饼干"
					},{
						"name":"泡面修改"
					}]
			}
			"""
	#修改有商品使用的二级分类名称
		Given yunying登录商品管理系统
		When yunying修改商品分类'分类2'的二级分类'饼干'的名称为'饼干修改'
		#运营端商品分类的校验
			Then yunying获得商品分类'分类2'
				"""
				{
					"分类2":
						[{
							"name":"饼干修改"
						},{
							"name":"泡面修改"
						}]
				}
				"""
		#运营端商品列表的校验
			Then yunying获得商品列表
				"""
				[{
					"name":"商品3",
					"product_category":"分类2-饼干修改",
					"storage_status":"已入库,已同步"
				},{
					"name":"商品2",
					"product_category":"分类2-饼干修改",
					"storage_status":"已入库,已同步"
				},{
					"name":"商品1",
					"product_category":"分类2-饼干修改",
					"storage_status":"待入库"
				}]
				"""
		#客户端商品列表的校验
			Given gddj登录商品管理系统
			Then gddj获得商品列表
				"""
				[{
					"product_info":{"name":"商品3"},
					"product_category":"分类2-饼干修改",
					"storage_status":"已入库",
					"sale_status":"已上架"
				},{
					"product_info":{"name":"商品2"},
					"product_category":"分类2-饼干修改",
					"storage_status":"已入库",
					"sale_status":"未上架"
				},{
					"product_info":{"name":"商品1"},
					"product_category":"分类2-饼干修改",
					"storage_status":"待入库",
					"sale_status":"未上架"
				}]
				"""
		#weapp端商品池及在售商品列表的校验
			Given zy1登录系统
			Then zy1获得商品池所有商品列表
				"""
				[{
					"product_info":{"name":"商品2"},
					"product_category":"分类2-饼干修改"
				}]
				"""
			Then zy1能获得'在售'商品列表
				"""
				[{
					"product_info":{"name":"商品3"},
					"product_category":"分类2-饼干修改"
				}]
				"""

Scenario:3 一级分类中添加二级分类
	Given yunying登录商品管理系统
	When yunying向商品分类'分类1'中添加二级分类
		"""
		{
			"values":
			[{
				"name":"a"
			},{
				"name":"b"
			}]
		}
		"""
	When yunying向商品分类'分类2'中添加二级分类
		"""
		{
			"values":
			[{
				"name":"果冻"
			}]
		}
		"""
	Then yunying获得商品分类'分类1'
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
	Then yunying获得商品分类'分类2'
		"""
		{
			"分类2":
				[{
					"name":"饼干"
				},{
					"name":"泡面"
				},{
					"name":"果冻"
				}]
		}
		"""

Scenario:4 一级分类中删除二级分类
	#删除未被商品使用的二级分类
		Given yunying登录商品管理系统
		When yunying删除商品分类'分类2'的二级分类'泡面'
		Then yunying获得商品分类'分类2'
			"""
			{
				"分类2":
					[{
						"name":"饼干"
					}]
			}
			"""
	#删除在被商品使用的二级分类
		When yunying删除商品分类'分类2'的二级分类'饼干'
		Then yunying获得提示信息'该分类正在被使用，请先将商品调整分类后再删除分类'