[English](https://github.com/zengzhengrong/ins-scraping/blob/master/README-English.md)

## 介绍

使用python爬取ins上用户信息

## 特性
- 采用selenium库模拟浏览器操作
- 完全采用面向对象编程
- 导出excel
- 多线程下载图片
- 模拟登陆

## 使用

要求：python >= 3.6 以及 selenium库支持浏览器的[驱动程序](https://selenium-python.readthedocs.io/installation.html)  
在本repo中已经添加了chrome的驱动程序（windows系统和mac）,如果驱动与你当前浏览器版本不兼容请自行[下载](https://sites.google.com/a/chromium.org/chromedriver/downloads)  

**重要的一点：墙内用户，需要一个良好的外网环境，至少访问ins能够畅通无阻**

安装相关依赖

```
pip install -r requirements.txt
```
### 爬取followers和following
尝试运行 run.py
或者在目录下进入python shell 运行如下代码：
```
from core.info import InsInfo
ins = InsInfo('your username','yourpassword',nickname='ins-username')

ins.login().export_all()
```
上面代码会shell中提示你没有爬取相关数据以至于没法导出数据，需要输入任意键继续，如果不想在shell中交互，可以提前采集数据：  
```
ins.login().followers().combo().following().export_all()
```
当然你也可以互换采集先后顺序：
```
ins.login().following().combo().followers().export_all()
```
只导出某个类型，例如（following）:
```
ins.login().following().export_following() 
# or
ins.login().export_following() 
```
所有export_*的方法都有一个 ```dest_filename```可选参数，用来指定文件路径。
### 爬取图片

爬取图片有两种可选
- 爬取帖子封面（速度较快）但图片不全
- 爬取帖子全部图片（速度较慢），可能会遇到网络问题

爬取封面：

```
ins.login().covers().save() # 下载图片
# or 
ins.login().covers().export_covers() #将图片信息导出excel
```

爬取全部图片：

```
ins.login().post_images().save() # 下载图片
```

save方法可选的并发参数-workers,默认是20```save(workers=50)```  
可以加大workers数量来提高并发性能，不过不建议太高，有可能被封IP

### 其他

浏览器轮播封面图

```
ins.login().covers().show_covers_broswer()
```
**有一些无需登陆的操作可以设置```login方法参数anon为True```,例如轮播封面图:**
```
ins.login(anon=True).covers().show_covers_broswer()
```

### 自定义类

这里已自定义下载为例

修改 run.py
```
from core.info import InsInfo

class MyIns(InsInfo):

    file_dir = './images/'

    def save(self, workers=20):
        urls = super().pre_save()
        for index,url in enumerate(urls):
            request.urlretrieve(url,self.file_dir + f'{index}.jpg')
        

if __name__ == "__main__":
    ins = MyIns('your-username','you-password',nickname='ins-username')
    ins.login().post_images().save()
    ins.driver.close()
```
