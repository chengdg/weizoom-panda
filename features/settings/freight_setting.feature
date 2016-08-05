#auther 徐梓豪 2016.08.04
Feature:客户端设置运费

Background:
	Given manager登录管理系统
	Then manager添加账号
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
		}]
	"""
@panda @hj
Scenario:1 客户端设置运费
	Given aini登录系统
	When aini进入运费设置页面
	Then aini设置运费
	"""
	{
	"door_price":"5.00"
	}
	"""