#auther:徐梓豪 2016-08-12
Feature:客户账号修改密码
	#旧密码必须与目前密码相同
	#要输入两次新密码，并且新密码必须相同
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
		[{
		"account_type":"体验客户",
		"product_style":{
						"电子数码"，
						"生活用品"
						},
		"business_limit":"5.00",
		"company_name":"周黑鸭",
		"shop_name":"周黑鸭旗舰店",
		"purchase_type":"固定底价",
		"connect_man":"周黑鸭",
		"mobile_number":"13813985507",
		"login_account":"zhouheiya",
		"password":"123456",
		"valid_time":"2016-07-15"至"2017-07-15",
		"ramarks":"周黑鸭"
		},{
		"account_type":"体验客户",
		"purchase_type":{
						"电子数码"，
						"生活用品"
						},
		"business_limit":"6.00",
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
		}]
		"""	
@panda @password
Scenario:客户账号修改密码
	Given aini使用密码123456登录系统
	When aini修改密码
		"""
		{
		"old_password":123456,
		"new_password":654321,
		"again_password":654321,
		}
		"""
	Given aini使用密码123456登录系统
	#无法登录
	Given aini使用密码654321登录系统
	#登录成功


