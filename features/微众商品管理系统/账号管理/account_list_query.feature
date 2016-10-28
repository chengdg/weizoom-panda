#_author_:张三香 2016.10.17

Feature:微众商品管理系统-账号管理列表查询
	"""
		查询条件:
			公司名称:模糊查询
			登录名：模糊查询
			账号类型：包含全部、客户账号、运营账号，默认显示全部
			账号状态：包含全部、启用中、已关闭
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
	When manager'关闭'账号'yunying'

Scenario:1 账号管理列表查询-默认查询
	Given manager登录商品管理系统
	When manger设置账号管理列表查询条件
		"""
		{
			"business_name":"",
			"login_name":"",
			"type":"全部",
			"status":"全部"
		}
		"""
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
			"shop_name":"固定底价店铺修改",
			"login_name":"gddj",
			"actions":["编辑","关闭"]
		},{
			"shop_name":"运营账号1",
			"login_name":"yunying",
			"actions":["开启","删除"]
		}]
		"""

Scenario:2 账号管理列表查询-公司名称
	Given manager登录商品管理系统
	#模糊查询
	When manger设置账号管理列表查询条件
		"""
		{
			"business_name":"北京"
		}
		"""
	Then manager获得账号管理列表
		"""
		[{
			"business_name":"北京大公司3"
		},{
			"business_name":"北京大公司2"
		},{
			"business_name":"北京大公司1"
		}]
		"""
	#精确查询
	When manger设置账号管理列表查询条件
		"""
		{
			"business_name":"北京大公司3"
		}
		"""
	Then manager获得账号管理列表
		"""
		[{
			"business_name":"北京大公司3"
		}]
		"""
	#查询结果为空
	When manger设置账号管理列表查询条件
		"""
		{
			"business_name":"高级"
		}
		"""
	Then manager获得账号管理列表
		"""
		[]
		"""

Scenario:3 账号管理列表查询-登录名
	Given manager登录商品管理系统
	#模糊查询
	When manger设置账号管理列表查询条件
		"""
		{
			"login_name":"yun"
		}
		"""
	Then manager获得账号管理列表
		"""
		[{
			"login_name":"yunying"
		}]
		"""
	#精确查询
	When manger设置账号管理列表查询条件
		"""
		{
			"login_name":"gddj"
		}
		"""
	Then manager获得账号管理列表
		"""
		[{
			"login_name":"gddj"
		}]
		"""
	#查询结果为空
	When manger设置账号管理列表查询条件
		"""
		{
			"login_name":"11"
		}
		"""
	Then manager获得账号管理列表
		"""
		[]
		"""

Scenario:4 账号管理列表查询-账号类型
	Given manager登录商品管理系统
	#运营账号
	When manger设置账号管理列表查询条件
		"""
		{
			"type":"运营账号"
		}
		"""
	Then manager获得账号管理列表
		"""
		[{
			"shop_name":"运营账号1",
			"login_name":"yunying"
		}]
		"""
	#客户账号
		When manger设置账号管理列表查询条件
		"""
		{
			"type":"客户账号"
		}
		"""
	Then manager获得账号管理列表
		"""
		[{
			"shop_name":"首月55分成店铺",
			"login_name":"syfc"
		},{
			"shop_name":"零售价返点店铺",
			"login_name":"lsjfd"
		},{
			"shop_name":"固定底价店铺修改",
			"login_name":"gddj"
		}]
		"""

Scenario:5 账号管理列表查询-账号状态
	Given manager登录商品管理系统
	#启用中
	When manger设置账号管理列表查询条件
		"""
		{
			"status":"启用中"
		}
		"""
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
			"shop_name":"固定底价店铺修改",
			"login_name":"gddj",
			"actions":["编辑","关闭"]
		}]
		"""
	#已关闭
	When manger设置账号管理列表查询条件
		"""
		{
			"status":"已关闭"
		}
		"""
	Then manager获得账号管理列表
		"""
		[{
			"shop_name":"运营账号1",
			"login_name":"yunying",
			"actions":["开启","删除"]
		}]
		"""

Scenario:6 账号管理列表查询-组合查询
	Given manager登录商品管理系统
	When manger设置账号管理列表查询条件
		"""
		{
			"business_name":"北京大公司",
			"login_name":"lsjfd",
			"type":"客户账号",
			"status":"启用中"
		}
		"""
	Then manager获得账号管理列表
		"""
		[{
			"shop_name":"零售价返点店铺",
			"business_name":"北京大公司2",
			"login_name":"lsjfd",
			"actions":["编辑","关闭"]
		}]
		"""