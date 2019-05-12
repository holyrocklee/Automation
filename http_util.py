#coding=utf-8
import json
from urllib import request

import requests
import random
import time
import socket

from offer.projects.Automation.file_util import fileutil
from offer.projects.Automation.mysql_util import mysql_util

"""

"""
def get_context(url,encode='utf-8',type='get',json=False,data=None,otherheader=None):
    header={
        'Accept':'*/*',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Content-type':'application/json'
    }
    if otherheader!=None:
        for h in otherheader:
            header[h]=otherheader[h]
    timeout = 200
    while True:
        try:
            rep = requests.Session()
            if type=='get':
                rep = requests.get(url,headers = header,timeout = timeout)
            elif type=='post':
                rep = requests.post(url,data,headers = header,timeout = timeout)
            else:
                print('request type is error !!')
                return 'error'
            rep.encoding = encode
            break
        except socket.timeout as e:
            print( '3:', e)
            time.sleep(random.choice(range(8,15)))

        except socket.error as e:
            print( '4:', e)
            time.sleep(random.choice(range(20, 60)))
    if json:
        return rep.json()
    return rep.text

def download(url,path):
    print('down')
    data = request.urlopen(url).read()
    f = open(path, "wb")
    f.write(data)
    f.close()


if __name__ == '__main__':
    util = mysql_util()
    util.connect({'host': '118.190.91.189', 'user': 'dev', 'passwd': 'Json#331', 'db': 'dingjia'})
    temp=util.getData('SELECT callback_content FROM dingjia.log_maintenance_result WHERE callback_content IS NOT NULL LIMIT 100;')
    for x in temp:
        if x[0].startswith('{'):
            x=json.loads(x[0])
            parameter = {}
            parameter["VechicleHistoryData"] = x
            text = get_context('http://118.190.5.1:5014/cs/vhis/analysis', type='post', data=parameter, json=True)
            print(parameter)
            print(text)
    # for x in data:
    #     print(type(x))
    #     print(x)
    #     parameter = {}
    #     parameter["VechicleHistoryData"]=json.loads(x)
    #     text = get_context('http://118.190.5.1:5014/cs/vhis/analysis', type='post', data=parameter, json=True)
    #     print(json.dumps(parameter))
    #     print(str(text))
