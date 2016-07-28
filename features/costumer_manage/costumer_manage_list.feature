auther:徐梓豪 2016-07-29
feature:客户管理列表
"""
	1.运营查看客户管理列表
	2.运营查看客户管理详情
	3.运营审核通过入驻申请
	4.运营驳回入驻申请
	5.运营修改入驻申请
	6.运营删除入驻申请
"""
Background:
		Given 登录页面
		When 录入企业相关信息
		"""
		{
		"company_type":"厂家直销",
		"company_name":"土小宝",
		"registered_capital":"200",
		"legal_press":"土小宝",
		"connext_person":"土小宝呀",
		"monile_number":"13813944325",
		"E-mail":"tuxiaobao@163.com",
		"weixin/qq":"445068325",
		"local_space":"江苏省南京市玄武区",
		"detail_address":"大学生创业园十二号楼"
		}
		"""
		Then 点击下一步,上传基本资质文件
		"""
		{
		"business_license":"",
		"end_time":"2016-09-31",
		"tax_authority":"",
		"end_time":"2016-09-31",
		"organization_code":"",
		"end_time":"2016-09-31",
		"establish_acount":"",
		"end_time":"2016-09-31"
		}
		"""
		Then 点击下一步,选择商品类别，并上传对应的资质
		"""
		{
		"first_classify":"家用电器",
		"second_classify":"净化器",
		"second_classify":"加湿器"
		}	
		"""
		#并且上传对应的资质证明

		Then 点击完成提交


		Given 登录页面
		When 录入企业相关信息
		"""
		{	
		"company_type":"代理/贸易/分销",
		"company_name":"爱伲咖啡",
		"registered_capital":"50",
		"legal_press":"爱伲",
		"connext_person":"爱伲",
		"monile_number":"13813944327",
		"E-mail":"ainicoffee@163.com",
		"weixin/qq":"445068327",
		"local_space":"江苏省南京市栖霞区",
		"detail_address":"和燕路18号"
		}
		"""
		Then 点击下一步,上传基本资质文件
		"""
		{
		"business_license":"",
		"end_time":"2016-09-31",
		"tax_authority":"",
		"end_time":"2016-09-31",
		"organization_code":"",
		"end_time":"2016-09-31",
		"establish_acount":"",
		"end_time":"2016-09-31"
		}
		"""
		Then 点击下一步,选择商品类别，并上传对应的资质
		"""
		{
		"first_classify":"家用电器",
		"second_classify":"净化器",
		"second_classify":"加湿器"
		}	
		"""
		#并且上传对应的资质证明

		Then 点击完成提交

		Given manager登录管理系统
		Then manager添加账号
		"""
		{
			"account_type":"运营",
			"account_name":"运营部门",
			"login_account":"yunying",
			"password":123456,
			"ramarks":"运营部门"
		}
		"""

@penda @lhy
Scenairo:1  运营查看客户管理列表
	Given yunying登录管理系统
	When yunying查看客户管理列表
	|costumer_code|  company_name  | local_space | company_type | connect_person |mobile_number| statute |
	| cs201607071 |		土小宝     |江苏省-南京市|   厂家直销   |      土小宝    | 13813944325 |  未审核 |
	| cs201607072 |    爱伲咖啡    |江苏省-南京市|代理/贸易/分销|		爱伲     | 13813944327 |  未审核 |

