#_author_:张三香 2016.10.13

Feature:微众商品管理系统-账号管理-添加账号
	"""
		0.manager可以添加两种类型的账号：合作客户和运营
		1.添加'运营'账号时，添加页面显示以下字段信息
			账号类型\账号名称\登录名\登录密码\备注
		2.添加'合作客户'类型账号时，有固定底价、零售价返点和首页55分成三种类型的客户:
				账号类型:合作客户,运营
				公司名称:客户的公司名称
				店铺名称:客户的店铺名称
				采购方式:有固定底价、零售价返点、首页55分成三种类型
					a.默认选择的是"零售价返点"，显示'零售扣点'字段
					b.选择'固定底价'类型时，零售扣点字段消失
					c.选择'首页55分成'类型时，会显示【首页（商品上架后30天含内）或金额不大于x元前提下，返点比例为x%,否则，将按x%基础扣点结】,其中x在界面中显示的是输入框
				结算账期:自然月、15天、自然周（默认选中'自然月'）
				经营类目:显示运营账号下所创建的所有一级商品分类
				商品个数上限：默认显示3
				联系人:客户的联系人
				手机号:客户的手机号
				有效期:客户账号的有效期
				登录名:客户的登录名
				登录密码:设置登录密码
				备注:备注信息（非必填）
		3.账号管理列表字段信息
			店铺名称:运营账号显示创建时设置的账号名称，客户账号显示创建时填写的店铺名称
			公司名称:显示创建时填写的公司名称信息
			客户来源:运营账号显示"--",客户账号显示？？
			登录名:显示账号的登录名称
			创建时间:显示账号的创建时间，格式为xxxx-xx-xx xx:xx:xx
			经营类目:运营账号显示"--",客户账号显示创建时勾选的经营类目信息
			采购方式:运营账号显示"--",客户账号显示创建时勾选的类型（'固定底价'或'零售价返点'或'首月55分成'）
			商品数上限:运营账号显示"--",客户账号显示创建时设置的商品上限数
			操作:【编辑】,【关闭】或【开启】,【删除】
	"""

Scenario:1 管理员添加运营账号
	Given manager登录商品管理系统
	Then manager获得账号管理列表
		"""
		[]
		"""
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
	Then manager获得账号管理列表
		"""
		[{
			"shop_name":"运营账号1",
			"business_name":"",
			"customer_from":"--",
			"login_name":"yunying",
			"create_time":"2016-10-10 09:00:00",
			"product_category":"--",
			"purchase_way":"--",
			"products_limit":"--",
			"actions":["编辑","关闭"]
		}]
		"""

Scenario:2 管理员添加合作客户账号
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
	When yunying添加商品分类
		"""
		{
			"服装":
			[{
				"name":"男装"
			},{
				"name":"女装"
			}]
		}
		"""
	When yunying添加商品分类
		"""
		{
			"户外运动":[]
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
			"product_category":["食品","服装"],
			"products_limit":3,
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
			"product_category":["服装"],
			"products_limit":30,
			"contact_name":"张小小",
			"mobile":"13511223344",
			"start_time":"2016-10-11 10:00",
			"end_time":"2026-10-10 11:00",
			"login_name":"lsjfd",
			"login_password":"test",
			"remark":"零售价返点客户备注信息",
			"create_time":"2016-10-11 09:00:00"
		}
		"""
	#添加'首月55分成'类型客户
	When manager添加账号
		"""
		{
			"type":"合作客户",
			"business_name":"北京大公司3",
			"shop_name":"首月55分成店铺",
			"purchase_way":"首月55分成",
			"conditions":
				{
					"first_month_money":1000.00,
					"points":50,
					"other_points":20
				},
			"payment_type":"自然周",
			"product_category":["户外运动"],
			"products_limit":300,
			"contact_name":"张小明",
			"mobile":"13611223344",
			"start_time":"2016-10-12 10:00",
			"end_time":"2026-10-12 10:00",
			"login_name":"syfc",
			"login_password":"test",
			"remark":"零售价返点客户备注信息",
			"create_time":"2016-10-12 09:00:00"
		}
		"""
	Then manager获得账号管理列表
		"""
		[{
			"shop_name":"首月55分成店铺",
			"business_name":"北京大公司3",
			"customer_from":"--",
			"login_name":"syfc",
			"create_time":"2016-10-12 09:00:00",
			"product_category":["户外运动"],
			"purchase_way":"首月55分成",
			"products_limit":"300",
			"actions":["编辑","关闭"]
		},{
			"shop_name":"零售价返点店铺",
			"business_name":"北京大公司2",
			"customer_from":"--",
			"login_name":"lsjfd",
			"create_time":"2016-10-11 09:00:00",
			"product_category":["服装"],
			"purchase_way":"零售价返点",
			"products_limit":"30",
			"actions":["编辑","关闭"]
		},{
			"shop_name":"固定底价店铺",
			"business_name":"北京大公司1",
			"customer_from":"--",
			"login_name":"gddj",
			"create_time":"2016-10-10 09:00:00",
			"product_category":["食品","服装"],
			"purchase_way":"固定底价",
			"products_limit":"3",
			"actions":["编辑","关闭"]
		}]
		"""