#_author_:张三香 2016.10.18

Feature:固定底价客户在商品管理系统添加商品
	"""
		备注：固定底价客户添加商品页面隐藏'售价'字段，商品列表页中显示售价，其值默认和结算价相等
		1、点击【+添加新商品】按钮，显示'请选择商品分类'弹框，点击弹框中的【下一步，编辑商品】进入商品基本信息页面
		2、'请选择商品分类'弹窗中显示运营分配给该账号的所有一级分类和二级分类
		3、商品基本信息页面字段信息：
			商品类目：显示已选择的类目信息（格式：xx--xx 【修改】）
			商品名称：最多30个字
			促销标题：最多30个字（非必填）
			多规格商品：是/否
			【结算价】:填写商品的结算价（结算价与物流重量直接有内容'提示:结算价为商品与微众的结算价格，如无扣点约定，可与售价相同'）
			【物流重量】:填写商品的重量
			库存数量：填写商品库存数量
			发货地区设置：下拉框显示'无限制'、'仅发货地区'、'不发货地区'；
				当选择'仅发货地区'或'不发货地区'时，会多出字段'地区限制'，该字段下拉框中会显示‘禁售仅售模板’列表中添加的地区非空的所有模板名称，默认显示‘请选择区域’
			运费：'统一运费'/'使用默认运费模板:xxxx'；默认勾选的是'使用默认运费模板:xxxx',xxxx显示的是当前系统的默认运费模板名称
				勾选'统一运费'时，下方会显示字段'运费金额（元）'，该字段输入框中可以填写统一运费的值
			提示：需要更换模板，请前往运费模板列表中将需要的模板设置为默认模板即可。
			商品图片：【+上传图片】按钮（按钮下方内容'提示:商品轮播图最多6张，200KB以内，建议640-960之间的正方形图片，web格式图片'）
			商品描述：富文本框显示，允许输入文字、添加图片等（富文本编辑框上方有内容'提示:商品详情描述的图片宽度640-960px之间，高度建议＜500px，大小300KB以内，web格式图片'）
		4、商品列表字段信息
			商品信息：显示商品图片和名称
			分类：显示商品的分类
			售价（元）：显示商品的售价，默认和结算价相同（保留2位小数）
			结算价（元）：显示商品的结算价（保留2位小数）
			销量：商品的销量
			库存：显示商品的库存（当库存小于20时红色字体显示）
			创建时间：商品的创建时间（格式为xxxx-xx-xx xx:xx）
			入库状态：待入库（运营未同步）/已入库（运营已同步）/已驳回（红字显示并且鼠标悬停?时，显示驳回记录详情）
			销售状态：未上架/已上架
			操作:【编辑】
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

	Given manager登录商品管理系统
	#添加'固定底价'类型客户
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
	#gdgj添加运费模板
		When ggdj添加运费模板
			"""
			{
				"name":"运费模板1",
				"first_weight":1.0,
				"first_weight_price": 1.00,
				"added_weight":1.0,
				"added_weight_price": 1.00
			}
			"""
		When ggdj添加运费模板
			"""
			{
				"name": "运费模板2",
				"first_weight": 1.0,
				"first_weight_price": 1.00,
				"added_weight": 1.0,
				"added_weight_price": 1.00,
				"special_area": [{
					"to_the": ["北京市"],
					"first_weight": 1.0,
					"first_weight_price": 2.00,
					"added_weight": 1.0,
					"added_weight_price": 2.00
					}],
				"free_postages": [{
					"to_the": ["上海市"],
					"condition":"count",
					"value": 1
				},{
					"to_the": ["北京市","重庆市","江苏省"],
					"condition":"money",
					"value": 20.0
				}]
			}
			"""
	#gddj添加禁售仅售模板
		When gddj添加禁售仅售模板
			"""
			{
				"name": "禁售仅售模板1",
				"limit_area":
					[{
						"province": "河北省",
						"is_select_all":false,
						"city":["秦皇岛市","唐山市","沧州市"]
					},{
						"province": "山西省",
						"is_select_all":true
					}]
			}
			"""
		When gddj添加禁售仅售模板
			"""
			{
				"name": "禁售仅售模板2",
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
	#添加商品规格
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

Scenario:1 固定底价客户添加无规格商品（统一运费、发货设置无限制）
	Given gddj登录商品管理系统
	Then gddj获得客户端商品列表
		"""
		[]
		"""
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
			"detail": "商品1描述信息",
			"create_time":"2016-10-18 08:00"
		}
		"""
	Then gddj获得客户端商品列表
		"""
		[{
			"product_info":
				{
					"name":"商品1",
					"image":"love.png"
				},
			"product_category":"食品-饼干",
			"price":"10.00",
			"purchase_price":"10.00",
			"sales":0,
			"stocks":"100",
			"create_time":"2016-10-18 08:00",
			"storage_status":"待入库",
			"sale_status":"未上架",
			"actions":["编辑"]
		}]
		"""

Scenario:2 固定底价客户添加多规格商品（模板运费、发货设置禁售或仅售）
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
			"limit_zone_type":"仅发货地区",
			"limit_zone_template":"禁售仅售模板1",
			"postage":"运费模板1",
			"image":["love.png"],
			"detail": "商品1描述信息",
			"create_time":"2016-10-18 08:00"
		}
		"""
	When gddj添加商品
		"""
		{
			"product_category":"食品-泡面",
			"name":"商品2",
			"promotion_title":"促销标题2",
			"is_enable_model":true,
			"model": {
				"models": {
					"黑色": {
						"purchase_price": 20.00,
						"weight":2.0,
						"stocks":200
						}
					}
				},
			"limit_zone_type":"不发货地区",
			"limit_zone_template":"禁售仅售模板2",
			"postage":"运费模板2",
			"image":["love.png"],
			"detail": "商品2描述信息",
			"create_time":"2016-10-18 09:00"
		}
		"""
	Then gddj获得客户端商品列表
		"""
		[{
			"product_info":
				{
					"name":"商品2",
					"image":"love.png"
				},
			"product_category":"食品-泡面",
			"price":"20.00",
			"purchase_price":"20.00",
			"sales":0,
			"stocks":"200",
			"create_time":"2016-10-18 09:00",
			"storage_status":"待入库",
			"sale_status":"未上架",
			"actions":["编辑"]
		},{
				"product_info":
				{
					"name":"商品1",
					"image":"love.png"
				},
			"product_category":"食品-饼干",
			"price":"10.00-20.00",
			"purchase_price":"10.00~20.00",
			"sales":0,
			"stocks":"100~200",
			"create_time":"2016-10-18 08:00",
			"storage_status":"待入库",
			"sale_status":"未上架",
			"actions":["编辑"]
		}]
		"""

