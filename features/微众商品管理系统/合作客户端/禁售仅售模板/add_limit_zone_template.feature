#_author_:张三香 2016.10.17

Feature:添加禁售仅售模板
	"""
		客户端用户可以添加禁售仅售模板
		允许添加地区为空的禁售禁售模板，该模板不会显示在添加商品页面'地区限制'下拉框中
		禁售仅售模板列表字段：
			模板名称：显示创建时的模板名称
			地区：按添加顺序正序显示,格式如下显示
					北京市:全选
					河北省:石家庄市,秦皇岛市
					山西省:全选
					香港特别行政区:全选
			操作:【修改】、【删除】
		删除禁售禁售模板：
			该模板未被商品使用，点击【删除】按钮，提示"确认删除吗？ 确认 取消"，点击【确认】后模板删除
			该模板在被商品使用，点击【删除】按钮，提示"确认删除吗？ 确认 取消"，点击【确认】页面上方红条提示'还有正在使用该模板的商品，请先处理！'
		禁售仅售列表顺序：添加时间正序显示

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

Scenario:1 添加禁售仅售模板
	Given gddj登录商品管理系统
	Then gddj获得禁售仅售模板列表
		"""
		[]
		"""
	When gddj添加禁售仅售模板
		"""
		{
			"name": "空模板1",
			"limit_area":[]
		}
		"""
	When gddj添加禁售仅售模板
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
	Then gddj获得禁售仅售模板列表
		"""
		[{
			"name":"空模板1",
			"area_info":[]
		},{
			"name":"非空模板2",
			"area_info":["河北省:秦皇岛市,唐山市,沧州市","山西省:全选","北京市:全选","香港特别行政区:全选"]
		}]
		"""


