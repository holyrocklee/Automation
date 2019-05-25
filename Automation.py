# -*- coding: utf-8 -*-
import json
import jsonpath
from offer.projects.Automation.excel_util import excelutil

#此处要想使用相对路径，需要将工作目录改成当前目录
#util = excelutil('./web_testcase.xls', 'w',head=['a','b']) #带表头的新表格，指定文件名
from offer.projects.Automation.http_util import get_context
from openpyxl import Workbook

# wb = Workbook()
# ws1 = wb.active
def get_statuscode():
    util = excelutil('interface_testcase.xlsx','r')
    #x = util.read_lines_to_list(0) #读所有列数据，从第1行开始
    url_list = util.read_lines_to_list_by_cols([2,3],1) #读第2列数据,从第2行开始
    print(len(url_list))
    for data in url_list:
        url_common = data[0]
        addparam = data[1]
        url = url_common +'?'+ addparam
        #print(url)
        response = get_context(url,encode='utf-8',type='get')
        response = json.loads(response)
        status_code = jsonpath.jsonpath(response,'$..status')[0]
        print(status_code)
        #col_F = 'F%s' % (url_list.index(data)+2)
        #ws1[col_F] = status_code
    #wb.save(filename='interface_testcase.xlsx')
    return status_code


if __name__ == '__main__':
    status_code = get_statuscode()