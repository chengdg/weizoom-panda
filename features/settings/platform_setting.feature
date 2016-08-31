auther:徐梓豪 2016-08-31
Feature:运营人员进行平台配置
"""
1.新增自营平台
2.对新增的平台，批量同步之前的商品
"""
Background:
	Given manager登录管理系统
	When manager添加账号
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
		
	Given 设置'jobs'为自营平台账号
	Given 添加jobs店铺名称为'微众家'
	Given 设置'Nokia'为自营平台账号
	Given 添加Nokia店铺名称为'微众妈妈'

@panda @platform
Scenario:1  新增自营平台

	Given yunying登录管理系统
	When yunying进入自营平台页面，点击添加自营平台
	"""
	[{
		"platform_name":"微众家 jobs",
		"comment":""
		},{
		"platform_name":"微众妈妈 Nokia",
		"comment":""
	}]
	"""
	Then yunying查看平台配置列表
	| num | platform_name | user_name |     operate      |
	|  01 |    微众家     |   jobs    | 批量同步现有商品 |
	|  02 |   微众妈妈    |   Nokia   | 批量同步现有商品 |

@panda @platform
Scenario:2  对新增的平台，批量同步之前的商品
	Given yunying登录管理系统
	When yunying进入自营平台页面，点击添加自营平台
	"""
	[{
		"platform_name":"微众家 jobs",
		"comment":""
		},{
		"platform_name":"微众妈妈 Nokia",
		"comment":""
	}]
	"""
	Then yunying查看平台配置列表
	| num | platform_name | user_name |     operate      |
	|  01 |    微众家     |   jobs    | 批量同步现有商品 |
	|  02 |   微众妈妈    |   Nokia   | 批量同步现有商品 |

	Then yunying批量同步现有商品
	"""
	{
	"platform_name":"微众家"
	}
	"""
	Then yunying查看平台配置列表 
	| num | platform_name | user_name |     operate      |
	|  01 |    微众家     |   jobs    |      同步中      |
	|  02 |   微众妈妈    |   Nokia   | 批量同步现有商品 |
	Then yunying在同步结束后查看列表
	| num | platform_name | user_name |     operate      |
	|  01 |    微众家     |   jobs    |      已同步      |
	|  02 |   微众妈妈    |   Nokia   | 批量同步现有商品 |





	
