# -*- coding: utf-8 -*-
# Author  ：Rocklee
# Time  ：2019/5/31  20:24

import pandas as pd
import re
from offer.projects.Automation.excel_util import excelutil

def get_result():
    df = pd.read_excel('E:\\javatest\\发动机.xlsx')
    # 将发动机excel文件插入第一行，表头分别为:描述详情的用simple_detail，描述序号的用num，其他表头无所谓
    data=df.ix[:,['simple_detail','num']].values  #读所有行的simple_detail以及num列的值，这里需要嵌套列表
    # detail = list(data[0][0])
    # number = data[0][1]
    PATTERN = r'([\u4e00-\u9fa5]*)(换)([\u4e00-\u9fa5]*)(发动机|引擎)([\u4e00-\u9fa5]*)'
    i = -1
    result = []
    singlenumbers = []
    detail = []
    for singledata in data:
        i = i+1
        singledetail = singledata[0]
        detail.append(singledetail)
        singlenum = singledata[1]
        print(singlenum)
        singlenumbers.append(singlenum)
        Regex = re.compile(PATTERN,re.S)
        m = Regex.findall(singledetail)
        if not m:
            result.append("格式不对应")
        else:
            result.append(m)
            result[i] = list(set(result[i]))
    print(result)
    return singlenumbers,result,detail

def manage_result(resultA):
    simplelist = []
    for i in range(len(resultA)):
        if resultA[i] == '格式不对应':
            simplelist.append("格式不对应")
        else:
            if len(resultA[i])==1:
                s = ''.join(resultA[i][0])
                simplelist.append(s)
            else:
                doublelist = []
                for j in range(len(resultA[i])):
                    s = ''.join(resultA[i][j])
                    doublelist.append(s)
                simplelist.append(doublelist)
    print(simplelist)
    return simplelist

def save_excel(singlenumbers,detail,simplelist):
    df = pd.DataFrame({'num':singlenumbers,'details':detail,'result':simplelist})
    df.to_excel('E:\\javatest\\final.xlsx')
    print("Done!")
    # util = excelutil('E:\\javatest\\final.xls','a', head=['num','details','result']) #注意先在本地建一个空白.xls文件
    # for singlenumber,singledetail,simpleresult in zip(singlenumbers,detail,simplelist):
    #     util.write_nextline([singlenumber,singledetail,simpleresult], save=True)

if __name__ == '__main__':
    singlenumbers,resultA,detail = get_result()
    simplelist = manage_result(resultA)
    save_excel(singlenumbers,detail,simplelist)