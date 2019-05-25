# -*- coding: utf-8 -*-
# Author  ：Rocklee
# Time  ：2019/5/25  12:24

from bs4 import BeautifulSoup
from offer.projects.Automation.requestutil import requestutil
import re
from offer.projects.Automation.excel_util import excelutil

requtil = requestutil()

def capture(url):
    global requtil
    requtil.setUrl(url)
    return requtil.request('get', json=False, isjson=False)

def analysisPage(html_doc):
    temp = []
    soup = BeautifulSoup(html_doc, 'html.parser')
    #print(soup)
    for x in soup.find_all('div',class_='rank__name'):
        #print(x)
        name = x.text
        url =str(list(x.children)[0])
        compile_mode = re.compile(r'["](.*?)["]',re.S)
        url = re.findall(compile_mode,url)[0]
        print("品牌名称：%s,链接：%s"%(name,url))
        temp.append(url)
    return temp

def analysis_rank(html_doc):
    soup1 = BeautifulSoup(html_doc, 'html.parser')
    #print(soup)
    product_name = soup1.find('h1', attrs={'class': 'product-model__name'}).get_text()
    score = ''
    peoplenum = ''
    price = ''
    print("品牌名称：%s"%product_name)
    ear_details = soup1.find('div', attrs={'class': 'review__score'})
    if ear_details:
        #print(ear_details)
        score = ear_details.find('strong').get_text() #评分
        peoplenum = ear_details.find('a').get_text() #评分人数
        peoplenum = re.sub('人评分','',peoplenum) #评分人数
        price = soup1.find('b', attrs={'class': 'price-type'}).get_text() #价格
    else:
        print("暂无评分")
    return product_name,score,peoplenum,price

def save_excel(product_name,score,peoplenum,price):
    util = excelutil('E:\\Earphone.xls','a', head=['品牌名字', '评分', '评分人数','价格']) #预先新建一个文件，使用追加模式写入文件，不然的话每次都是写入第一行，覆盖上次的内容
    util.write_nextline([product_name,score,peoplenum,price], save=True)

if __name__ == '__main__':
    page = capture('http://top.zol.com.cn/compositor/223/param_11032_17.html')
    earphone_list = analysisPage(page)
    #print(earphone_list)
    for i in range(len(earphone_list)):
        print("排行第%s的品牌：%s"%(i+1,'https:' + earphone_list[i]))
        product_name, score, peoplenum, price = analysis_rank(capture('https:' + earphone_list[i]))
        save_excel(product_name,score,peoplenum,price)