@penda @lhy
Scenairo:2 运营查看客户管理详情
	Given yunying登录管理系统
	When yunying查看客户管理列表
	|costumer_code|  company_name  | local_space | company_type | connect_person |mobile_number| statute |
	| cs201607071 |		土小宝     |江苏省-南京市|   厂家直销   |      土小宝    | 13813944325 |  未审核 |
	| cs201607072 |    爱伲咖啡    |江苏省-南京市|代理/贸易/分销|		爱伲     | 13813944327 |  未审核 |
	Then yunying查看公司名称为'土小宝'的详情
	"""
	[{
	"base_information":{
					"company_type":"厂家直销",
					"company_name":"土小宝",
					"registered_capital":"200",
					"legal_press":"土小宝",
					"connext_person":"土小宝呀",
					"monile_number":"13813944325",
					"E-mail":"tuxiaobao@163.com",
					"weixin/qq":"445068325",
					"local_space":"江苏省南京市玄武区"
	},
	"base_aptitude":{
					"business_license":"",
					"end_time":"2016-09-31",
					"tax_authority":"",
					"end_time":"2016-09-31",
					"organization_code":"",
					"end_time":"2016-09-31",
					"establish_acount":"",
					"end_time":"2016-09-31"
	},
	"classify":{
			   "first_classify":"家用电器",
				"second_classify":"净化器",
				"second_classify":"加湿器"
	}
	}]

@penda @lhy
Scenairo:3 运营审核通过入驻申请
	Given yunying登录系统
	When yunying审核通过公司名称为'土小宝'的入驻申请
	Then yunying查看客户管理列表
	|costumer_code|  company_name  | local_space | company_type | connect_person |mobile_number| statute |
	| cs201607071 |		土小宝     |江苏省-南京市|   厂家直销   |      土小宝    | 13813944325 | 审核通过|
	| cs201607072 |    爱伲咖啡    |江苏省-南京市|代理/贸易/分销|		爱伲     | 13813944327 |  未审核 |

@penda @lhy
Scenairo:4 运营审核驳回入驻申请
	Given yunying登录系统
	When yunying驳回公司名称为'爱伲咖啡'的入驻申请
	"""
	{
	"reason":"资质不全",
	"comment":"缺少资质证明"
	}
	"""
	Then yunying查看客户管理列表
	|costumer_code|  company_name  | local_space | company_type | connect_person |mobile_number| statute |
	| cs201607071 |		土小宝     |江苏省-南京市|   厂家直销   |      土小宝    | 13813944325 |  未审核 |
	| cs201607072 |    爱伲咖啡    |江苏省-南京市|代理/贸易/分销|		爱伲     | 13813944327 |  不合格 |

@penda @lhy
Scenairo:5 运营修改入驻申请
	Given yunying登录系统
	When yunying修改公司名称为'土小宝'的入驻申请
	"""
	[{
	"base_information":{
					"company_type":"厂家直销",
					"company_name":"土小宝",
					"registered_capital":"200",
					"legal_press":"土小宝",
					"connext_person":"土小宝",
					"monile_number":"13813944325",
					"E-mail":"tuxiaobao@163.com",
					"weixin/qq":"445068327",
					"local_space":"北京北京市海淀区"
	},
	"base_aptitude":{
					"business_license":"",
					"end_time":"2016-09-10",
					"tax_authority":"",
					"end_time":"2016-09-31",
					"organization_code":"",
					"end_time":"2016-09-31",
					"establish_acount":"",
					"end_time":"2016-09-10"
	},
	"classify":{
			   "first_classify":"家用电器",
				"second_classify":"净化器",
				"second_classify":"加湿器",
				"first_classify":"3c数码",
				"second_classify":"手机"
	}
	}]
	Then yunying查看客户管理列表
	|costumer_code|  company_name  | local_space | company_type | connect_person |mobile_number| statute |
	| cs201607071 |		土小宝     |江苏省-南京市|   厂家直销   |      土小宝    | 13813944325 |  未审核 |
	| cs201607072 |    爱伲咖啡    | 北京-北京市 |代理/贸易/分销|		爱伲     | 13813944327 |  不合格 |

@penda @lhy
Scenairo:6 运营删除入驻申请
	Given yunying登录系统
	When yunying删除公司名称为'土小宝'的入驻申请	
	Then yunying查看客户管理列表
	|costumer_code|  company_name  | local_space | company_type | connect_person |mobile_number| statute |
	| cs201607072 |    爱伲咖啡    | 北京-北京市 |代理/贸易/分销|		爱伲     | 13813944327 |  未审核 | 
	

	
