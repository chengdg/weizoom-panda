#-*- coding: utf8 -*-
import xlrd
import sys


reload(sys)
sys.setdefaultencoding("utf-8")
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "panda.settings")

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)



from django.core.management.base import BaseCommand
from eaglet.utils.resource_client import Resource
from panda.settings import ZEUS_SERVICE_NAME, EAGLET_CLIENT_ZEUS_HOST

from product import models as product_models
from account import models as account_models




print 'OK!'

fname = "axe.xlsx"
bk = xlrd.open_workbook(fname)
shxrange = range(bk.nsheets)
try:
	sh = bk.sheet_by_name("1")
except:
	print "no sheet in %s named Sheet1" % fname
#获取行数
nrows = sh.nrows
#获取列数
ncols = sh.ncols
print "nrows %d, ncols %d" % (nrows,ncols)
#获取第一行第一列数据 
cell_value = sh.cell_value(1,1)
#print cell_value
  
row_list = []
#获取各行数据
for i in xrange(1,nrows):
	row_data = sh.row_values(i)
	panda_id, corpid = row_data[0], row_data[3]
	if corpid.find('-') == -1:
		print panda_id, corpid
		account_models.UserProfile.objects.filter(user_id=int(panda_id)).update(corpid=corpid)
		#row_list.append(row_data)
