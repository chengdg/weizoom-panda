#_author_:徐梓豪 2016-07-28

Feature:客户管理-入主申请查询

	#说明
		#a.查询条件：【客户编号】，【公司名称】，【一级类目】，【二级类目】，【企业类型】，【手机号】，【客户状态】，【所在地】
		#b.点击【查询】按钮，列表中出现所有未被删除的客户入驻申请
		   #列表字段包括【客户编号】，【公司名称】，【所在地】，【企业类型】，【类目】，【联系人】，【手机号】，【状态】
		   #已通过的入驻申请操作栏中只保留修改和删除

Background:
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

		Given yunying登录系统
		When yunying添加分类
		"""
		[{
		{
		"head_classify":"无",
		"classify_name":"家用电器",
		"comments":"1"
		},{
		"head_classify":"无",
		"classify_name":"早餐冲饮",
		"comments":"1"
		},{
		"head_classify":"无",
		"classify_name":"零食小吃",
		"comments":"1"
		},{
		"head_classify":"家用电器",
		"classify_name":"净化器",
		"comments":"2"
		},{
		"head_classify":"家用电器",
		"classify_name":"加湿器",
		"comments":"2"
		},{
		"head_classify":"早餐冲饮",
		"classify_name":"咖啡豆",
		"comments":"2"
		},{
		"head_classify":"早餐冲饮",
		"classify_name":"咖啡粉",
		"comments":"2"
		},{
		"head_classify":"零食小吃",
		"classify_name":"地方特产",
		"comments":"2"
		}{
		"head_classify":"零食小吃",
		"classify_name":"饼干蛋糕",
		"comments":"2"
		}
		}]
		"""




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
		"first_classify":"早餐冲饮",
		"second_classify":"咖啡粉",
		"second_classify":"咖啡豆"
		}	
		"""
		#并且上传对应的资质证明

		Then 点击完成提交	


		Given 登录页面
		When 录入企业相关信息
		"""
		{
		"company_type":"厂家直销",
		"company_name":"武汉鸭脖",
		"registered_capital":"300",
		"legal_press":"武汉鸭脖",
		"connext_person":"  ",
		"monile_number":"13756432550",
		"E-mail":"whyb@163.com",
		"weixin/qq":"1414125981",
		"local_space":"湖北省武汉市",
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
		"first_classify":"零食小吃",
		"second_classify":"地方特产",
		}	
		"""
		#并且上传对应的资质证明

		Then 点击完成提交

@panda @lhy
Scenario:1 通过不同的条件过滤列表
	Given yunying登录管理系统
	When yunying查看客户管理列表
	|costumer_code |  company_name  | local_space | company_type |       classify       | connect_person |mobile_number| statute |   operate  |
	| cj2016000001 |	土小宝      |江苏省-南京市|   厂家直销   |家用电器;净化器;加湿器|      土小宝    | 13813944325 |  未审核 |通过驳回修改删除|
	| dl2016000001 |    爱伲咖啡    |江苏省-南京市|代理/贸易/分销|早餐冲饮;咖啡粉;咖啡豆|     	爱伲      | 13813944327 |  未审核 |
	|通过驳回修改删除|
	| cj2016000002 |    武汉鸭脖    |湖北省—武汉市|   厂家直销   |零食小吃;地方特产     |     武汉鸭脖    | 13756432550 |  未审核 |
	|通过驳回修改删除|
	When yunying设置客户管理列表的查询条件
	"""
	{
	"costumer_code":"cj2016000001"
	}
	"""
	Then yunying可以获得客户管理列表
	|costumer_code |  company_name  | local_space | company_type |       classify       | connect_person |mobile_number| statute |   operate  |
	| cj2016000001 |	土小宝      |江苏省-南京市|   厂家直销   |家用电器;净化器;加湿器|      土小宝    | 13813944325 |  未审核 |通过驳回修改删除|
	When yunying设置客户管理列表的查询条件
	"""
	{
	"costumer_code":"cj"
	}
	"""
	Then yunying可以获得客户管理列表
	|costumer_code |  company_name  | local_space | company_type |       classify       | connect_person |mobile_number| statute |   operate  |
	| cj2016000001 |	土小宝      |江苏省-南京市|   厂家直销   |家用电器;净化器;加湿器|      土小宝    | 13813944325 |  未审核 |通过驳回修改删除|
	| cj2016000002 |    武汉鸭脖    |湖北省—武汉市|   厂家直销   |零食小吃;地方特产     |     武汉鸭脖    | 13756432550 |  未审核 |
	|通过驳回修改删除|
	When yunying设置客户管理列表的查询条件
	"""
	{
	"company_name":"爱伲咖啡"
	}
	"""
	Then yunying可以获得客户管理列表
	|costumer_code |  company_name  | local_space | company_type |       classify       | connect_person |mobile_number| statute |   operate  |
	| dl2016000001 |    爱伲咖啡    |江苏省-南京市|代理/贸易/分销|早餐冲饮;咖啡粉;咖啡豆|     	爱伲      | 13813944327 |  未审核 |
	|通过驳回修改删除|
	When yunying设置客户管理列表的查询条件
	"""
	{
	"company_name":"武汉"
	}
	"""
	Then yunying可以获得客户管理列表	
	|costumer_code |  company_name  | local_space | company_type |       classify       | connect_person |mobile_number| statute |   operate  |
	| cj2016000002 |    武汉鸭脖    |湖北省—武汉市|   厂家直销   |零食小吃;地方特产     |     武汉鸭脖    | 13756432550 |  未审核 |
	|通过驳回修改删除|
	When yunying设置客户管理列表的查询条件
	"""
	[{
		"classify":{
					"first_classify":"零食小吃",
					"second_classify":""
		}
	}]
	"""
	Then yunying可以获得客户管理列表
	|costumer_code |  company_name  | local_space | company_type |       classify       | connect_person |mobile_number| statute |   operate  |
	| cj2016000002 |    武汉鸭脖    |湖北省—武汉市|   厂家直销   |零食小吃;地方特产     |     武汉鸭脖    | 13756432550 |  未审核 |
	|通过驳回修改删除|
	When yunying设置客户管理列表的查询条件
	"""
	[{
		"classify":{
					"first_classify":"零食小吃",
					"second_classify":"饼干蛋糕"
		}
	}]
	"""
	Then yunying可以获得客户管理列表
	|costumer_code |  company_name  | local_space | company_type |       classify       | connect_person |mobile_number| statute |   operate  |
	When yunying设置客户管理列表的查询条件
	"""
	[{
		"classify":{
					"first_classify":"早餐冲饮",
					"second_classify":"咖啡粉"
		}
	}]
	"""
	Then yunying可以获得客户管理列表
	|costumer_code |  company_name  | local_space | company_type |       classify       | connect_person |mobile_number| statute |   operate  |
	| dl2016000001 |    爱伲咖啡    |江苏省-南京市|代理/贸易/分销|早餐冲饮;咖啡粉;咖啡豆|     	爱伲      | 13813944327 |  未审核 |
	|通过驳回修改删除|
	When yunying设置客户管理列表的查询条件
	"""
	{
	"company_type":"厂家直销"
	}	
	"""
	Then yunying可以获得客户管理列表
	|costumer_code |  company_name  | local_space | company_type |       classify       | connect_person |mobile_number| statute |   operate  |
	| cj2016000001 |	土小宝      |江苏省-南京市|   厂家直销   |家用电器;净化器;加湿器|      土小宝    | 13813944325 |  未审核 |通过驳回修改删除|
	| cj2016000002 |    武汉鸭脖    |湖北省—武汉市|   厂家直销   |零食小吃;地方特产     |     武汉鸭脖    | 13756432550 |  未审核 |
	|通过驳回修改删除|
	When yunying设置客户管理列表的查询条件
	"""
	{
	"company_type":"代理/分销/贸易"
	}	
	"""
	Then yunying可以获得客户管理列表
	|costumer_code |  company_name  | local_space | company_type |       classify       | connect_person |mobile_number| statute |   operate  |
	| dl2016000001 |    爱伲咖啡    |江苏省-南京市|代理/贸易/分销|早餐冲饮;咖啡粉;咖啡豆|     	爱伲      | 13813944327 |  未审核 |
	|通过驳回修改删除|
	When yunying设置客户管理列表的查询条件
	"""
	{
	"mobile_number":"13813944327"
	}	
	"""
	Then yunying可以获得客户管理列表
	|costumer_code |  company_name  | local_space | company_type |       classify       | connect_person |mobile_number| statute |   operate  |
	| dl2016000001 |    爱伲咖啡    |江苏省-南京市|代理/贸易/分销|早餐冲饮;咖啡粉;咖啡豆|     	爱伲      | 13813944327 |  未审核 |
	|通过驳回修改删除|
	When yunying设置客户管理列表的查询条件
	"""
	{
	"mobile_number":"13713744352"
	}	
	"""
	Then yunying可以获得客户管理列表
	|costumer_code |  company_name  | local_space | company_type |       classify       | connect_person |mobile_number| statute |   operate  |
	When yunying设置客户管理列表的查询条件
	"""
	{
	"statute":"未审核"
	}	
	"""
	Then yunying可以获得客户管理列表
	|costumer_code |  company_name  | local_space | company_type |       classify       | connect_person |mobile_number| statute |   operate  |
	| cj2016000001 |	土小宝      |江苏省-南京市|   厂家直销   |家用电器;净化器;加湿器|      土小宝    | 13813944325 |  未审核 |通过驳回修改删除|
	| dl2016000001 |    爱伲咖啡    |江苏省-南京市|代理/贸易/分销|早餐冲饮;咖啡粉;咖啡豆|     	爱伲      | 13813944327 |  未审核 |
	|通过驳回修改删除|
	| cj2016000002 |    武汉鸭脖    |湖北省—武汉市|   厂家直销   |零食小吃;地方特产     |     武汉鸭脖    | 13756432550 |  未审核 |
	|通过驳回修改删除|
	When yunying设置客户管理列表的查询条件
	"""
	{
	"statute":"审核通过"
	}	
	"""
	Then yunying可以获得客户管理列表
	|costumer_code |  company_name  | local_space | company_type |       classify       | connect_person |mobile_number| statute |   operate  |
	When yunying设置客户管理列表的查询条件
	"""
	[{
		"local_space":{
						"province":"江苏省",
						"city":"南京市",
						"area":"玄武区"
		}
	}]	
	"""
	Then yunying可以获得客户管理列表
	|costumer_code |  company_name  | local_space | company_type |       classify       | connect_person |mobile_number| statute |   operate  |
	| cj2016000001 |	土小宝      |江苏省-南京市|   厂家直销   |家用电器;净化器;加湿器|      土小宝    | 13813944325 |  未审核 |通过驳回修改删除|
	When yunying设置客户管理列表的查询条件
	"""
	[{
		"local_space":{
						"province":"江苏省",
						"city":"南京市",
						"area":""
		}
	}]	
	"""
	Then yunying可以获得客户管理列表
	|costumer_code |  company_name  | local_space | company_type |       classify       | connect_person |mobile_number| statute |   operate  |
	| cj2016000001 |	土小宝      |江苏省-南京市|   厂家直销   |家用电器;净化器;加湿器|      土小宝    | 13813944325 |  未审核 |通过驳回修改删除|
	| dl2016000001 |    爱伲咖啡    |江苏省-南京市|代理/贸易/分销|早餐冲饮;咖啡粉;咖啡豆|     	爱伲      | 13813944327 |  未审核 |
	|通过驳回修改删除|
	When yunying设置客户管理列表的查询条件
	"""
	[{
		"local_space":{
						"province":"江西省",
						"city":"南昌市",
						"area":""
		}
	}]	
	"""
	Then yunying可以获得客户管理列表
	|costumer_code |  company_name  | local_space | company_type |       classify       | connect_person |mobile_number| statute |   operate  |