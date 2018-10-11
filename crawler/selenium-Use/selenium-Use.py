import json
import time
from selenium import webdriver

f = open('./user.dat', 'r')
user = json.loads(f.read())
username = user['username']
password = user['password']
f.close()

# PhantomJS是一个无界面浏览器
# browser = webdriver.PhantomJS()

browser = webdriver.Chrome()
browser.get("https://qzone.qq.com/")
browser.switch_to.frame('login_frame')
browser.find_element_by_id('switcher_plogin').click()
browser.find_element_by_id('u').send_keys(username)
browser.find_element_by_id('p').send_keys(password)
browser.find_element_by_id('login_button').click()
time.sleep(2)  # 休眠一定时间,等待加载

# 如果使用PhantomJS,可以配合截图查看当前页面截图
# browser.save_screenshot("截图.png")
