import schedule
from ChengDuHouseSpider import ChengDuHouseSpider


def job():
    spider = ChengDuHouseSpider()
    spider.start()

schedule.every().day.at("15:33").do(job) # 每天某时间执行

# while True:
#     time.sleep(61)
#     time_now = time.strftime("%H%M", time.localtime())
#     if time_now == "16:01": # 设置要执行的时间:
#         # 要执行的代码
#         time.sleep(61) # 停止执行61秒，防止反复运行程序。
#         spider = ChengDuHouseSpider()
#         spider.start()


while True:
    schedule.run_pending()
    