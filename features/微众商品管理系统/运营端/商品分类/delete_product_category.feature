#_author_:张三香 2016.10.21

Feature:运营端删除商品分类
	"""
		1.删除一级分类
			a.删除一级分类（无二级分类且未开放给客户）,提示"确认删除该商品分类吗？ 确定/取消"，点击【确定】可删除商品分类，提示'删除分类成功'
			b.删除一级分类（无二级分类且已开放给客户）,提示"确认删除该商品分类吗？ 确定/取消"，点击【确定】会提示'分类已被使用，删除失败，请先修改客户账户'
			c.删除一级分类（有二级分类）,提示"确认删除该商品分类吗？ 确定/取消"，点击【确定】会提示'该分类下还存在额二级分类，请先删除二级分类'
		2.删除一级分类后，weapp中的在售商品管理/待售商品管理/商品池列表中查询条件'商品分类'的一级分类下拉框中不再显示删除的一级分类
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
			"分类2":[]
		}
		"""
	When yunying添加商品分类
		"""
		{
			"分类3":
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
			"product_category":["分类2","分类3"],
			"products_limit":30,
			"start_time":"2016-10-20 10:00",
			"end_time":"2026-10-20 10:00",
			"login_name":"gddj",
			"login_password":"test"
		}
		"""

Scenario:1 删除一级分类（无二级分类且未开放给客户）
	Given yunying登录商品管理系统
	When yunying删除商品分类'分类1'
	Then yunying获得商品分类列表
		"""
		[{
			"categroy_name":"分类3"
		},{
			"categroy_name":"分类2"
		}]
		"""

Scenario:2 删除一级分类（无二级分类且已开放给客户）
	Given yunying登录商品管理系统
	When yunying删除商品分类'分类2'
	Then yunying获得提示信息'分类已被使用,删除失败,请先修改客户账户'
	Then yunying获得商品分类列表
		"""
		[{
			"categroy_name":"分类3"
		},{
			"categroy_name":"分类2"
		},{
			"categroy_name":"分类1"
		}]
		"""

Scenario:3 删除一级分类（有二级分类）
	Given yunying登录商品管理系统
	When yunying删除商品分类'分类3'
	Then yunying获得提示信息'该分类下还存在额二级分类，请先删除二级分类'
	Then yunying获得商品分类列表
		"""
		[{
			"categroy_name":"分类3"
		},{
			"categroy_name":"分类2"
		},{
			"categroy_name":"分类1"
		}]
		"""