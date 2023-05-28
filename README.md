# ChengDuHouseSpider
用于下载成都市每日住房成交数据

每日成交数据来自：https://www.cdzjryb.com/SCXX/Default.aspx?action=ucEveryday2

# 配置环境：

1.安装python3.x

2.在代码根目录下安装依赖： pip install -r requirements.txt

# 手动执行：

python ChengDuHouseSpider.py

# 每日定时自动执行：

1.修改daily_spider.py指定的时间

2.启动定时任务，执行python daily_spider.py
