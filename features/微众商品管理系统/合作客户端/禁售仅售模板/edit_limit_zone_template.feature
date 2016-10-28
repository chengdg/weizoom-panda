#_author_:张三香 2016.10.17

Feature:修改禁售仅售模板
	"""
		客户端用户可以修改禁售仅售模板
		点击模板列表中'操作'列的【修改】按钮,弹出'禁售/仅售模板'弹框，允许用户修改模板名称
		点击模板列表中'地区'列的【选择地区】按钮,弹出'选择区域'弹框，允许用户修改模板的地区信息
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
	When gddj添加禁售仅售模板
		"""
		{
			"name": "空模板1",
			"limit_area":[]
		}
		"""
	When gddj添加禁售仅售模板'非空模板2'
		"""
		{
			"name": "非空模板2",
			"limit_area":
				[{
					"province": "河北省",
					"is_select_all":false,
					"city":["秦皇岛市","唐山市","沧州市"]
				},{
					"province": "山西省",
					"is_select_all":true
				},{
					"province": "北京市",
					"is_select_all":true
				},{
					"province": "香港特别行政区",
					"is_select_all":true
				}]
		}
		"""

Scenario:1 修改禁售仅售模板（未被使用）
	Given gddj登录商品管理系统
	When gddj修改禁售仅售模板'空模板1'的模板名称为
		"""
		{
			"name": "空模板1修改"
		}
		"""
	When gddj修改禁售仅售模板'空模板1修改'的地区为
		"""
		{
			"limit_area":
				[{
					"province": "河北省",
					"is_select_all":true
				},{
					"province": "北京市",
					"is_select_all":true
				}]
		}
		"""

	When gddj修改禁售仅售模板'非空模板2'的地区为
		"""
		{
			"name": "非空模板2",
			"limit_area":
				[{
					"province": "河北省",
					"is_select_all":false,
					"city":["秦皇岛市","唐山市"]
				},{
					"province": "山西省",
					"is_select_all":true
				},{
					"province": "北京市",
					"is_select_all":true
				}]
		}
		"""

	Then gddj获得禁售仅售模板列表
		"""
		[{
			"name":"空模板1修改",
			"area_info":["河北省:全选","北京市:全选"]
		},{
			"name":"非空模板2",
			"area_info":["河北省:秦皇岛市,唐山市","山西省:全选","北京市:全选"]
		}]
		"""

Scenario:2 修改禁售仅售模板（在被使用）
	Given gddj登录商品管理系统
	#添加禁售商品1-非空模板2
	When gddj添加商品
		"""
		{
			"product_category":"食品-饼干"
			"name":"禁售商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":false,
			"purchase_price": 10.00,
			"weight": 1,
			"stocks": 100,
			"limit_zone_type":"不发货地区",
			"limit_zone_template":"非空模板2",
			"postage":1.00,
			"image":["love.png"],
			"detail": "商品1描述信息"
		}
		"""
	When gddj修改禁售仅售模板'非空模板2'的模板名称为
		"""
		{
			"name": "非空模板2修改"
		}
		"""
	When gddj修改禁售仅售模板'非空模板2修改'的地区为
		"""
		{
			"name": "非空模板2修改",
			"limit_area":
				[{
					"province": "河北省",
					"is_select_all":false,
					"city":["秦皇岛市","唐山市"]
				},{
					"province": "山西省",
					"is_select_all":true
				},{
					"province": "北京市",
					"is_select_all":true
				}]
		}
		"""
	Then gddj获得禁售仅售模板列表
		"""
		[{
			"name":"空模板1",
			"area_info":[]
		},{
			"name":"非空模板2修改",
			"area_info":["河北省:秦皇岛市,唐山市","山西省:全选","北京市:全选"]
		}]
		"""
	Then gddj获得商品'禁售商品1'
		"""
		{
			"product_category":"食品-饼干"
			"name":"禁售商品1",
			"promotion_title":"促销标题1",
			"is_enable_model":false,
			"purchase_price": 10.00,
			"weight": 1,
			"stocks": 100,
			"limit_zone_type":"不发货地区",
			"limit_zone_template":"非空模板2修改",
			"postage":1.00,
			"image":["love.png"],
			"detail": "商品1描述信息"
		}
		"""