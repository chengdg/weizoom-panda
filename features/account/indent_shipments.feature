#author: 徐梓豪 2016.06.06

Feature:云商通-新增商品-订单发货
"""
	1.用jobs在云商通系统中新增并上架商品
    3.在微信上下订单
    4.用运营账号在管理系统中进行订单发货 
"""

Background:
	Given manager登录管理系统
	When manager添加账号
	"""
		[{
			"account_type":"合作客户",
			"account_name":"土小宝",
			"login_account":"tuxiaobao",
			"password":123456,
			"ramarks":"土小宝客户体验账号"
		},{
			"account_type":"运营",
			"account_name":"运营部门",
			"login_account":"yunying",
			"password":123456,
			"ramarks":"运营部门"
		}]
	"""
	When tuxiaobao使用密码123456登录管理系统
	When tuxiaobao添加商品
	"""
		[{
			"commodity_name":"武汉鸭脖",
			"title"："周黑鸭 鲜卤鸭脖 230g/袋 办公室休闲零食 肉干小食",
			"product_price":9.9,
			"setlement_price":9.9,
			"product_weight":0.23,
			"repertory":{
						"is_limit":"on",
						"limit_num":500
			},
			"picture":"",
			"description":"周黑鸭 鲜卤鸭脖 230g/袋 办公室休闲零食 肉干小食"
			},{
			"commodity_name":"NIKE耐克男鞋便减震舒适休闲跑步鞋",
			"title"："旗舰店—618粉丝狂欢， 赢200元粉丝券！",
			"product_price":322,
			"setlement_price":298,
			"product_weight":0.5,
			"repertory":{
						"is_limit":"off"
			},
			"description":"旗舰店—618粉丝狂欢，关注微信公众号"jdxyyz" 赢200元粉丝券！"
		}]
	"""
@weiapp @weiapp @hj
#Scenario:1 新增商品
	Given jobs使用密码1登录云商通系统
    When jobs添加商品
	"""
	[{
		"name":"武汉鸭脖",
		"supplier":"周黑鸭",
		"type":"普通商品",
		"procurement_price":40,
		"title":"周黑鸭 鲜卤鸭脖 230g/袋 办公室休闲零食 肉干小食",
		"price":60,
		"weight":0.5,
		"stock_type":{"有限"，
					  "num":100
					}，
		"images":[{
					"url":"桌面/鸭脖.jpg"
					},{
					"url":"桌面/鸭脖1.jpg"
					}
				}],
		"carriage_set":"统一运费",
		"carriage"：5,
		"payment":"货到付款"，
		"destribe":"香辣鸭脖"
		},{
		"name":"IKE耐克男鞋便减震舒适休闲跑步鞋",
		"supplier":"耐克旗舰店",
		"type":"普通商品",
		"procurement_price":320,
		"title":"旗舰店—618粉丝狂欢， 赢200元粉丝券！",
		"price":450,
		"weight":1.5,
		"stock_type":"无限",
		"images":[{
					"url":"桌面/耐克.jpg"
					},{
					"url":"桌面/耐克1.jpg"
					}
				}],
		"carriage_set":"统一运费",
		"carriage"：7,
		"payment":"货到付款"，
		"destribe":"旗舰店—618粉丝狂欢， 赢200元粉丝券！"
	}]
	"""
	Then jobs查看代售商品列表
	| information | supplier | group | price | stocks | sales | synchronize_time |
	|  武汉鸭脖   |南京火腿肠|       | 60.00 |  100   |  0    | 2016-06-06 17:44 |
	|  耐克男鞋   |南京火腿肠|       |450.00 |  无限  |  0    | 2016-06-06 17:44 |


	Given jobs使用密码1登录云商通系统
    When jobs上架信息为'武汉鸭脖'和'耐克男鞋'的商品
    """
    {
    	"information":"武汉鸭脖",
    	"information":"耐克男鞋"
    }
    """
    Then jobs查看代售商品列表
    | information | supplier | group | price | stocks | sales | synchronize_time |
	
	
	And jobs查看在售商品列表
    | information | supplier | group | price | stocks | sales | synchronize_time |order|
    |  武汉鸭脖   |南京火腿肠|       | 60.00 |  100   |  0    | 2016-06-06 17:44 |  0  |
    |  耐克男鞋   |南京火腿肠|       |450.00 |  无限  |  0    | 2016-06-06 17:44 |  0  |

@weiapp @weiapp @hj
#Scenario:2 下订单

    When yunying使用密码123456登录系统
	When yunying绑定商品关联的云商通商品
	"""
		[{
			"name":"武汉鸭脖",
			"weapp_id":["微众家":"2400"]
			},{
			"name":"耐克男鞋",
			"weapp_id":["微众家":"2401"]
		}]
		
	"""
@weiapp @weiapp @hj    	
	When 微信用户批量消费aini在云商通商家'微众家'关联的商品
		|	order_id	  | date       | consumer |    type   |businessman|   product | payment  | payment_method | freight |   price  | product_integral |  	 coupon  		| paid_amount | 		weizoom_card 		| alipay | wechat | cash |      action       |  order_status   |
		|对应订单编号001  | 2016-6-7   | bill     |    购买   | 微众商城   | 武汉鸭脖  | 支付    | 支付宝         | 10      | 10.00    | 		          |                		|           10.00       |              				  | 10.00  | 0      | 0    |    jobs,支付      |  待发货         |
		|对应订单编号002  | 2016-6-7   | tom      |    购买   | 微众家     | 耐克男鞋  | 支付    | 支付宝         | 15      | 20.00    | 200              |        				|           10.00       |              				  | 10.00  | 0      | 0    |    jobs,支付      |  待发货         |	
		

@panda @customer
#Scenario:3 运营查看订单列表
	Given yunying使用密码123456登录管理系统
	Then yunying能获得订单列表
	"""
		[{
			"order_no":001,
			"order_time":"2016-06-07",
			"member":"徐梓豪",
			"status":"待发货",
			"actions":["发货"],
			"order_price":60.00,
			"products":[{
				"name":"武汉鸭脖",
				"price":180.00,
				"count":3
			}]
		},{
			"order_no": 002,
			"order_time":"2016-06-07",
			"member": "徐梓豪",
			"status":"待发货",
			"actions": ["发货"],
			"order_price": 450.00,
			"products": [{
				"name": "耐克男鞋",
				"price": 450.00,
				"count": 1
			}]
		}]
	"""
	And yunying选择订单编号'001'进行发货
	"""
	{
		"company":"中通快递",
		"code":101,
		"consigner":"徐梓豪"
	}
	Then yunying获得订单列表
	"""
		[{
			"order_no":001,
			"order_time":"2016-06-07",
			"member": "徐梓豪",
			"status":"已发货",
			"actions": ["完成"],
			"order_price":60.00,
			"products": [{
				"name": "武汉鸭脖",
				"price":180.00,
				"count":3
			}]
		},{
			"order_no":002,
			"order_time":"2016-06-07",
			"member": "徐梓豪",
			"status":"待发货",
			"actions": ["发货"],
			"order_price":450.00,
			"products":[{
				"name":"耐克男鞋",
				"price":450.00,
				"count": 1
			}]
		}]
	"""