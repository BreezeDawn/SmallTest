# 每日练习,即用即更
import json
import re
import threading
import time
from queue import Queue

import requests
from bs4 import BeautifulSoup
from lxml import etree
from retrying import retry

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36"
}


# 1.转换cookie为字典,将字典转换为cookie
def trans_test():
    response = requests.get('http://www.xingtu.info/')
    cookies = requests.utils.dict_from_cookiejar(response.cookies)  # cookie -> dict
    print('cookie_dict:', cookies)
    cookies = requests.utils.cookiejar_from_dict(cookies)  # dict -> cookie
    print('cookie_object', cookies)

# trans_test()


# 2.使用代理(proxies指定代理,可放多个)
def proxie_test():
    proxies = {
        "http": '218.14.115.211:3128'
    }
    requests.get('http://www.xingtu.info/', headers=headers, proxies=proxies)

# proxie_test()


# 3.处理证书错误(使用verify参数跳过证书验证)
def ssl_test():
    response = requests.get('https://www.12306.cn/mormhweb/', headers=headers, verify=False)
    with open('./1.html', 'wb') as file:
        file.write(response.content)

# ssl_test()


# 4.超时处理(超时会报错),并重试(retrying)
@retry(stop_max_attempt_number=3)
def retry_test():
    proxies = {
        "https": '120.33.247.207:8010'
    }
    response = requests.get('https://www.baidu.com', headers=headers, proxies=proxies, timeout=3)
    print(response.content)

# retry_test()


# 5.dump,dump2,load,loads
def json_test():
    data = json.dumps([{"a": "1"}, '3'])  # dumps-python格式转json格式

    print(json.loads(data))  # loads-json格式转python格式

    file = open('./test.dat', 'w')  # dump-向文件写入json
    json.dump(data, file)
    file.close()

    file = open('./test.dat', 'r')  # load-从文件读取json
    content = json.load(file)
    file.close()
    print(content)


# json_test()


# 6.zip(),将可迭代.的对象作为参数,将每个对象中相同下标的元素打包成一个元组，然后返回由这些元组组成的列表。
def zip_test():
    a = [1, 2, 3]
    b = [4, 5, 6]
    c = [4, 5, 6, 7, 8]

    zipped = zip(a, b)     # 打包
    print(zipped)

    print(zip(a, c))              # 列表中元素的个数与最短的列表一致

    print(zip(*zipped))          # *zipped 可理解为解压，返回二维矩阵式


# zip_test()


# 7.re(使用compile,re.S(使'.'包括换行符),re.I(忽略大小写))
def re_test():
    string = '123qwe\n123QWE'

    reg = re.compile(r'.*', re.S)  # re.S - 使'.'包括换行符
    print(reg.search(string))

    reg = re.compile(r'.*qwe.*qwe', re.S | re.I)  # re.I - 忽略大小写
    print(reg.search(string))


# re_test()


# 8.xpath
def xpath_test():
    with open('./test.html', 'r') as file:
        e = etree.HTML(file.read())
    print(e.xpath('//p'))


# xpath_test()


# 9.bs4(规则可百度css选择器)
def bs4_test():
    with open('./test.html', 'r') as file:
        html = file.read()

    soup = BeautifulSoup(html, 'lxml')
    # 标签选择器
    print(soup.a.string)  # 获取注释或内容,type:bs4对象
    print(soup.a.get_text())  # 获取内容,type:str
    print(soup.find('a'))
    print(soup.find('a', attrs={'id': 'link2'}))
    print(soup.find_all('a', attrs={'id': 'link2', 'class': 'sister'}))
    print(soup.find_all('a'))
    print(soup.find_all('a', attrs={'class': 'sister'}))
    # 类选择器
    print(soup.select('.sister'))
    print(soup.select('.sister.haha'))  # 多个类名
    print(soup.select('.sister .haha'))  # 子孙
    print(soup.select('.sister > .haha'))  # 儿子
    print(soup.select('.sister , .haha'))  # 或
    # id选择器
    print(soup.select('#link2'))
    # 属性选择器
    print(soup.select('a[id="link2"]'))
    # 层级选择器
    print(soup.select('p a'))  # 子孙
    print(soup.select('p > a'))  # 儿子
    print(soup.select('p , a'))  # 或


# bs4_test()


# 10.守护线程和守护进程(True:随着主进程结束,False:主进程结束子线程(进程)继续运行)
def daemon_test():

    def run():
        while True:
            print('1')
            time.sleep(1)

    th = threading.Thread(target=run)
    th.setDaemon(True)
    th.start()


# daemon_test()


# 11.队列使用
def queue_test():
    queue = Queue(maxsize=10)

    print('-----------程序开始------------')
    print('qsize:', queue.qsize())
    print('unfinished_tasks:', queue.unfinished_tasks)  # unfinished_tasks是Queue内部变量 - 队列中尚未结束的任务数

    print('-----------put------------')
    queue.put('1')
    print('qsize:', queue.qsize())
    print('unfinished_tasks:', queue.unfinished_tasks)

    print('-----------get------------')
    queue.get()
    print('qsize:', queue.qsize())
    print('unfinished_tasks:', queue.unfinished_tasks)

    print('-----------task_done------------')
    queue.task_done()  # unfinished_tasks - 1
    print('qsize:', queue.qsize())
    print('unfinished_tasks:', queue.unfinished_tasks)

    print('-----------join------------')
    queue.join()  # 监控unfinished_tasks,如果不为0就阻塞


# queue_test()
