import time
import json
from .excel import Excel
from .login import InsLogin
from .download import InsDownLoad
from .post import InsPost
class InfoScript:
    '''
    xpath
        following count
        '//a[@href="/{self.nickname}/following/"]//span[@class="g47SY "]'
        follower count
        '//a[@href="/{self.nickname}/followers/"]//span[@class="g47SY "]'

    '''
    time_stop = 0
    time_out = 60
    followers_names = []
    following_names = []
    
    def script(self,count,li_list,_pre=None,get_from=None):
        if get_from not in ['followers','following']:
            raise AttributeError(f'{get_from} not in follower or following')

        if get_from == 'followers':
            names = self.followers_names
        if get_from == 'following':
            names = self.following_names
        _pre = len(li_list)
        if count != len(li_list):
            
            js='document.getElementsByClassName("isgrP")[0].scrollTo(0,100000);'
            self.driver.execute_script(js)
            time.sleep(1.5)

            li_list = self.driver.find_elements_by_xpath('//div[@class="enpQJ"]')  
            print(len(li_list))
            
            self.time_stop += 1.5
            # if count mismatching  len(li_list),based len(li_list) to continue
            if _pre == len(li_list):
                count = len(li_list)

            if self.time_stop == self.time_out:
                count = len(li_list)
            return self.script(count,li_list,_pre=_pre,get_from=get_from)
        elif count == len(li_list):
            '''
            args
            .//div[@class="d7ByH"]
            .//div[@class="wFPL8 "]
            '''
            print(f'滚动已耗时：{self.time_stop}')
            print('滚动完毕，准备获取name')
            # print(li.find_element_by_xpath('.//a[@class="FPmhX notranslate _0imsa "]').text)
            for li in li_list:
                follow_nickname = li.find_element_by_xpath('.//div[@class="d7ByH"]').text
                name = follow_nickname
                approved = '无验证'
                if '\n' in follow_nickname:
                    name,approved  = follow_nickname.splitlines()

                describe = li.find_element_by_xpath('.//div[@class="wFPL8 "]').text
                name_describe = describe if describe else '无描述'

                item = (name,approved,name_describe)
                names.append(item)
                print(item)
            return names
        return None


    def change_window(self):
        size = self.driver.get_window_size()
        original_width = size.get('width')
        original_height = size.get('height')
        self.driver.set_window_size(400,800)
        return original_width , original_height
    


    def get_follow_name(self,text_xpath=None):
        
        li_xpath='//div[@class="enpQJ"]'

        # get_from type
        if 'followers' in text_xpath:
            get_from_type = 'followers'
        if 'following' in text_xpath:
            get_from_type = 'following'
        count_text = self.driver.find_element_by_xpath(text_xpath).text
        
        
        count = int(count_text)

        original_width,original_height = self.change_window()
        
        time.sleep(5)
        self.driver.set_window_size(original_width,original_height)
        time.sleep(1)
        li_list = self.driver.find_elements_by_xpath(li_xpath)
        
        names = self.script(count,li_list,get_from=get_from_type)
        return names


class CoverScript:
    '''
    Get post cover by info  
    xpath
        cover：
        //img[@class="FFVAD"]
        total post:
        //span[@class="g47SY "]
    '''

    cover_items =[]

    @property
    def total_post(self):
        post_count = self.driver.find_element_by_xpath('//span[@class="g47SY "]')
        post_count_text =  post_count.text
        return int(post_count_text)

    def math_cover(self):
        current_covers = self.driver.find_elements_by_xpath('//img[@class="FFVAD"]')
        return current_covers

    def scroll(self,count=1):
        for i in range(count):
            self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
            time.sleep(1)

    def covers(self,size=640):
        if size not in [240,480,640]:
            raise AttributeError('size argument must be 240,480 or 640')
        current_covers = self.math_cover()
        for cover in current_covers:
            srcset = cover.get_attribute('srcset')
            alt = cover.get_attribute('alt')
            describe = alt if alt else '无'

            all_size_list = srcset.split(',')
            url = all_size_list.pop().replace(f'{size}w','').strip()

            item = (describe,url)
            if item not in self.cover_items:
                # print(item)
                self.cover_items.append(item)
        self.scroll()
        self.time_stop += 1
        # print(self.time_stop)
        if self.time_stop == self.time_out:
            return self

        if len(self.cover_items) == self.total_post:
            print(f'总共：{len(self.cover_items)}个动态')
            # print(self.cover_items)
            return self
        return self.covers()

    def show_covers_broswer(self):
        '''
        Cycle cover on broswer
        '''
        covers = [cover for _ , cover in self.cover_items]
        for cover in covers:
            js=f"window.open('{cover}');"
            self.driver.execute_script(js)
            time.sleep(1)
            handles = self.driver.window_handles
            # print(handles)
            if len(handles) == 2:
                self.driver.switch_to.window(handles[-1])
                self.driver.close()
                self.driver.switch_to.window(handles[0])
        return self


