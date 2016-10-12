#author:徐梓豪 2016-10-12
Feature:运费模板列表页
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
		"manage_type":"休闲食品",
		"purchase_type":"固定底价",
		"connect_man":"aini",
		"mobile_number":"13813985506",
		"login_account":"aini",
		"password":"123456",
		"valid_time":"2016-07-15"至"2017-07-15",
		"ramarks":"爱昵咖啡客户体验账号"
		}
		"""	

	Given aini登录系统：panda
	When aini创建运费模板
		"""
		[{
		"moudle_name":"测试模板1",
		"freight_style":"默认运费",
		"first_weight":1.00,
		"freight":5.00,
		"follow_weight":3.00,
		"follow_freight":7.00,
		"special_place_setting":"no",
		"special_free_freight_setting":"no"
		},{
		"moudle_name":"测试模板2",
		"special_place_setting":"yes",
			{
			"area":"新疆,西藏",
			"first_weight":4.00,
			"freight":5.00,
			"follow_weight":3.00,
			"follow_freight":7.00,
			"operate":"删除"
			},
		"special_free_freight_setting":"no"
		},{
		"moudle_name":"测试模板3",
		"freight_style":"默认运费",
		"first_weight":1.00,
		"freight":5.00,
		"follow_weight":3.00,
		"follow_freight":7.00,
		"special_place_setting":"no",
		"special_free_freight_setting":"yes",
			{
			"area":"江苏,上海",
			"style":"金额", 
			"condition":60.00,
			"operate":"删除"
			}
		}]
		"""
@panda @list
Scenario: 客户查看运费模板列表页
	Then aini查看运费列表
	|moudle_name|freight_style| address |first_weight|freight|follow_weight|follow_freight|
	| 测试模板1 |  普通快递   |  全国   |    1.00    |  5.00 |    3.00     |    7.00      |
	| 测试模板2 |  普通快递   |新疆,西藏|    4.00    |  5.00 |    3.00     |    7.00      |
	|测试模板3(已设置包邮条件)|普通快递|全国|  1.00  |  5.00 |    3.00     |    7.00      | 