import time
from bs4 import BeautifulSoup
import bs4
import re
import os
import datetime
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
from CSVUtil import CSVUtil

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}


class ChengDuHouseSpider:
    def __init__(self):
        self.url = 'https://www.cdzjryb.com/SCXX/Default.aspx?action=ucEveryday2'

        itemNames = ['区域', '总面积（平方米）', '住宅套数(套)', '住宅面积(平方米)', '非住宅面积（平方米）', '日期']
        self.bussinessCSV = CSVUtil('./datas/chengdu/bussiness.csv', itemNames)
        self.secondHandCSV = CSVUtil('./datas/chengdu/secondHand.csv', itemNames)

    # 下载网页
    def crawl(self, url):
        print('正在爬取: ', url)
        r = ''
        try:
            r = requests.get(url, stream=False, headers=headers, verify=False)
        except requests.exceptions.RequestException as e:
            print(e)
            print('requests error')
        return r

    # 解析网页数据
    def parse(self, html):
        soup = BeautifulSoup(html, 'lxml')
        tables = soup.find_all('table', {"class": "blank"}, recursive=True)
        if not tables and len(tables)==0:
            print('table is empty')
            return
        if len(tables) != 2:
            print('table is incomplete')
            return

        today = datetime.datetime.now().strftime('%Y%m%d')

        # 商品房今日成交
        i = 0
        for tr in tables[0].children:
            if type(tr) is bs4.element.NavigableString:
                continue
            i = i + 1
            if i < 3:
                continue
            bussinessData = []
            for td in tr.children:
                if type(td) is bs4.element.NavigableString:
                    continue
                bussinessData.append(td.text.strip())

            bussinessData.append(today)
            self.bussinessCSV.append(bussinessData)
            # print(bussinessData)

        i = 0
        # 二手房今日成交
        for tr in tables[1].children:
            if type(tr) is bs4.element.NavigableString:
                continue
            i = i + 1
            if i < 3:
                continue
            secondHandData = []
            for td in tr.children:
                if type(td) is bs4.element.NavigableString:
                    continue
                secondHandData.append(td.text.strip())

            secondHandData.append(today)
            self.secondHandCSV.append(secondHandData)
            # print(secondHandData)

    def start(self):
        print('成都%s日数据爬取开始' % datetime.datetime.now().strftime('%Y%m%d'))
        html = self.crawl(self.url)
        self.parse(html.content)
        print('成都%s日数据爬取完成'%datetime.datetime.now().strftime('%Y%m%d'))

if __name__ == "__main__":
    spider = ChengDuHouseSpider()
    spider.start()