class InsInfo(InsLogin,InfoScript,CoverScript,InsDownLoad,InsPost):
    '''
    xpath

        follower:
        //a[@class="-nal3 "]
        following:
        //a[@href="/pancake0203/following/"]

        following count
        '//a[@href="/{self.nickname}/following/"]//span[@class="g47SY "]'
        follower count
        '//a[@href="/{self.nickname}/followers/"]//span[@class="g47SY "]'

        close button
        '//button[@class="dCJp8 afkep _0mzm-"]'
    '''

    _following = None
    _followers = None

    def __init__(self,*args,**kwargs):
        
        super().__init__(*args)


        if 'nickname' not in kwargs:
            raise AttributeError('You must provide the nickname')
        self.nickname = kwargs.pop('nickname')
        if 'timeout' in kwargs:
            self.time_out = kwargs.pop('time_out')

    def get_follower_link(self):
        xpath='//a[@class="-nal3 "]' 

        follower_link = self.driver.find_element_by_xpath(xpath)
        follower_link.click()
        time.sleep(1)
    
    def get_following_link(self):
        xpath='//a[@href="/{}/following/"]'

        following_link = self.driver.find_element_by_xpath(xpath.format(self.nickname))
        following_link.click()
        time.sleep(1)

    def get_following_name(self):
        self.get_following_link()
        result = super().get_follow_name(text_xpath=f'//a[@href="/{self.nickname}/following/"]//span[@class="g47SY "]')
        return result

    def get_followers_name(self):
        self.get_follower_link()
        result = super().get_follow_name(text_xpath=f'//a[@href="/{self.nickname}/followers/"]//span[@class="g47SY "]')
        return result


    def following(self):
        items = self.get_following_name()
        if items:
            print(f'已获取{len(items)}个following信息')
        self._following = items
        return self


    def followers(self):
        items = self.get_followers_name()
        if items:
            print(f'已获取{len(items)}个followers信息')
        self._followers = items
        return self

    @property
    def to_info(self):
        self.driver.get(f'https://www.instagram.com/{self.nickname}/')
        time.sleep(1)
        return self

    # @property
    def login(self,anon=None):
        
        if anon:
            self.to_info
            return self
        done = super().login()
        time.sleep(1)
        if done:
            self.to_info
        return self
        
    def export_following(self,dest_filename=None):
        '''
        following execl export
        param: dest_filename = 'following'
        '''
        if not self._following:
            input('following未采集,输入任意键开始采集:')
            self.following()
        data = {
            'following':{
                'fields':['用户名','有无验证','描述'],
                'data':self._following,
            }
        }
        excel = Excel(data)
        excel.export(dest_filename)

    def export_followers(self,dest_filename=None):
        '''
        followers execl export
        param: dest_filename = 'followers'
        '''
        if not self._followers:
            input('followers未采集,输入任意键开始采集:')
            self.followers()
        data = {
            'followers':{
                'fields':['用户名','有无验证','描述'],
                'data':self._followers,
                }
            }
        excel = Excel(data)
        excel.export(dest_filename)

    # @property
    def combo(self):
        # button = self.driver.find_element_by_xpath('//button[@class="dCJp8 afkep _0mzm-"]')
        # close_button = button.find_element_by_tag_name('span')
        close_button = self.driver.find_element_by_xpath('//div[@class="WaOAr"]/button[@class="dCJp8 afkep _0mzm-"]')
        close_button.click()
        time.sleep(1)
        return self

    def export_all(self,dest_filename=None):
        if not (self._followers or self._following):
            input('未采集,输入任意键开始采集:')
            self.following().combo().followers()

        if self._followers and not self._following:
            input('following未采集,输入任意键开始采集:')
            self.to_info.following()

        if self._following and not self._followers:
            input('followers未采集,输入任意键开始采集:')
            self.to_info.followers()

        data = {
            'following':{
                'fields':['用户名','有无验证','描述'],
                'data':self._following,
                },
            'followers':{
                'fields':['用户名','有无验证','描述'],
                'data':self._followers,
                }
            }
        excel = Excel(data)
        dest_filename = dest_filename if dest_filename else self.nickname + '.xlsx'
        excel.export(dest_filename=dest_filename)
        return self

    def export_covers(self,dest_filename=None):
        if not self.cover_items:
            input('covers未采集,输入任意键开始采集')
            self.covers()
        data = {
            'covers':{
                'fields':['图片描述','图片地址'],
                'data':self.cover_items,
                }
            }
        excel = Excel(data)
        excel.export(dest_filename)
    
    def test(self):
        log_type = self.driver.log_types
        print(log_type)
        har = self.driver.get_log('driver')
        print(har)
        har = self.driver.get_log('browser')
        print(har)
        # har = self.driver.get_log('client')
        # print(har)
        har = self.driver.get_log('server')
        print(har)
