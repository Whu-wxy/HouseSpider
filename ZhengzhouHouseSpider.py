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
from config import *

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}

# 判断是否为数字
def is_number(s):
    try:    # 如果能运⾏ float(s) 语句，返回 True（字符串 s 是浮点数）
        float(s)
        return True
    except ValueError:  # ValueError 为 Python 的⼀种标准异常，表⽰"传⼊⽆效的参数"
        pass  # 如果引发了 ValueError 这种异常，不做任何事情（pass：不做任何事情，⼀般⽤做占位语句）
    try:
        import unicodedata  # 处理 ASCII 码的包
        unicodedata.numeric(s)  # 把⼀个表⽰数字的字符串转换为浮点数返回的函数
        return True
    except (TypeError, ValueError):
        pass
        return False

# 郑州按月爬
class ZhengzhouHouseSpider:
    def __init__(self):

        self.itemNames = ['全市商品房批准预售面积', '商品住宅批准预售面积', '非住宅批准预售面积',
                     '商品房（套）', '商品房面积（万平方米）', '商品房均价',
                     '商品住宅（套）', '商品住宅（万平方米）', '商品住宅均价'
                    , '非住宅（套）', '非住宅面积（万平方米）', '非住宅面积均价'
                    , '二手房（套）', '二手房面积（万平方米）', '二手房均价',
                     '住宅二手房（套）', '住宅二手房面积（万平方米）', '住宅二手房均价', '月份']
        self.dataCSV = CSVUtil(os.path.join(DATA_SAVE_PATH, 'zhengzhou/month_data.csv'), self.itemNames)

    def crawl(self, url):
        print('正在爬取: ', url)
        r = ''
        try:
            r = requests.get(url, stream=False, headers=headers, verify=False)
        except requests.exceptions.RequestException as e:
            print(e)
            print('requests error')
        return r

    def getAllData(self, page_num):
        for page in range(1, page_num+1):
            print('正在爬取页数: ', page)
            self.parsePage(page)

    def getIncrementData(self):
        pass

    # 解析一页网页数据
    def parsePage(self, page_num):

        page_data = self.crawl('https://public.zhengzhou.gov.cn/?a=path&d=19&p=D12Y&page=' + str(page_num))
        page_data = BeautifulSoup(page_data.content, 'lxml')
        month_data = page_data.find('ul', {"class": "page-list"}, recursive=True)
        for month in month_data.children:
            if type(month) is bs4.element.NavigableString:
                continue
            if month.attrs.get('href') is not None:
                month_link = month.attrs.get('href')
                # month_link = 'https://public.zhengzhou.gov.cn/D12Y/322017.jhtml'
                month_data = self.crawl(month_link)
                month_data = BeautifulSoup(month_data.content, 'lxml')

                 # 从标题中找出年月
                content_title = month_data.find('div', {"class": "content-title"})
                year_month = re.findall("\d+", content_title.text)
                year_month[1] = year_month[1] if len(year_month[1]) > 1 else '0' + year_month[1]
                year_month = year_month[0] + year_month[1]

                content = month_data.find('div', {"class": "content-txt"})
                save_data = []
                for p in content.children:
                    numbers = re.findall(r"\d+\.?\d*", p.text)
                    save_data.extend(numbers)

                save_data.append(year_month)
                if len(save_data[1:]) != len(self.itemNames):
                    print('该月份数据存在问题：', year_month)
                    # continue
                self.dataCSV.append(save_data[1:])
            # break

    def start(self):
        print('郑州%s日数据爬取开始'%datetime.datetime.now().strftime('%Y%m%d'))
        self.getAllData(8)
        print('郑州%s日数据爬取完成'%datetime.datetime.now().strftime('%Y%m%d'))


if __name__ == "__main__":
    spider = ZhengzhouHouseSpider()
    spider.start()
