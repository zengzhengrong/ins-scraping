from core.info import InsInfo

        
if __name__ == "__main__":
    username = input('输入你的ins账号：')
    password = input('输入你的password：')
    target = input('输入需要爬取的用户：')

    ins = InsInfo(username,password,nickname=target)
    ins.login().followers().combo().following().export_all().combo().post_images().save()
    input('采集已结束,输入任意键退出:')
    ins.driver.close()