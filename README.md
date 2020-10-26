# MyLovelyDomain
用来检测域名，获取自己喜欢的域名

### 概要设计

获取域名 -- 筛选五官端正 -- 检测历史记录 -- 过滤link114 -- 验证是否注册 -- 挑选颜值担当

### 详细设计

*一、获取域名*

- CN下载链接：[今天删除](http://www.cnnic.cn/download/registar_list/1todayDel.txt) 、[明天删除](http://www.cnnic.cn/download/registar_list/future1todayDel.txt)、[后天删除](http://www.cnnic.cn/download/registar_list/future2todayDel.txt)

二、获取历史记录

- 获取首页历史的[API]("http://web.archive.org/web/timemap/json?url={domain}/&fl=timestamp:4,timestamp,original")
- 获取子页面历史的[API]("http://web.archive.org/web/timemap/json?url={domain}/&fl=timestamp:4,timestamp,original&matchType=prefix")

- 获取详细页的内容[API]("https://web.archive.org/web/{20141218034700}/{http://puttt.com/}")，获取详细页，需要有cookie

三、过滤link114

- 可以检测被墙、QQ拦截、微信拦截：[link114](http://www.link114.cn/)

