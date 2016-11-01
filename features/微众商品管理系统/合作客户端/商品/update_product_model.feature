#_author_:张三香 2016.10.19

Feature:修改商品规格
	"""
		1、panda中不支持修改规格的名名称
		2、允许增加规格值、删除规格值
		3、修改规格的显示样式（文本改成图片，图片改成文本）
			a:文本-规格值+图片，修改样式为'图片'后，规格值则显示对应文本的图片
			b:文本-规格值，修改样式为'图片'后，规格值仍则显示文本
			c:图片-规格值+图片，修改样式为'文本'后，规格值则显示对应图片的文本
			d:图片-规格值，修改样式为'文本'后，规格值仍显示文本
		4、更新商品正在使用的规格时，商品中的规格信息也随着变化
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
			"remark":"固定底价客户备注信息",
			"create_time":"2016-10-10 09:00:00"
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

Scenario:1 更新商品规格信息（无商品使用该规格）
	Jobs更新商品规格后, 更新包括：
		1.增加、删除规格值
		2.修改规格的显示样式
	Given gddj登录商品管理系统
	#向规格中增加规则值
	When gddj向商品规格'颜色'中增加规格值
		"""
		{
			"values":
				{
					"name": "黄色",
					"image": "/standard_static/test_resource_img/hangzhou3.jpg"
				}
		}
		"""
	#从规格中删除规格值
	When gddj删除商品规格'颜色'的规格值'白色'
	#将规格类型又图片修改成文本
	When gddj修改商品规格'颜色'的类型为
		"""
		{
			"type": "文本"
		}
		"""
	Then gddj能获取商品规格'颜色'
		"""
		{
			"name": "颜色",
			"type": "文本",
			"values": [{
				"name": "黑色",
				"image": "/standard_static/test_resource_img/hangzhou1.jpg"
			},{
				"name": "黄色",
				"image": "/standard_static/test_resource_img/hangzhou3.jpg"
			}]
		}
		"""
	#将规格类型又文本修改成图片
	When gddj修改商品规格'尺寸'的类型为
		"""
		{
			"type": "图片"
		}
		"""
	Then gddj能获取商品规格'尺寸'
		"""
		{
			"name": "尺寸",
			"type": "图片",
			"values": [{
				"name": "M",
				"image":""
			},{
				"name": "S",
				"image": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]
		}
		"""
	#校验商品规格列表
	Then gddj能获取商品规格列表
		"""
		[{
			"name": "颜色",
			"type": "文本",
			"values": [{
				"name": "黑色",
				"image": "/standard_static/test_resource_img/hangzhou1.jpg"
			},{
				"name": "黄色",
				"image": "/standard_static/test_resource_img/hangzhou3.jpg"
			}]
		},{
			"name": "尺寸",
			"type": "图片",
			"values": [{
				"name": "M",
				"image":""
			},{
				"name": "S",
				"image": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]
		}]
		"""

Scenario:2 删除商品规格的规格值（有商品（待入库、未上架状态）使用该规格）
	1.创建如下多规格商品:
		商品1-黑色
		商品2-黑色 S  白色 S
		商品3-黑色 M  黑色 S
	2.当删除规格值'黑色'后，校验商品的变化
		商品1-商品详情页规格为空
		商品2-商品详情页只显示规格'白色 S'
		商品3-商品详情页规格为空
		备注:目前panda商品列表中对此种情况没有做处理（列表中显示的仍然是规格值未被删除时的信息）

	Given gddj登录商品管理系统
	When gddj添加商品
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":true,
			"model": {
				"models": {
					"黑色": {
						"purchase_price": 10.00,
						"weight":1.0,
						"stocks":100
					}
				}
			},
			"limit_zone_type":"无限制",
			"postage":1.00,
			"image": "love.png",
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
			"image": "love.png",
			"detail": "商品2描述信息",
			"create_time":"2016-10-18 09:00"
		}
		"""
	When gddj添加商品
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品3",
			"promotion_title":"促销标题3",
			"is_enable_model":true,
			"model": {
				"models": {
					"黑色 M": {
						"purchase_price": 10.00,
						"weight":1.0,
						"stocks":100
					},
					"黑色 S": {
						"purchase_price": 20.00,
						"weight": 2.0,
						"stocks":200
					}
				}
			},
			"limit_zone_type":"无限制",
			"postage":3.00,
			"image": "love.png",
			"detail": "商品3描述信息",
			"create_time":"2016-10-18 10:00"
		}
		"""
	When gddj删除商品规格'颜色'的规格值'黑色'
	#校验商品规格
	Then gddj能获取商品规格'颜色'
		"""
		{
			"name": "颜色",
			"type": "文本",
			"values": [{
				"name": "白色",
				"image": ""
			}]
		}
		"""
	Then gddj能获取商品规格列表
		"""
		[{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "白色",
				"image": ""
			}]
		},{
			"name": "尺寸",
			"type": "文本",
			"values": [{
				"name": "M",
				"image":""
			},{
				"name": "S",
				"image": "/standard_static/test_resource_img/hangzhou2.jpg"
			}]
		}]
		"""
	#校验使用该规格值的商品的详情页
	Then gddj获得客户端商品'商品1'
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":true,
			"model": {
				"models": {}
				},
			"limit_zone_type":"无限制",
			"postage":1.00,
			"image": "love.png",
			"detail": "商品1描述信息",
			"create_time":"2016-10-18 08:00"
		}
		"""
	Then gddj获得客户端商品'商品2'
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品2",
			"promotion_title":"促销标题2",
			"is_enable_model":true,
			"model": {
				"models": {
					"白色 S": {
						"purchase_price": 20.00,
						"weight": 2.0,
						"stocks":200
					}
				}
			},
			"limit_zone_type":"无限制",
			"postage":2.00,
			"image": "love.png",
			"detail": "商品2描述信息",
			"create_time":"2016-10-18 09:00"
		}
		"""
	Then gddj获得客户端商品'商品3'
		"""
		{
			"product_category":"食品-饼干",
			"name":"商品3",
			"promotion_title":"促销标题3",
			"is_enable_model":true,
			"model": {
				"models": {}
				},
			"limit_zone_type":"无限制",
			"postage":3.00,
			"image": "love.png",
			"detail": "商品3描述信息",
			"create_time":"2016-10-18 10:00"
		}
		"""