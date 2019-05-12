# -*- coding: utf-8 -*-
from offer.projects.Automation.excel_util import excelutil

#此处要想使用相对路径，需要将工作目录改成当前目录
#util = excelutil('./web_testcase.xls', 'w',head=['a','b']) #带表头的新表格，指定文件名
util = excelutil('web_testcase.xlsx','r')
x = util.read_lines_to_list(0) #读所有列数据，从第1行开始
print(x)