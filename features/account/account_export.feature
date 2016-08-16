auther:徐梓豪 2016-08-12
Feature:管理员导出账号列表

Background:
	"""
		[{
		"account_type":"体验客户",
		"company_name":"爱昵咖啡有限责任公司",
		"shop_name":"爱昵咖啡",
		"manage_type":"休闲食品",
		"purchase_type":"固定底价",
		"connect_man":"aini",
		"mobile_number":"13813985506",
		"login_account":"aini",
		"password":"123456",
		"valid_time":"2016-07-15"至"2017-07-15",
		"ramarks":"爱昵咖啡客户体验账号"
		},{
		"account_type":"运营",
		"account_name":"运营部门",
		"login_account":"yunying",
		"password":123456,
		"ramarks":"运营部门"
		},{
		"account_type":"体验客户",
		"company_name":"零售价返点客户",
		"shop_name":"零售价返点商店",
		"manage_type":"休闲食品",
		"purchase_type":"零售价返点",
		purchase_promotin":"5.00",
		"group_purchase":{
						"weizoom_home":"4.00",
						"weizoom_mum":"3.00",
						"weizoom_baifumei":"1.00",
						"weizoom_club":"2.00",
						"weizoom_shop":"1.42",
						"weizoom_xuesheng":"1.64",
						"weizoom_life":"2.38",
						"weizoom_yijiaren":"4.56",
						"huihuilaila":"3.81"
		}",
		"connect_man":"零售价",
		"mobile_number":"13813985506",
		"login_account":"lingshou",
		"password":"123456",
		"valid_time":"2016-08-15"至"2017-07-15",
		"ramarks":"零售价客户账号"
		},{
		"account_type":"体验客户",
		"company_name":"首月55分成账号",
		"shop_name":"55分成",
		"manage_type":"休闲食品",
		"purchase_type":{
					"首月55分成",
					"首月(商品上架30天含内)或金额不大于"3000"时,返点比例为50%,否则按5%基础扣点结算"
					},
		"connect_man":"55分成",
		"mobile_number":"13813985506",
		"login_account":"fencheng",
		"password":"123456",
		"valid_time":"2016-07-15"至"2017-07-15",
		"ramarks":"爱昵咖啡客户体验账号"
		},{
		"account_type":"代理商",
		"account_name":"代理商",
		"login_account":"daili",
		"password":123456,
		"ramarks":"代理商"
		}]

@panda @account
Scenario:1 管理员账号导出账号列表
	Given manager登录系统
	When manager查看账号列表
	|    account_name    |login_account|purchase_type|account_type|
	|爱昵咖啡有限责任公司|     aini    |   固定底价  |  体验客户  |
	|     运营部门       |   yunying   |      --     |    运营    |
	|   零售价返点客户   |  lingshou   |  零售价返点 |  体验客户  |
	|   首月55分成账号   |  fencheng   |  首月55分成 |  体验客户  |
	|       代理商       |   daili     |      --     |   代理商   |
	Then manager导出账号列表
	|    account_name    |login_account|purchase_type|account_type|
	|爱昵咖啡有限责任公司|     aini    |   固定底价  |  体验客户  |
	|     运营部门       |   yunying   |      --     |    运营    |
	|   零售价返点客户   |  lingshou   |  零售价返点 |  体验客户  |
	|   首月55分成账号   |  fencheng   |  首月55分成 |  体验客户  |
	|       代理商       |   daili     |      --     |   代理商   |
