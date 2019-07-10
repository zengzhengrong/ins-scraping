## Introduction

scraping ins by python and selenium

## Features
- Simulated operation
- OOP
- Export excel
- multi-thread download


## Usage

Requirement：python >= 3.6 and selenium   
Requires a driver to interface with the chosen browser-[link](https://selenium-python.readthedocs.io/installation.html)  
Chrome driver has been in this repo（windows and mac）,if driver not working , to choose Compatible version-[link](https://sites.google.com/a/chromium.org/chromedriver/downloads)  


Install requirements

```
pip install -r requirements.txt
```
### followers & following
Run Script ```run.py```
or python shell on this repo directory：
```
from core.info import InsInfo
ins = InsInfo('your username','yourpassword',nickname='ins-username')

ins.login().export_all()
```
Enter any key to continue because data was no scraped , if do no Interact with the shell ：  
```
ins.login().followers().combo().following().export_all()
```
Change the order：
```
ins.login().following().combo().followers().export_all()
```
Use one type（following）:
```
ins.login().following().export_following() 
# or
ins.login().export_following() 
```
function of export_* have a args ```dest_filename``` to specified file path
### Images

Two main types of  scraping images
- Cover images（fast,Incomplete）
- Post images（slow）

Cover：

```
ins.login().covers().save() # download image
# or 
ins.login().covers().export_covers() # infomation export excel 
```

Post：

```
ins.login().post_images().save() 
```

save function args workers,default 20```save(workers=20)```  
more workers would improve concurrent performance

### Other

Slideshow

```
ins.login().covers().show_covers_broswer()
```
**```anon=True``` as well in some case**
```
ins.login(anon=True).covers().show_covers_broswer()
```

###  Custom class

e.g: override ```save```

run.py
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