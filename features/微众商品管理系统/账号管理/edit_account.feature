#_author_:张三香 2016.10.17

Feature:微众商品管理系统-账号管理-对账号进行不同操作（编辑、开启、关闭、删除）
	"""
		1.编辑'运营'账号时，除了'账号类型'和'登录名'不允许修改其他以下字段均可以被修改
			账号名称\登录密码\备注
		2.编辑'合作客户'类型账号（固定底价、零售价返点和首页55分成三种类型），除了'账号类型'和'登录名'不允许修改，其他以下字段均可被修改
			公司名称\店铺名称\采购方式\结算账期\经营类目\商品个数上限\联系人\手机号\有效期\登录密码\备注
		3.开启和关闭账号
			状态为'启用中'的账号操作列:编辑、关闭
			状态为'已关闭'的账号操作列:开启、删除
				账号有效期未过期，点击【开启】，弹窗提示"确认开启该账号吗？"，点击【确定】后账号开启，点击【取消】弹窗关闭账号不开启
				账号有效期已过期，点击【开启】，调转到账号编辑页面，通过修改账号的有效期来改变账号的状态
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

Scenario:1 管理员编辑运营账号
	Given manager登录商品管理系统
	When manager编辑账号'yunying'
		"""
		{
			"type":"运营",
			"account_name":"运营账号1修改",
			"login_name":"yunying",
			"login_password":"test1",
			"remark":"账号备注信息修改"
		}
		"""
	Then manager获得账号"yunying"
		"""
		{
			"type":"运营",
			"account_name":"运营账号1修改",
			"login_name":"yunying",
			"login_password":"test1",
			"remark":"账号备注信息修改"
		}
		"""
	And manager获得账号管理列表
		"""
		[{
			"shop_name":"首月55分成店铺"
		},{
			"shop_name":"零售价返点店铺"
		},{
			"shop_name":"固定底价店铺"
		},{
			"shop_name":"运营账号1修改",
			"business_name":"",
			"customer_from":"--",
			"login_name":"yunying",
			"create_time":"2016-10-10 09:00:00",
			"product_category":["--"],
			"purchase_way":"--",
			"products_limit":"--",
			"actions":["编辑","关闭"]
		}]
		"""

Scenario:2 管理员编辑合作客户账号
	Given manager登录商品管理系统
	#编辑'固定底价'类型客户
	When manager编辑账号'gddj'
		"""
		{
			"type":"合作客户",
			"business_name":"北京大公司1修改",
			"shop_name":"固定底价店铺修改",
			"purchase_way":"固定底价",
			"payment_type":"15天",
			"product_category":["食品"],
			"products_limit":30,
			"contact_name":"张张",
			"mobile":"18511223344",
			"start_time":"2016-10-10 10:00",
			"end_time":"2026-12-30 10:00",
			"login_name":"gddj",
			"login_password":"test1",
			"remark":"固定底价客户备注信息修"
		}
		"""
	Then manager获得账号'gddj'
		"""
		{
			"type":"合作客户",
			"business_name":"北京大公司1修改",
			"shop_name":"固定底价店铺修改",
			"purchase_way":"固定底价",
			"payment_type":"15天",
			"product_category":["食品"],
			"products_limit":30,
			"contact_name":"张张",
			"mobile":"18511223344",
			"start_time":"2016-10-10 10:00",
			"end_time":"2026-12-30 10:00",
			"login_name":"gddj",
			"login_password":"test1",
			"remark":"固定底价客户备注信息修"
		}
		"""
	#编辑'零售价返点'客户
	When manager编辑账号'lsjfd'
		"""
		{
			"type":"合作客户",
			"business_name":"北京大公司2修改",
			"shop_name":"零售价返点店铺修改",
			"purchase_way":"零售价返点",
			"points":"30",
			"payment_type":"自然月",
			"product_category":["服装","户外运动"],
			"products_limit":100,
			"contact_name":"张小",
			"mobile":"13211223344",
			"start_time":"2016-10-11 10:00",
			"end_time":"2026-12-30 11:00",
			"login_name":"lsjfd",
			"login_password":"test1",
			"remark":"零售价返点客户备注信息修改"
		}
		"""
	Then manager获得账号'lsjfd'
		"""
		{
			"type":"合作客户",
			"business_name":"北京大公司2修改",
			"shop_name":"零售价返点店铺修改",
			"purchase_way":"零售价返点",
			"points":"30",
			"payment_type":"自然月",
			"product_category":["服装","户外运动"],
			"products_limit":100,
			"contact_name":"张小",
			"mobile":"13211223344",
			"start_time":"2016-10-11 10:00",
			"end_time":"2026-12-30 11:00",
			"login_name":"lsjfd",
			"login_password":"test1",
			"remark":"零售价返点客户备注信息修改"
		}
		"""
	#编辑'首月55分成'客户
	When manager编辑账号'syfc'
		"""
		{
			"type":"合作客户",
			"business_name":"北京大公司3修改",
			"shop_name":"首月55分成店铺修改",
			"purchase_way":"首月55分成",
			"conditions":
				{
					"first_month_money":2000.00,
					"points":55,
					"other_points":25
				},
			"payment_type":"15天",
			"product_category":["食品","户外运动"],
			"products_limit":200,
			"contact_name":"张明",
			"mobile":"13811223344",
			"start_time":"2016-10-12 10:00",
			"end_time":"2026-12-30 10:00",
			"login_name":"syfc",
			"login_password":"test1",
			"remark":"零售价返点客户备注信息修改"
		}
		"""
	Then manager获得账号'syfc'
		"""
		{
			"type":"合作客户",
			"business_name":"北京大公司3修改",
			"shop_name":"首月55分成店铺修改",
			"purchase_way":"首月55分成",
			"conditions":
				{
					"first_month_money":2000.00,
					"points":55,
					"other_points":25
				},
			"payment_type":"15天",
			"product_category":["食品","户外运动"],
			"products_limit":200,
			"contact_name":"张明",
			"mobile":"13811223344",
			"start_time":"2016-10-12 10:00",
			"end_time":"2026-12-30 10:00",
			"login_name":"syfc",
			"login_password":"test1",
			"remark":"零售价返点客户备注信息修改"
		}
		"""
	And manager获得账号管理列表
		"""
		[{
			"shop_name":"首月55分成店铺修改",
			"business_name":"北京大公司3修改",
			"customer_from":"--",
			"login_name":"syfc",
			"create_time":"2016-10-12 09:00:00",
			"product_category":["食品","户外运动"],
			"purchase_way":"首月55分成",
			"products_limit":"200",
			"actions":["编辑","关闭"]
		},{
			"shop_name":"零售价返点店铺修改",
			"business_name":"北京大公司2修改",
			"customer_from":"--",
			"login_name":"lsjfd",
			"create_time":"2016-10-11 09:00:00",
			"product_category":["服装","户外运动"],
			"purchase_way":"零售价返点",
			"products_limit":"100",
			"actions":["编辑","关闭"]
		},{
			"shop_name":"固定底价店铺修改",
			"business_name":"北京大公司1修改",
			"customer_from":"--",
			"login_name":"gddj",
			"create_time":"2016-10-10 09:00:00",
			"product_category":["食品"],
			"purchase_way":"固定底价",
			"products_limit":"30",
			"actions":["编辑","关闭"]
		},{
			"shop_name":"运营账号1",
			"business_name":"",
			"customer_from":"--",
			"login_name":"yunying",
			"create_time":"2016-10-10 09:00:00",
			"product_category":["--"],
			"purchase_way":"--",
			"products_limit":"--",
			"actions":["编辑","关闭"]
		}]
		"""

Scenario:3 管理员开启或关闭账号
	Given manager登录商品管理系统
	When manager'关闭'账号'yunying'
	When manager'关闭'账号'syfc'
	Then manager获得账号管理列表
		"""
		[{
			"shop_name":"首月55分成店铺",
			"login_name":"syfc",
			"actions":["开启","删除"]
		},{
			"shop_name":"零售价返点店铺",
			"login_name":"lsjfd",
			"actions":["编辑","关闭"]
		},{
			"shop_name":"固定底价店铺",
			"login_name":"gddj",
			"actions":["编辑","关闭"]
		},{
			"shop_name":"运营账号1",
			"login_name":"yunying",
			"actions":["开启","删除"]
		}]
		"""
	When manager'开启'账号'syfc'
	Then manager获得账号管理列表
		"""
		[{
			"shop_name":"首月55分成店铺",
			"login_name":"syfc",
			"actions":["编辑","关闭"]
		},{
			"shop_name":"零售价返点店铺",
			"login_name":"lsjfd",
			"actions":["编辑","关闭"]
		},{
			"shop_name":"固定底价店铺",
			"login_name":"gddj",
			"actions":["编辑","关闭"]
		},{
			"shop_name":"运营账号1",
			"login_name":"yunying",
			"actions":["开启","删除"]
		}]
		"""

Scenario:4 管理员删除账号
	Given manager登录商品管理系统
	Then manager获得账号管理列表
		"""
		[{
			"shop_name":"首月55分成店铺",
			"login_name":"syfc",
			"actions":["编辑","关闭"]
		},{
			"shop_name":"零售价返点店铺",
			"login_name":"lsjfd",
			"actions":["编辑","关闭"]
		},{
			"shop_name":"固定底价店铺",
			"login_name":"gddj",
			"actions":["编辑","关闭"]
		},{
			"shop_name":"运营账号1",
			"login_name":"yunying",
			"actions":["编辑","关闭"]
		}]
		"""
	When manager'关闭'账号'yunying'
	When manager'关闭'账号'syfc'
	When manager删除账号'yunying'
	When manager删除账号'syfc'
	Then manager获得账号管理列表
		"""
		[{
			"shop_name":"零售价返点店铺",
			"login_name":"lsjfd",
			"actions":["编辑","关闭"]
		},{
			"shop_name":"固定底价店铺",
			"login_name":"gddj",
			"actions":["编辑","关闭"]
		}]
		"""