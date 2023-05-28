import schedule
from ChengDuHouseSpider import ChengDuHouseSpider

def job():
    spider = ChengDuHouseSpider()
    spider.start()

schedule.every().day.at("15:33").do(job) # 每天某时间执行

while True:
    schedule.run_pending()
