# ChengDuHouseSpider
用于下载成都市每日住房成交数据

成都市住房每日成交数据来自：
https://www.cdzjryb.com/SCXX/Default.aspx?action=ucEveryday2

## 其他城市住房成交数据：
杭州：http://fgj.hangzhou.gov.cn/col/col1229440802/index.html

武汉：http://data.wuhan.gov.cn/page/data/data_set.html

广州：
http://zfcj.gz.gov.cn/zfcj/tjxx/spfxstjxx            http://zfcj.gz.gov.cn/spxx_clfjyjl.html

# 配置环境：

1.安装python3.x

2.在代码根目录下安装依赖： pip install -r requirements.txt

# 手动执行：

python ChengDuHouseSpider.py

杭州的脚本：

需要下载一个Chromedriver，详细见https://zhuanlan.zhihu.com/p/373688337

# 每日定时自动执行：

1.修改daily_spider.py指定的时间

2.启动定时任务，执行python daily_spider.py
