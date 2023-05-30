import schedule
from ChengDuHouseSpider import ChengDuHouseSpider
from HangzhouHouseSpider import HangzhouHouseSpider
from GuangzhouHouseSpider import GuangzhouHouseSpider
import time

def chengduTask():
    spider = ChengDuHouseSpider()
    spider.start()
def hangzhouTask():
    spider = HangzhouHouseSpider()
    spider.start()

def guangzhouTask():
    spider = GuangzhouHouseSpider()
    spider.start()

schedule.every().day.at("22:00").do(chengduTask) # 每天某时间执行
schedule.every().day.at("22:01").do(hangzhouTask) # 每天某时间执行
schedule.every().day.at("22:02").do(guangzhouTask) # 每天某时间执行

print("start daily_spider")
while True:
    time.sleep(1)
    schedule.run_pending()

print("daily_spider stop")