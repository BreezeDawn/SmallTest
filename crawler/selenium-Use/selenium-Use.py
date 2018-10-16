# selenium
import time

from selenium import webdriver


def selenium_chrome_test():
    # 创建浏览器对象 (传递驱动文件路径,不传递会从 PATH 中寻找驱动文件,找不到报错)
    # 浏览器对象如果放在函数里,程序执行完毕执行完毕,python垃圾回收机制会将打开的浏览器关闭
    browser = webdriver.Chrome('./chromedriver')

    # 请求网址
    browser.get('https://www.baidu.com')

    # 两个系列
    # find_element 系列 获取符合条件的第一个元素 (WebElement 元素对象)
    # find_elements 系列 获取符合条件的所有元素 (列表)

    print(browser.page_source)
    element = browser.find_element_by_id('u1')  # 通过 id 获取
    print('获取class内容:', element.get_attribute('class'))

    browser.find_element_by_name('wd')  # 通过name属性查找

    print('标签名获取:', browser.find_element_by_tag_name('a'))

    element = browser.find_element_by_class_name('bri')  # 通过 class 名称获取
    element.click()
    print('获取text内容:', element.text)

    browser.find_element_by_link_text('地图')  # 选择符合链接文本的元素的内容搜索(完全匹配)
    browser.find_element_by_partial_link_text('图')  # 选择包含链接内容的元素内容搜索(模糊匹配)
    browser.find_element_by_xpath('//div')  # 通过xpath规则提起,只能节点选择,不支持直接获取属性和内容,仅仅提供节点选择功能
    # browser.find_element_by_css_selector()  # css样式选择器

    # 获取请求地址
    print(browser.current_url)
    # 获取响应源码
    print(browser.page_source)  # js渲染后的源码
    # cookie
    browser.get_cookie('BAIDUID')  # 获取指定cookie
    browser.get_cookies()  # 获取所有cookie
    browser.add_cookie({'name': 'a', 'value': '1'})  # 添加cookie
    print(browser.get_cookie('a'))  # 获取指定cookie,cookie中带有很多key/value
    browser.delete_all_cookies()  # 删除所有cookie
    browser.delete_cookie('a')  # 删除指定cookie

    # 执行js代码
    browser.execute_script("alert(1)")
    time.sleep(5)
    browser.close()  # 关闭浏览器


# selenium_chrome_test()


def selenium_phantomjs_test():
    # phantomjs无界面 - 官方不推荐使用,推荐使用chrome/firefox无界面显示
    # 高级使用 - 切换User-Agent/使用代理
    # PhantomJS 无界面
    browser = webdriver.PhantomJS('./phantomjs')
    # chrome 无界面
    # options = webdriver.ChromeOptions()  # 创建配置对象
    # options.add_argument('--headless')  # 开启无界面模式
    # options.add_argument('--disable-gpu')  # 禁用gpu(显卡),解决一些奇怪的问题
    # options.add_argument('--user-agent=UA内容')  # 切换User-Agent
    # options.add_argument('--proxy-server=代理服务器地址')  # 设置代理
    # browser = webdriver.Chrome('./chromedriver',chrome_options=options)
    browser.get('https://www.douban.com')
    browser.save_screenshot('1.png')  # 截图并保存
    browser.close()


# selenium_phantomjs_test()


def switch_window_test():
    # 切换选项卡,
    browser = webdriver.Chrome('./chromedriver')
    browser.get('https://www.baidu.com')
    browser.find_element_by_id('kw').send_keys('itcast')
    browser.find_element_by_id('su').click()
    time.sleep(3)
    browser.find_element_by_class_name('favurl').click()
    print(browser.window_handles)  # 不同的选项卡是存在列表里browser.window_handles
    time.sleep(1)
    browser.switch_to.window(browser.window_handles[1])  # 取下标第一个选项卡并切换
    print(browser.title)  # 打印当前选项卡标题


# switch_window_test()


def selenium_iframe_test():
    # iframe切换,qq登陆的登陆小窗口是一个frame,
    browser = webdriver.Chrome('./chromedriver')
    browser.get("https://qzone.qq.com/")
    browser.switch_to.frame('login_frame')  # 使用switch_to.frame切换frame
    browser.find_element_by_id('switcher_plogin').click()
    time.sleep(1)


# selenium_iframe_test()


def implicitly_wait_test():
    # 隐形等待和高级使用
    # 通常我们会使用time.sleep强制等待,必须够时间
    # 隐性等待,到了一定的时间发现元素还没有加载，则继续等待我们指定的时间，如果超过了我们指定的时间还没有加载就会抛出异常，如果没有需要等待的时候就已经加载完毕就会立即执行获取元素时进行等待,秒数内完成就返回数据
    # 这个是切换选项卡的代码,只是把time.sleep都去掉了,使用隐性等待
    browser = webdriver.Chrome('./chromedriver')
    browser.implicitly_wait(3)  # 隐性等待
    browser.get('https://www.baidu.com')
    browser.find_element_by_id('kw').send_keys('itcast')
    browser.find_element_by_id('su').click()
    browser.find_element_by_class_name('favurl').click()
    print(browser.window_handles)  # 不同的选项卡是存在列表里browser.window_handles
    browser.switch_to.window(browser.window_handles[1])  # 取下标第一个选项卡并切换
    print(browser.title)  # 打印当前选项卡标题


# implicitly_wait_test()


def ec_wait_test():
    # EC.presence_of_element_located() - 确认元素是否存在
    # EC.element_to_be_clickable() - 可点击的元素是否存在
    # 显示等待,指定一个等待条件，并且指定一个最长等待时间，会在这个时间内进行判断是否满足等待条件，如果成立就会立即返回，如果不成立，就会一直等待，直到等待你指定的最长等待时间，如果还是不满足，就会抛出异常，如果满足了就会正常返回
    # 显性等待-常用的判断条件：
    # title_is 标题是某内容
    # title_contains 标题包含某内容
    # presence_of_element_located 元素加载出，传入定位元组，如(By.ID, 'p')
    # visibility_of_element_located 元素可见，传入定位元组
    # visibility_of 可见，传入元素对象
    # presence_of_all_elements_located 所有元素加载出
    # text_to_be_present_in_element 某个元素文本包含某文字
    # text_to_be_present_in_element_value 某个元素值包含某文字
    # frame_to_be_available_and_switch_to_it frame加载并切换
    # invisibility_of_element_located 元素不可见
    # element_to_be_clickable 元素可点击
    # staleness_of 判断一个元素是否仍在DOM，可判断页面是否已经刷新
    # element_to_be_selected 元素可选择，传元素对象
    # element_located_to_be_selected 元素可选择，传入定位元组
    # element_selection_state_to_be 传入元素对象以及状态，相等返回True，否则返回False
    # element_located_selection_state_to_be 传入定位元组以及状态，相等返回True，否则返回False
    # alert_is_present 是否出现Alert
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as ec
    browser = webdriver.Chrome('./chromedriver')
    browser.get('https://www.taobao.com/')
    wait = WebDriverWait(browser, 10)
    inp = wait.until(ec.presence_of_element_located((By.ID, 'q')))
    button = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search')))
    print(inp, button)


# ec_wait_test()


def base_test():
    # 浏览器的前进和后退
    browser = webdriver.Chrome('./chromedriver')
    browser.back()  # 前进
    browser.forward()  # 后退
    browser.close()  # 退出当前页面
    browser.quit()  # 退出浏览器

# base_test()
