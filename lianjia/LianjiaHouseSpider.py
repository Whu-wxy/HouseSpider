import requests
from lxml import etree
from tqdm import tqdm
import time
import random
import pandas as pd
import re
import os


class LianjiaHouseSpider:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'dtSessionId': 'nfqhu3qjvmilibolq3f'
        }
        self.filepath = './datas/chengduSecondHand.csv'
        self.maxPage = 51

        self.qu = ['jinjiang', 'wuhou', 'gaoxin', 'qingyang', 'jinniu', 'chenghua', 'tianfuxinqu']
        self.qu2 = ['锦江', '武侯', '高新', '青羊', '金牛', '成华', '天府新区']

        self.xiaoqu_list = []
        self.quyu_list = []
        self.huxing_list = []
        self.mianji_list = []
        self.chaoxiang_list = []
        self.zhuangxiu_list = []
        self.louceng_list = []
        self.build_time_list = []
        self.price_list = []
        self.unitPrice_list = []
        self.intro_list = []
        self.tihu_list = []
        self.dianti_list = []
        self.fangwu_list = []


    # 获取有“房屋卖点”等数据
    def get_intro(self, url):
        r = requests.get(url, headers=self.headers).text
        s = etree.HTML(r)
        intro = str(s.xpath('/html/body/div[3]/div/div/div[1]/div/text()'))  # 房屋特色介绍
        tihu = str(s.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[10]/text()'))  # 房屋梯户比例
        fangwu = str(s.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[2]/span[2]/text()'))  # 商品房or住宅房
        dianti = str(s.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li[11]/text()'))  # 梯户比例
        intro = intro.lstrip('[\'')
        intro = intro.rstrip('\']')
        tihu = tihu.lstrip('[\'')
        tihu = tihu.rstrip('\']')
        fangwu = fangwu.lstrip('[\'')
        fangwu = fangwu.rstrip('\']')
        dianti = dianti.lstrip('[\'')
        dianti = dianti.rstrip('\']')
        return intro, tihu, fangwu, dianti


    def get_content(self, qu, qu2):
        print('正在爬{}区二手房数据...'.format(qu2))
        for j in range(1, self.maxPage):
            time.sleep(round(random.uniform(1, 2), 2))
            try:
                url = 'https://cd.lianjia.com/ershoufang/' + qu + '/pg' + str(j)
                r = requests.get(url, headers=self.headers).text
                s = etree.HTML(r)
                for k in range(1, 31):  # 一页里面有30套房源
                    try:
                        xiaoqu = str(s.xpath('//*[@id="content"]/div[1]/ul/li[{}]/div[1]/div[2]/div/a[1]/text()'.format(k)))
                        xiaoqu = xiaoqu.lstrip('[\'')
                        xiaoqu = xiaoqu.rstrip('\']')
                        quyu = str(s.xpath('//*[@id="content"]/div[1]/ul/li[{}]/div[1]/div[2]/div/a[2]/text()'.format(k)))
                        quyu = quyu.lstrip('[\'')
                        quyu = quyu.rstrip('\']')
                        # 获取房型相关的数据，通过split将数据进行分割，-1表示分割次数（全部分割）
                        fangxing = str(s.xpath('//*[@id="content"]/div[1]/ul/li[{}]/div[1]/div[3]/div/text()'.format(k))).split(
                            '|', -1)
                        huxing = fangxing[0].lstrip('[\'').rstrip()
                        mianji = fangxing[1].strip()
                        chaoxiang = fangxing[2].strip()
                        zhuangxiu = fangxing[3].strip()
                        louceng = fangxing[4].strip()
                        build_time = fangxing[5].strip()
                        price = str(s.xpath('//*[@id="content"]/div[1]/ul/li[{}]/div[1]/div[6]/div[1]/span/text()'.format(k)))
                        price = price.lstrip('[\'')
                        price = price.rstrip('\']')
                        unitPrice = str(
                            s.xpath('//*[@id="content"]/div[1]/ul/li[{}]/div[1]/div[6]/div[2]/span/text()'.format(k)))
                        unitPrice = unitPrice.lstrip('[\'')
                        unitPrice = unitPrice.rstrip('\']')

                        intro_url = str(s.xpath('//*[@id="content"]/div[1]/ul/li[{}]/div[1]/div[1]/a/@href'.format(k)))
                        # 一定要将中括号和单引号去掉才能正常爬取数据。
                        intro_url = intro_url.lstrip('[\'')
                        intro_url = intro_url.rstrip('\']')
                        intro, tihu, fangwu, dianti = self.get_intro(intro_url)
                        self.xiaoqu_list.append(xiaoqu)
                        self.quyu_list.append(quyu)
                        self.huxing_list.append(huxing)
                        self.mianji_list.append(mianji)
                        self.chaoxiang_list.append(chaoxiang)
                        self.zhuangxiu_list.append(zhuangxiu)
                        self.louceng_list.append(louceng)
                        self.build_time_list.append(build_time)
                        self.price_list.append(price)
                        self.unitPrice_list.append(unitPrice)
                        self.intro_list.append(intro)
                        self.tihu_list.append(tihu)
                        self.dianti_list.append(dianti)
                        self.fangwu_list.append(fangwu)
                    except Exception as r:
                        print('异常:', r)
                        continue
            except Exception as r:
                print('异常:', r, '\n异常页码：', j)
                continue

            print('[{}区]：第{}/{}页'.format(qu2, j, self.maxPage))
            self.writeToCSV(qu2)
            self.reset()


    def reset(self):
        self.xiaoqu_list = []
        self.quyu_list = []
        self.huxing_list = []
        self.mianji_list = []
        self.chaoxiang_list = []
        self.zhuangxiu_list = []
        self.louceng_list = []
        self.build_time_list = []
        self.price_list = []
        self.unitPrice_list = []
        self.intro_list = []
        self.tihu_list = []
        self.dianti_list = []
        self.fangwu_list = []

    def writeToCSV(self, qu):
        infos = {'小区': self.xiaoqu_list,
                 '区域': self.quyu_list,
                 '所属区': [qu] * len(self.xiaoqu_list),
                 '户型': self.huxing_list,
                 '面积': self.mianji_list,
                 '朝向': self.chaoxiang_list,
                 '装修': self.zhuangxiu_list,
                 '楼层': self.louceng_list,
                 '建造时间': self.build_time_list,
                 '总价': self.price_list,
                 '单价': self.unitPrice_list,
                 '房屋卖点': self.intro_list,
                 '梯户比例': self.tihu_list,
                 '是否有电梯': self.dianti_list,
                 '房屋属性': self.fangwu_list}

        data = pd.DataFrame(infos,
                            columns=['小区', '区域', '所属区', '户型', '面积', '朝向', '装修', '楼层', '建造时间', '总价', '单价',
                                     '房屋卖点', '梯户比例', '是否有电梯', '房屋属性'])
        data.to_csv(self.filepath, mode='a', header=False)

    # 数据获取并保存
    def start(self):

        if not os.path.exists(os.path.dirname(self.filepath)):
            os.makedirs(os.path.dirname(self.filepath))

        if not os.path.exists(self.filepath):
            data = pd.DataFrame(None,
                                columns=['小区', '区域', '所属区', '户型', '面积', '朝向', '装修', '楼层', '建造时间', '总价', '单价',
                                         '房屋卖点', '梯户比例', '是否有电梯', '房屋属性'])
            data.to_csv(self.filepath)
        else:
            print('CSV文件已存在，无需创建:', self.filepath)

        for i in range(1, len(self.qu)):
            self.get_content(self.qu[i], self.qu2[i])



if __name__ == '__main__':
    spider = LianjiaHouseSpider()
    spider.start()
