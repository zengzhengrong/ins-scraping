import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import platform



class InsLogin:
    '''
    home:
        https://www.instagram.com
    xpath:

        login_link:
        //a[@href="/accounts/login/?source=auth_switcher"]
        
        login_form:
        //input[@name="username"]
        //input[@name="password"]

        login_submit_button:
        //button[@type="submit"]

        skip:
        //button[@class="aOOlW   HoLwm "]
    '''

    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.driver = self.get_os
        self.driver.get('https://www.instagram.com')
        
    @property
    def get_os(self):
        OS_name = platform.system()
        # print(OS_name)
        if OS_name == 'Windows':
            driver = webdriver.Chrome('./chromedriver.exe')
        elif OS_name == 'Darwin': # Mac OS
            driver = webdriver.Chrome('./chromedriver')
        return driver

    def click_login_link(self):
        xpath='//a[@href="/accounts/login/?source=auth_switcher"]'

        login_url = self.driver.find_element_by_xpath(xpath)
        login_url.click()
        time.sleep(1)
    
    def input_loginform(self):
        # send username
        xpath_username='//input[@name="username"]'
        xpath_password='//input[@name="password"]'

        username = self.driver.find_element_by_xpath(xpath_username)
        username.clear()
        username.send_keys(self.username)
        
        # sleep 1s 
        time.sleep(1)

        # send password
        password = self.driver.find_element_by_xpath(xpath_password)
        password.clear()
        password.send_keys(self.password)

    def click_login_button(self):

        xpath='//button[@type="submit"]'

        login_button = self.driver.find_element_by_xpath(xpath)
        login_button.click()
        time.sleep(5)

    def skip(self):
        xpath='//button[@class="aOOlW   HoLwm "]'


        ins =  self.driver.get('https://www.instagram.com')
        time.sleep(1)
        if ins is None:
            skip = self.driver.find_element_by_xpath(xpath)
            skip.click()
    
    def required_valid(self,error=False):

        xpath = '//div[@class="x8k0n "]'
        send_xpath = '//button[@class="_5f5mN       jIbKX KUBKM      yZn4P   "]'
        submit_xpath = '//button[@class="_5f5mN       jIbKX KUBKM      yZn4P   "]'
        input_xpath = '//input[@name="security_code"]'
        input_error_xpath = '//div[@id="form_error"]'
        current_url = self.driver.current_url

        if 'challenge' in current_url:
            if not error:
                select = self.driver.find_element_by_xpath(xpath)
                select.click()
                time.sleep(2)

                send_button = self.driver.find_element_by_xpath(send_xpath)
                send_button.click()
                time.sleep(2)
            
            valid_code = input('请输入手机验证码:')

            security_code = self.driver.find_element_by_xpath(input_xpath)
            security_code.send_keys(valid_code)
            time.sleep(3)

            submit_button = self.driver.find_element_by_xpath(submit_xpath)
            submit_button.click()
            time.sleep(5)
            
            try:
                form_error = self.driver.find_element_by_xpath(input_error_xpath)
            except NoSuchElementException as e:
                return True

            if form_error:
                print('手机验证码输入错误')
                security_code.clear()
                return self.required_valid(error=True)
            return True
            

    def login(self):
        self.click_login_link()
        self.input_loginform()
        self.click_login_button()
        if self.required_valid():
            print('验证成功')
        # self.skip()
        time.sleep(2)
        return True







        
        
        
