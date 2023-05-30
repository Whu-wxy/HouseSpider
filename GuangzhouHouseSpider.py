from selenium import webdriver
import bs4
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import sys
import time
import re
import os
from datetime import datetime, timedelta
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
from CSVUtil import CSVUtil
# import chardet

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service

chrome_options = Options()
#chrome_options.add_argument('--headless')
options = webdriver.ChromeOptions()
options.add_argument("service_args=['–ignore-ssl-errors=true', '–ssl-protocol=TLSv1']") # Python2/3
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")

def getDriverHttp(url):
    s = Service("C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe")
    driver = webdriver.Chrome(service=s)

    soup = ''
    try:
        element = WebDriverWait(driver, 1200).until(driver.get(url))
    except Exception as e:
        print(e)
    try:
        time.sleep(3)

        WebDriverWait(driver, 30000).until(EC.visibility_of(driver.find_element(by=By.CSS_SELECTOR, value='tr[bgcolor="#ffffff"]')))

        soup = BeautifulSoup(driver.page_source, "html.parser")
    except Exception as e:
        print(e)
    return soup

class GuangzhouHouseSpider:
    def __init__(self):
        self.url = 'http://zfcj.gz.gov.cn/zfcj/tjxx/spfxstjxx'

        itemNames = ['行政区',
                     '住宅总套数', '住宅总面积',
                     '商业总套数', '商业总面积',
                     '办公总套数', '办公总面积',
                     '车位总套数', '车位总面积',
                     '日期']
        self.bussinessAvailableCSV = CSVUtil('./datas/guangzhou/bussinessAvailable.csv', itemNames)
        self.bussinessUnsoldCSV = CSVUtil('./datas/guangzhou/bussinessUnsold.csv', itemNames)
        self.bussinessSoldCSV = CSVUtil('./datas/guangzhou/bussinessSold.csv', itemNames)


    def parseAvailable(self, soup):
        tbody = soup.find('tbody', {"id": "keshou"}, recursive=True)
        trs = tbody.find_all('tr', {"bgcolor": "#ffffff"})

        today = (datetime.now() + timedelta(days=-1)).strftime('%Y%m%d')

        table = []
        for tr in trs:
            tds = tr.find_all('td')
            line = []
            for td in tds:
                line.append(td.text.strip())
            line.append(today)
            table.append(line)
            self.bussinessAvailableCSV.append(line)

        n = len(table)
        sumLine = ['全市']
        for i in range(1, n-2):
            col = [int(row[i]) for row in table]
            sumLine.append(sum(col))
        sumLine.append(today)
        self.bussinessAvailableCSV.append(sumLine)

    def parseUnsold(self, soup):
        tbody = soup.find('tbody', {"id": "weishou"}, recursive=True)
        trs = tbody.find_all('tr', {"bgcolor": "#ffffff"})

        today = (datetime.now() + timedelta(days=-1)).strftime('%Y%m%d')

        table = []
        for tr in trs:
            tds = tr.find_all('td')
            line = []
            for td in tds:
                line.append(td.text.strip())
            line.append(today)
            table.append(line)
            self.bussinessUnsoldCSV.append(line)

        n = len(table)
        sumLine = ['全市']
        for i in range(1, n-2):
            col = [int(row[i]) for row in table]
            sumLine.append(sum(col))
        sumLine.append(today)
        self.bussinessUnsoldCSV.append(sumLine)

    def parseSold(self, soup):
        tbody = soup.find('tbody', {"id": "qianyue"}, recursive=True)
        trs = tbody.find_all('tr', {"bgcolor": "#ffffff"})

        today = (datetime.now() + timedelta(days=-1)).strftime('%Y%m%d')

        table = []
        for tr in trs:
            tds = tr.find_all('td')
            line = []
            for td in tds:
                line.append(td.text.strip())
            line.append(today)
            table.append(line)
            self.bussinessSoldCSV.append(line)

        n = len(table)
        sumLine = ['全市']
        for i in range(1, n-2):
            col = [int(row[i]) for row in table]
            sumLine.append(sum(col))
        sumLine.append(today)
        self.bussinessSoldCSV.append(sumLine)

    def start(self):
        print('广州%s日数据爬取开始'%datetime.now().strftime('%Y%m%d'))
        soup = getDriverHttp(self.url)

        self.parseAvailable(soup)
        self.parseUnsold(soup)
        self.parseSold(soup)

        print('广州%s日数据爬取完成'%datetime.now().strftime('%Y%m%d'))


if __name__ == "__main__":
    spider = GuangzhouHouseSpider()
    spider.start()
