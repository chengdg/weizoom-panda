#_author_:张三香 2016.10.18

Feature:添加商品规格
	"""
		1.客户端允许添加商品规格
		2.商品规格列表字段信息
			规格名:显示规格的名称
			显示样式:文本/图片
			规格值：显示规格中的规格值(允许添加和删除)
			操作：【删除】
		3.商品规格列表排序：添加时间正序显示
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

Scenario:1 添加商品规格
	1.gddj添加空的规格（文本和图片类型）
	2.gddj添加非空的规格（文本和图片类型）

	Given gddj登录商品管理系统
	Then gddj能获取商品规格列表
		"""
		[]
		"""
	When gddj添加商品规格
		"""
		{
			"name": "文本空规格",
			"type": "文本",
			"values": []
		}
		"""
	Then gddj能获取商品规格'文本空规格'
		"""
		{
			"name": "文本空规格",
			"type": "文本",
			"values": []
		}
		"""
	When gddj添加商品规格
		"""
		{
			"name": "图片空规格",
			"type": "图片",
			"values": []
		}
		"""
	Then gddj能获取商品规格'图片空规格'
		"""
		{
			"name": "图片空规格",
			"type": "图片",
			"values": []
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
	Then gddj能获取商品规格'颜色'
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
	Then gddj能获取商品规格'尺寸'
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
	And gddj能获取商品规格列表
		"""
		[{
			"name": "文本空规格",
			"type": "文本",
			"values": []
		},{
			"name": "图片空规格",
			"type": "图片",
			"values": []
		},{
			"name": "颜色",
			"type": "图片",
			"values": [{
				"name": "黑色",
				"image": "/standard_static/test_resource_img/hangzhou1.jpg"
			},{
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
