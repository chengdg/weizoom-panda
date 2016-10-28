#_author_:张三香 2016.10.27

Feature:运营端商品更新列表进行驳回修改
	"""
		商品更新列表点击商品操作列的【驳回修改】，会显示'商品驳回'弹框，选择或填写驳回原因后点击【确定】商品驳回成功
			运营端'商品更新'列表中该商品消失
			运营端'商品'列表中该商品状态变为'修改驳回'
			客户端'商品'列表中该商品状态目前未变化（需求会要优化）
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
			"products":["商品1","商品2"],
			"platforms":["自营平台1","自营平台2"]
		}
		"""
	Given gddj登录商品管理系统
	When gddj编辑商品'商品1'
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":false,
			"purchase_price": 10.99,
			"weight": 1,
			"stocks": 100,
			"limit_zone_type":"无限制",
			"postage":1.00,
			"image":["love.png"],
			"detail": "商品1描述信息"
		}
		"""
	When gddj编辑商品'商品2'
		"""
		{
			"product_category":"食品-泡面",
			"name":"商品2",
			"promotion_title":"促销标题2",
			"is_enable_model":true,
			"model": {
				"models": {
					"黑色 S": {
						"purchase_price": 21.99,
						"weight":1.0,
						"stocks":100
					},
					"白色 S": {
						"purchase_price": 22.99,
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

Scenario:1 运营端商品更新列表'驳回修改'商品
	Given yunying登录商品管理系统
	When yunying在'商品更新'列表驳回修改商品
		"""
		{
			"name":"商品1",
			"reject_reason":"驳回修改原因1"
		}
		"""
	#运营端商品更新列表的校验
	Then yunying获得商品更新列表
		"""
		[{
			"product_info":{"name":"商品2"}
		}]
		"""
	#运营端商品列表的校验（状态变为'修改驳回'）
	Then yunying获得商品列表
		"""
		[{
			"name":"商品2",
			"storage_status":"修改驳回"
		},{
			"name":"商品1",
			"storage_status":"已入库,已同步"
		}]
		"""
	#客户端商品列表的校验（待需求最终确定后补充）