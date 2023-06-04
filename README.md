# HouseSpider
用于下载每日住房成交数据

## 住房销售数据来源：
成都市住房每日成交数据：
https://www.cdzjryb.com/SCXX/Default.aspx?action=ucEveryday2

杭州：http://fgj.hangzhou.gov.cn/col/col1229440802/index.html

武汉：http://data.wuhan.gov.cn/page/data/data_set.html

广州：
http://zfcj.gz.gov.cn/zfcj/tjxx/spfxstjxx            http://zfcj.gz.gov.cn/spxx_clfjyjl.html

链家二手房数据：
https://cd.lianjia.com/ershoufang/wuhou/

北京：
http://bjjs.zjw.beijing.gov.cn/eportal/ui?pageId=307749

深圳：
http://zjj.sz.gov.cn/xxgk/ztzl/pubdata/index.html

上海：
http://www.fangdi.com.cn/trade/trade.html

# 配置环境：

1.安装python3.x

2.在代码根目录下安装依赖： pip install -r requirements.txt

# 手动执行：

python ChengDuHouseSpider.py

杭州、广州的脚本：

需要下载一个Chromedriver，详细见https://zhuanlan.zhihu.com/p/373688337

# 每日定时自动执行：

1.修改daily_spider.py指定的时间

2.启动定时任务，执行python daily_spider.py

3.（可选）加入开启自启动项中，开机时自动运行，防止忘记。

**以win10为例：**

将daily_spider.bat文件复制到windows目录（C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp）下，可能杀毒软件会阻止，选择允许，重启电脑。

注：开机自启以后会打开一个cmd窗口，关闭窗口，python程序将停止运行。
