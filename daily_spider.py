import schedule
from ChengDuHouseSpider import ChengDuHouseSpider
import time

def job():
    spider = ChengDuHouseSpider()
    spider.start()

schedule.every().day.at("22:00").do(job) # 每天某时间执行

print("start daily_spider")
while True:
    time.sleep(1)
    schedule.run_pending()

print("daily_spider stop")