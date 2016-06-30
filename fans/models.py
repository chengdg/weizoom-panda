from django.db import models

# Create your models here.

class Fans(models.Model):
	fans_id = models.IntegerField(default=0) #粉丝id
	fans_url = models.CharField(max_length=2048, default='') #粉丝头像
	male = models.BooleanField(default=True) #性别,1-男:0-女
	location = models.CharField(max_length=1024, default='') #所在地
	purchasing_index = models.FloatField(default=0) #购买指数
	spread_index = models.FloatField(default=0) #传播指数
	status = models.IntegerField(default=0) #投放状态
	related_order_id = models.CharField(max_length=1024, default='') #关联订单号
	created_at = models.DateTimeField(auto_now_add=True) #投放日期

	class Meta(object):
		db_table = 'fans_fans'