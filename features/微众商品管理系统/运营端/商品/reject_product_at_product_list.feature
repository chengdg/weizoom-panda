#_author_:张三香 2016.10.24

Feature:运营驳回修改商品
	"""
		1.'待入库'状态的商品操作列存在【驳回修改】按钮
		2.点击【驳回修改】按钮，显示'商品驳回'弹框，弹框中存在一条已定义好的驳回原因和输入框（可自定义驳回原因）
		3.输入驳回原因点击确定后，运营端该商品状态会由'待入库'变为'入库驳回'状态；对应客户端该商品状态由'待入库'变为'入库驳回>>'
		4.运营端和客户端的'待入库'和'入库驳回'状态的商品，鼠标悬浮时会显示驳回原因（待入库无驳回记录时显示'暂无记录'）
		5.不勾选商品直接点击列表上方的【批量驳回】按钮，页面上方红条提示'请先选择要驳回的商品!'
		6.勾选商品后点击列表上方的【批量驳回】按钮，显示'商品驳回'弹框，和单个【驳回修改】逻辑一样
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
	#添加商品
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
			"detail": "商品2描述信息"
		}
		"""

Scenario:1 运营驳回修改单个商品
	Given yunying登录商品管理系统
	When yunying批量驳回修改商品
	#驳回修改单个商品
	When yunying在'商品'列表批量驳回修改商品
		"""
		{
			"name":["商品1"],
			"reject_reason":"驳回修改原因1"
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品2",
			"storage_status":"待入库",
			"actions":["同步商品","驳回修改","删除商品"]
		},{
			"name":"商品1",
			"storage_status":"入库驳回",
			"actions":["删除商品"]
		}]
		"""
	#客户端商品列表的校验
	Given gddj登录商品管理系统
	Then gddj获得商品列表
		"""
		[{
			"product_info":{"name":"商品2"},
			"storage_status":"待入库",
			"sale_status":"未上架",
			"actions":["编辑"]
		},{
			"product_info":{"name":"商品1"},
			"storage_status":"入库驳回",
			"sale_status":"未上架",
			"actions":["重新修改提交"]
		}]
		"""

Scenario:2 运营批量驳回修改多个商品
	Given yunying登录商品管理系统
	When yunying批量驳回修改商品
	#批量驳回修改多个商品
	When yunying在'商品'列表批量驳回修改商品
		"""
		{
			"name":["商品1","商品2"],
			"reject_reason":"驳回修改原因1"
		}
		"""
	Then yunying获得商品列表
		"""
		[{
			"name":"商品2",
			"storage_status":"入库驳回",
			"actions":["删除商品"]
		},{
			"name":"商品1",
			"storage_status":"入库驳回",
			"actions":["删除商品"]
		}]
		"""
	#客户端商品列表的校验
	Given gddj登录商品管理系统
	Then gddj获得商品列表
		"""
		[{
			"product_info":{"name":"商品2"},
			"storage_status":"入库驳回",
			"sale_status":"未上架",
			"actions":["重新修改提交"]
		},{
			"product_info":{"name":"商品1"},
			"storage_status":"入库驳回",
			"sale_status":"未上架",
			"actions":["重新修改提交"]
		}]
		"""