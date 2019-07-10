import sys
import os
import secrets
import time
from urllib import request,error
from tqdm import tqdm
from concurrent import futures

class InsDownLoad:
    
    file_dir = './images/'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    suffixe = 'jpg'

    def save(self,workers=20):
        print('开始下载图片')
        self.pre_save()
        self.io_asy(workers=workers)
        return self

    def pre_save(self):
        self.covers_urls = self._filter(self.cover_items,size=640)
        self.image_urls = self._filter(self.post_image_urls)

        if not self.covers_urls and not self.image_urls:
            key = input('你没有采集过任何图片，是否采集后再下载？y/n:')
            if key == 'y':
                self.post_images()
                return self.pre_save()
            if key == 'n':
                self.driver.close()
        self.download_urls = self.covers_urls

        if self.image_urls:
            self.download_urls = self.image_urls

        if not os.path.exists(self.file_dir):
            self._mkdir()
        return self.download_urls

    def _mkdir(self):
        if self.file_dir[-1] != '/':
            self.file_dir += '/'
        dir_list = self.file_dir.split('/')
        first_dir = dir_list[0]
        last_dir = dir_list[-1]
        if last_dir == '':
            dir_list.remove('')
        path = first_dir + '/' # init path
        for dir in dir_list:
            if dir == first_dir:
                continue
            add_dir = dir + '/'
            path += add_dir
            os.mkdir(path)

    def _filter(self,_from,size=1080):
        urls = []
        for _ , image in _from:
            all_size_list = image.split(',')
            urls.append(all_size_list.pop().replace(f'{size}w',''))
        return urls

    def generate_file(self):
        random_hex = secrets.token_hex(8)
        rename_img = random_hex + '.' + self.suffixe # 空二进制图像文件
        return rename_img

    def download_one(self,url,index=None):
        request_url = request.Request(url,headers=self.headers)
        try:
            response = request.urlopen(request_url)
        except error.URLError as e:
            print (index,e.reason)
        filename = self.generate_file()
        filepath = self.file_dir + filename
        with open(filepath,'wb') as f:
            data = response.read()
            f.write(data)
            f.close()

    def io_blocking(self):
        '''
        IO blocking download
        '''
        for url in tqdm(self.download_urls):
            self.download_one(url)
        
    def io_asy(self,workers=20):
        '''
        asy download
        parm:workers=20
        '''
        t0 = time.time()
        with futures.ThreadPoolExecutor(workers) as executor:
            todo = []
            combo_urls = enumerate(self.download_urls,1)
            for combo_url in combo_urls:
                future = executor.submit(self.io_asy_one,combo_url)
                todo.append(future)
                # print(f'The {combo_url[0]} status:{future}')

            result = []
            tqdm_done = tqdm(futures.as_completed(todo),total=len(self.download_urls))
            for future in tqdm_done:
                res = future.result()
                # print(f'The {res} image result:{future}')
                result.append(res)
        elapsed = time.time() -t0
        # result = [self.io_asy_one,...]
        print(f'speed in {elapsed:.2f}s')

    def io_asy_one(self,url):
        index , url = url
        self.download_one(url,index=index)
        sys.stdout.flush()
        return index