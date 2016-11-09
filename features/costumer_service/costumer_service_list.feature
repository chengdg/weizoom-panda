#_author_:徐梓豪 2016-11-09
Feature:客户端查看自己对应的客服
	#进入账号后，在线客服模块默认为收起状态
Background:
	Given manager登录管理系统
	When manager添加账号
		"""
		{
			"account_type":"运营",
			"account_name":"运营部门",
			"login_account":"yunying",
			"password":123456,
			"ramarks":"运营部门"
		}
		"""
	Given yunying登录系统
	When yunying添加分类
		"""
		{
		"head_classify":"无",
		"classify_name":"电子数码",
		"comments":"1"
		},{
		"head_classify":"无",
		"classify_name":"生活用品",
		"comments":"1"
		},{
		"head_classify":"电子数码",
		"classify_name":"手机",
		"comments":""
		},{
		"head_classify":"电子数码",
		"classify_name":"平板电脑",
		"comments":""
		},{
		"head_classify":"电子数码",
		"classify_name":"耳机",
		"comments":""
		},{
		"head_classify":"生活用品",
		"classify_name":"零食",
		"comments":""
		},{
		"head_classify":"生活用品",
		"classify_name":"肥皂",
		"comments":""
		},{
		"head_classify":"生活用品",
		"classify_name":"清洗用品,
		"comments":""
		}
		"""
	Given manager登录管理系统
	When manager添加账号
		"""
		{
		"account_type":"体验客户",
		'product_style':{
						"电子数码"，
						"生活用品"
						},
		"company_name":"爱昵咖啡有限责任公司",
		"shop_name":"爱昵咖啡",
		"purchase_type":"固定底价",
		"connect_man":"aini",
		"mobile_number":"13813985506",
		"login_account":"aini",
		"password":"123456",
		"valid_time":"2016-07-15"至"2017-07-15",
		"ramarks":"爱昵咖啡客户体验账号",
		"costumer_service_telphone":13813984402,
		"costumer_service_qq1":445068326,
		"costumer_service_qq2":1417102986
		},{
		"account_type":"体验客户",
		'product_style':{
						"电子数码"，
						"耳机"
						},
		"company_name":"土小宝食品有限公司",
		"shop_name":"土小宝食品",
		"purchase_type":"固定底价",
		"connect_man":"tuxiaobao",
		"mobile_number":"13813985506",
		"login_account":"aini",
		"password":"123456",
		"valid_time":"2016-07-15"至"2017-07-15",
		"ramarks":"土小宝客户体验账号",
		"costumer_service_telphone":15951921193,
		"costumer_service_qq1":445068326,
		"costumer_service_qq2":1417102986
		}
		"""	
@panda @costumer_service
Scenario:1 客户端查看自己对应的客服
	Given aini登录系统
	When aini查看自己的在线客服
		"""
		[{
			"qq_service":"445068326",
			"costumer_service_telphone":13813984402
		}]
		"""

	Given tuxiaobao登录系统
	When tuxiaobao查看自己的在线客服
		"""
		[{
			"qq_service":"445068326",
			"costumer_service_telphone":15951921193
		}]
		"""