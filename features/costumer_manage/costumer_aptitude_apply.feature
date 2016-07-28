auther:徐梓豪 2016-07-29
feature:客户上传资质文件
Background:
		#客户准备好对应资质文件的截图
		#客户明确自身产品的分类
		#客户登录网站
@penda @apitude
Scenairo:1 客户上传资质文件
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