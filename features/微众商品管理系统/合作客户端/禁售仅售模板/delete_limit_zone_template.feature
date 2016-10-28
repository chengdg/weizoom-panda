#_author_:张三香 2016.10.18

Feature:删除禁售仅售模板
	"""
		客户端用户可以删除禁售仅售模板
		用户'删除'禁售禁售模板:
			该模板未被商品使用，点击【删除】按钮，弹出提示"确认删除吗？ 确定 取消"，点击【确定】后该模板删除，点击【取消】确认弹窗关闭
			该模板在被商品使用，点击【删除】按钮，弹出提示"确认删除吗？ 确定 取消"，点击【确定】后页面上方红条提示'还有正在使用该模板的商品，请先处理！'，点击【取消】确认弹窗关闭
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
	When gddj修改禁售仅售模板'非空模板2'
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

Scenario:1 删除禁售仅售模板-未被使用
	Given gddj登录商品管理系统
	When gddj删除禁售仅售模板'空模板1'
	Then gddj获得禁售仅售模板列表
		"""
		[{
			"name":"非空模板2",
			"area_info":["河北省:秦皇岛市,唐山市,沧州市","山西省:全选","北京市:全选","香港特别行政区:全选"]
		}]
		"""
	When gddj删除禁售仅售模板'非空模板2'
	Then gddj获得禁售仅售模板列表
		"""
		[]
		"""

Scenario:2 删除禁售禁售模板-正被使用
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
	When gddj删除禁售仅售模板'非空模板2'
	Then gddj获得提示信息'还有正在使用该模板的商品，请先处理！'