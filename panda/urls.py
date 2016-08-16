# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

from core.restful_url import restful_url
from account import views as account_view
from business import views as business_view


# from admin.sites import site
# site = admin_sites.AdminSite()

#import admin as loc_admin
#from weixin import sinulator_views as sinulator_views

urlpatterns = patterns('',
	url(r'^$', account_view.index),
	url(r'^component/', restful_url('component')),
	url(r'^account/', restful_url('account')),
	url(r'^outline/', restful_url('outline')),
	url(r'^resource/', restful_url('resource')),
	url(r'^order/', restful_url('order')),
	url(r'^product/', restful_url('product')),
	url(r'^fans/', restful_url('fans')),
	url(r'^reconcile/', restful_url('reconcile')),
	url(r'^manager/', restful_url('manager')),
	url(r'^customer/', restful_url('customer')),
	url(r'^product_catalog/', restful_url('product_catalog')),
	url(r'^self_shop/', restful_url('self_shop')),
	url(r'^freight_service/', restful_url('freight_service')),
	url(r'^business/',restful_url('business'))
)

urlpatterns += staticfiles_urlpatterns()

# handler404 = 'account.views.show_error_page'
# handler500 = 'account.views.show_error_page'
