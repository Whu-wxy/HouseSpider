#-*- coding:utf-8 -*-
from selenium import webdriver
import bs4
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import sys
import time
import re
import os
import datetime
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
from CSVUtil import CSVUtil
from config import *

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
        time.sleep(6)
        # iframes = driver.find_elements(by=By.TAG_NAME, value='iframe')
        # iframe = iframes[0]
        # driver.switch_to.frame(iframe)                          # 最重要的一步

        WebDriverWait(driver, 10000).until(EC.visibility_of(driver.find_element(by=By.CLASS_NAME, value='box3_tab')))

        soup = BeautifulSoup(driver.page_source, "html.parser")
    except Exception as e:
        print(e)
    return soup

class HangzhouHouseSpider:
    def __init__(self):
        self.url = 'https://zwfw.fgj.hangzhou.gov.cn/hzfcweb_ifs/interaction/scxx'

        itemNames = ['套数(套)', '总面积（平方米）', '住宅套数(套)', '住宅面积(平方米)', '日期']
        itemNames2 = ['房屋用途', '成交套数', '成交面积', '日期']
        self.secondHandCSV = CSVUtil(os.path.join(DATA_SAVE_PATH, 'hangzhou/secondHand.csv'), itemNames)
        self.bussinessCSV = CSVUtil(os.path.join(DATA_SAVE_PATH, 'hangzhou/bussiness.csv'), itemNames2)

    # 解析网页数据
    # 二手房今日成交
    def parseSecondHand(self, soup):
        secondHandDiv = soup.find('div', {"class": "box3_tab"}, recursive=True)
        secondHandTotal = secondHandDiv.find('div', {"class": "total"}, recursive=True)
        secondHandDatas = secondHandTotal.find_all('span', recursive=True)

        today = datetime.datetime.now().strftime('%Y%m%d')

        i = 0
        secondHandData = []

        for span in secondHandDatas:
            if type(span) is bs4.element.NavigableString:
                continue
            i = i + 1
            if i < 2:
                continue

            data = span.text.strip()
            if i == 2 or i == 4:
                data = data[:-1]
            if i == 3 or i == 5:
                data = data[:-2]
            secondHandData.append(data)

        secondHandData.append(today)
        self.secondHandCSV.append(secondHandData)

    def parseBussiness(self, soup):
        bussinessDiv = soup.find('div', {"class": "E_table1"}, recursive=True)
        secondHandTr = bussinessDiv.find_all('tr', recursive=True)
        # secondHandDatas = secondHandTotal.find_all('span', recursive=True)

        today = datetime.datetime.now().strftime('%Y%m%d')

        i = 0
        for tr in secondHandTr:
            if type(tr) is bs4.element.NavigableString:
                continue
            i = i + 1
            if i < 2:
                continue

            tds = tr.find_all('td', recursive=True)
            j = 0
            bussinessData = []
            for td in tds:
                data = td.text.strip()
                if j == 1:
                    data = data[:-1]
                if j == 2:
                    data = data[:-2]
                j = j + 1
                bussinessData.append(data)
            bussinessData.append(today)
            self.bussinessCSV.append(bussinessData)

    def start(self):
        print('杭州%s日数据爬取开始'%datetime.datetime.now().strftime('%Y%m%d'))
        soup = getDriverHttp(self.url)

        self.parseSecondHand(soup)
        self.parseBussiness(soup)
        print('杭州%s日数据爬取完成'%datetime.datetime.now().strftime('%Y%m%d'))


if __name__ == "__main__":
    spider = HangzhouHouseSpider()
    spider.start()
