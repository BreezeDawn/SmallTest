# 糗事百科数据提取,使用进程中的线程池Pool + bs4 + queue.Queue - 熟悉生产消费模式
import time
import requests

from queue import Queue
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool


class Qiushi:
    def __init__(self):
        self.url = 'https://www.qiushibaike.com/text/page/{}'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36"
        }
        self.pool = Pool()
        self.page_list = Queue()
        self.detail_url_list = Queue()
        self.detail_list = Queue()

    def run(self):
        self.pool.apply_async(self.get_page_url)
        self.pool.apply_async(self.get_detail_url, callback=self.call_back)
        self.pool.apply_async(self.get_detail_url, callback=self.call_back)
        self.pool.apply_async(self.get_detail, callback=self.call_back)
        self.pool.apply_async(self.get_detail, callback=self.call_back)
        self.pool.apply_async(self.get_content, callback=self.call_back)
        self.pool.apply_async(self.get_content, callback=self.call_back)
        time.sleep(3)
        self.page_list.join()
        self.detail_url_list.join()
        self.detail_list.join()

    def call_back(self, *args):
        if isinstance(*args, tuple()):
            args = args[0]
        print(args[0].__name__, '任务执行完毕')
        if len(args) != 1:
            print('--------------------录入新内容---------------------')
            print(args[1])
            print('--------------------End---------------------')
        print('开始一个新任务:', args[0].__name__)
        self.pool.apply_async(args[0], callback=self.call_back)

    def get_page_url(self):
        # 生成链接列表
        for pn in range(0, 13):
            url = self.url.format(pn + 1)
            self.page_list.put(url)

    def get_detail_url(self):
        # 获取每页的所有帖子url
        url = self.page_list.get()
        # 获取响应
        response = requests.get(url, headers=self.headers)
        html = response.content.decode()
        # 提取本页每条内容的url
        soup = BeautifulSoup(html, 'lxml')
        detail_url_list = ['https://www.qiushibaike.com' + href for href in
                           [a['href'] for a in soup.select('.contentHerf')]]
        for url in detail_url_list:
            self.detail_url_list.put(url)
        self.page_list.task_done()
        return self.get_detail_url

    def get_detail(self):
        # 获取每个详情页的内容
        url = self.detail_url_list.get()
        # 获取响应
        response = requests.get(url, headers=self.headers)
        html = response.content.decode()
        # 提取本页的详情内容
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find('div', attrs={'id': 'single-next-link'}).div.get_text()
        self.detail_list.put(content)
        self.detail_url_list.task_done()
        return self.get_detail

    def get_content(self):
        content = self.detail_list.get()
        self.detail_list.task_done()
        return self.get_content, content


if __name__ == '__main__':
    qiushi = Qiushi()
    qiushi.run()
