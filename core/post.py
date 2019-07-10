from .login import InsLogin
from selenium.common.exceptions import NoSuchElementException
import time

class InsPost:
    '''
    获取每个动态采集高清图片
    xpath
        获取第一个动态
            //div[@class="eLAPa"] 
        获取动态图片
            //div[@class="_97aPb "]
            //img[@class="FFVAD"]
        获取动态多张图片
            //button[@class="  _6CZji"]
        获取下一个动态
            //a[@class="HBoOv coreSpriteRightPaginationArrow"]
    '''
    post_image_urls = []
    image_get_error_count = 0


    def post_images(self):

        post = self.driver.find_element_by_xpath('//div[@class="eLAPa"]')
        post.click()
        time.sleep(1)
        finish = self.get_post_images()
        if finish is None:
            return True
        return self

    def get_post_images(self):

        curl = self.driver.current_url
        try:
            div = self.driver.find_element_by_xpath('//div[@class="_97aPb "]')
        except NoSuchElementException:

            if self.image_get_error_count > 10:
                print(f'获取失败，跳过该post:{curl}')
                self.image_get_error_count = 0 # 清0
                return self.click_right()

            if self.image_get_error_count > 5:
                print('尝试重新获取')
                self.click_left()
                time.sleep(3)
                self.click_right()
                self.image_get_error_count +=1

            print(f'{curl}网络出现问题，图片获取失败，等待图片显示正常')
            self.image_get_error_count += 1
            time.sleep(2)

            return self.get_post_images()

        images = div.find_elements_by_class_name("FFVAD")

        images_url = self.get_slide_image(images)
        if self.click_subright():
            images = div.find_elements_by_class_name("FFVAD")
            self.get_slide_image(images)
            return self.get_post_images()
        # print(images_url)
        print(len(images_url))
        next_post = self.click_right()
        if next_post is None:
            print(f'已无动态，采集到{len(self.post_image_urls)}图片')
            return True
        return True

    def click_subright(self):
        try:
            sub_right = self.driver.find_element_by_xpath('//button[@class="  _6CZji"]')
        except Exception as e: 
            pass
            return None
        sub_right.click()
        time.sleep(1)
        return True

    def click_left(self):
        try:
            left = self.driver.find_element_by_xpath('//a[@class="HBoOv coreSpriteLeftPaginationArrow"]')
        except Exception as e:
            pass
            return None
        left.click()
        time.sleep(1.5)
        return self.get_post_images()
        
    def click_right(self):
        try:
            right = self.driver.find_element_by_xpath('//a[@class="HBoOv coreSpriteRightPaginationArrow"]')
        except Exception as e:
            pass
            return None
        right.click()
        time.sleep(1.5)
        return self.get_post_images()

    def get_slide_image(self,images):
        for image in images:
            srcset = image.get_attribute('srcset')
            alt = image.get_attribute('alt')
            describe = alt if alt else '无'
            item = (describe,srcset)
            if item not in self.post_image_urls:
                self.post_image_urls.append(item)
        return self.post_image_urls