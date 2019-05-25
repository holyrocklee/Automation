from bs4 import BeautifulSoup, Tag


from offer.projects.Automation.http_util import download
from offer.projects.Automation.requestutil import requestutil

requtil = requestutil()
count = 0

'''
汽车之家论坛抓取图片；
爬取照片容易碰到10060问题，关闭系统防火墙能爬到更多的照片；
另一个问题是网站爬虫限制
'''


def capture(url):
    global requtil
    requtil.setUrl(url)
    return requtil.request('get', json=False, isjson=False)


def analysisPage(html_doc):
    temp = []
    soup = BeautifulSoup(html_doc, 'html.parser')
    for x in soup.find_all('a'):
        if x.get('href').startswith('//club.autohome.com.cn/bbs/thread') and len(list(x.children)) == 1 and x.get('onclick') is None:
            temp.append(x.get('href'))
    return temp


def analysisTie(savepath, html_doc):
    global count
    soup = BeautifulSoup(html_doc, 'html.parser')
    for x in soup.find_all('img'):
        if x.get('onerror') == 'tz.picNotFind(this)':
            count = count + 1
            if x.get('src9'):
                download('https:' + x.get('src9'), savepath + str(count) + '.jpg')
            else:
                download('https:' + x.get('src'), savepath + str(count) + '.jpg')


if __name__ == '__main__':
    for x in range(71):
        print('page======' + str(x))
        page = capture('https://club.autohome.com.cn/JingXuan/275/' + str(x + 1))
        tielist = analysisPage(page)
        analysisTie('E:\\下载\\', capture('https:' + tielist[0]))
