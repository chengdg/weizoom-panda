#coding=utf8

# 调用接口发送钉钉消息的工具 duhao

from django.conf import settings

from bdem import msgutil

topic_name = "customer-add-product"
msg_name = "customer_product_info"

def send_product_message(data):
	data = {
		"product_id": data.product_id,
		"product_name": data.product_name,
		"customer_name": data.customer_name,
		"product_image": data.product_image,
		"category": data.category,
		"price": data.price,
		"price_info": data.price_info,
		"push_status": data.push_status,
		"first_sale_time": data.first_sale_time,
		"show_list": data.show_list,
		"sales_revenue": data.sales_revenue,
		"buyer_count": data.buyer_count,
		"order_area": data.order_area,
		"evaluation": data.evaluation,
		"evaluation_list": data.evaluation_list
	}
	
	msgutil.send_message(topic_name, msg_name, data)
	