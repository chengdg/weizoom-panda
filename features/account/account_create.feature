#author: 张雪 2016-5-6
#editor: 徐梓豪  新增团购返点账号

Feature:精简版云商通-创建合作客户、代理商、运营账号
"""
	1.管理员创建固定底价账号
	2.管理员创建运营账号
	3.新增零售返点账号
	4.新增首月55分成账号
	


"""
#account_type   账号类型
#account_name   账号名称
#login_account  登录账号
#password       密码
#remarks        备注

Background:
	Given test22使用密码weizoom登录系统:axe
	When test22创建销售
	"""
	{
	"sale_name":"爱伲咖啡",
	"connect_way":"13813984485"
	}
	"""

	Then test22新建客户
	"""
	{
	"costumer_name":"爱伲咖啡",
	"agent":"test22",
	"sales":"爱伲咖啡",
	"area":"南京",
	"business_license":"国家安全许可证",
	"connect_man":"爱伲",
	"tel":"025-85341268",
	"mobile":"13813984402",
	"email":"1414102598@qq.com",
	"address":"南京市玄武区湖南路224号",
	"main_product":"咖啡豆"
	}
	"""

@panda @account_create
Scenario:1  管理员创建固定底价账号
	Given jobs登录管理系统
	When jobs添加账号
	"""
	{
		account_type":"体验客户",
		"company_name":"爱昵咖啡有限责任公司",
		"shop_name":"爱昵咖啡",
		"purchase_type":"固定底价",
		"settlement_time":"15天",
		"manage_type":"零食"
		"connect_man":"aini",
		"mobile_number":"13813985506",
		"valid_time":"2016-07-15"至"2017-07-15",
		"login_account":"aini",
		"password":"123456",
		"ramarks":"爱昵咖啡客户体验账号"
	}
	"""



@panda @account_create
Scenario:2  管理员创建运营账号
	Given jobs登录管理系统
	When jobs添加账号
	"""
		[{
			"account_type":"运营",
			"account_name":"运营部门",
			"login_account":"yunying",
			"password":"123456",
			"ramarks":"运营部门"
		},{
			"account_type":"代理商",
			"account_name":"代理商公司",
			"login_account":"daili",
			"password":"123456",
			"ramarks":"代理商有限公司"
		},{
			"account_type":"合作客户",
			"account_name":"爱昵咖啡",
			"login_account":"aini",
			"password":"123456",
			"ramarks":"爱昵咖啡客户体验账号"
		}]
	"""
	Then jobs能获得账号管理列表
	"""
		[{
			"account_name":"爱昵咖啡",
			"login_account":"aini",
			"actions": ["编辑","关闭"]
		},{
			"account_name":"代理商公司",
			"login_account":"daili",
			"actions": ["编辑","关闭"]
		},{
			"account_name":"运营部门",
			"login_account":"yunying",
			"actions": ["编辑","关闭"]
		}]
	"""
@panda @account_create
Scenario:3  新增零售返点账号
	Given manager登录管理系统
	When manager添加账号
		"""
		{
			account_type":"体验客户",
			"company_name":"爱昵咖啡有限责任公司",
			"shop_name":"爱昵咖啡",
			"manage_type":"休闲食品",
			"purchase_type":"零售价返点",
			"purchase_promotin":"5.00",
			"settlement_time":"15天",
			"type":"零食"
			"connect_man":"aini",
			"mobile_number":"13813985506",
			"valid_time":"2016-07-15"至"2017-07-15",
			"login_account":"aini",
			"password":"123456",
			"ramarks":"爱昵咖啡客户体验账号"
		}
		"""

@panda @account_create
Scenario:4  新增首月55分成账号
	Given manager登录管理系统
	When manager添加账号
	"""
	[{
	"account_type":"体验客户",
	"company_name":"爱昵咖啡有限责任公司",
	"shop_name":"爱昵咖啡",
	"manage_type":"休闲食品",
	"purchase_type":{
				"首月55分成",
				"首月(商品上架30天含内)或金额不大于"3000"时,返点比例为50%,否则按5%基础扣点结算"
				},
	"connect_man":"aini",
	"mobile_number":"13813985506",
	"login_account":"aini",
	"password":"123456",
	"valid_time":"2016-07-15"至"2017-07-15",
	"settlement_time":"15天",
	"ramarks":"爱昵咖啡客户体验账号"
	}]
	"""

	When manager编辑'爱伲咖啡'使之含有多个条件的首月55分成账号
	"""
	[{
	"account_type":"体验客户",
	"company_name":"爱昵咖啡有限责任公司",
	"shop_name":"爱昵咖啡",
	"manage_type":"休闲食品",
	"purchase_type":{
				"首月55分成",
				"首月(商品上架30天含内)或金额不大于"3000"时,返点比例为50%,否则按5%基础扣点结算"		
				},
	"connect_man":"aini",
	"mobile_number":"13813985506",
	"login_account":"aini",
	"password":"123456",
	"valid_time":"2016-07-15"至"2017-07-15",
	"settlement_time":"15天",
	"ramarks":"爱昵咖啡客户体验账号"
	}]
	"""

	Then manager删除'爱伲咖啡'中'首月55分成'的一个条件
	"""
	[
	"purchase_type":"周期'2016-07-03 00:00'-'2017-07-03 00:00'或金额不大于"3000"时,返点比例为50%,否则按5%基础扣点结算"
	]
	"""
	Then manager查看'爱伲咖啡'的账号详情
	"""
	[{
	"account_type":"体验客户",
	"company_name":"爱昵咖啡有限责任公司",
	"shop_name":"爱昵咖啡",
	"manage_type":"休闲食品",
	"purchase_type":{
				"首月55分成",
				"首月(商品上架30天含内)或金额不大于"3000"时,返点比例为50%,否则按5%基础扣点结算",
				},
	"connect_man":"aini",
	"mobile_number":"13813985506",
	"login_account":"aini",
	"password":"123456",
	"valid_time":"2016-07-15"至"2017-07-15",
	"settlement_time":"15天",
	"ramarks":"爱昵咖啡客户体验账号"
	}]


