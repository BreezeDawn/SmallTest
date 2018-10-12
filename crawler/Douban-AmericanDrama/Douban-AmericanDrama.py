import csv
import time

import jsonpath
import requests


class Douban:
    def __init__(self):
        self.url = 'https://movie.douban.com/j/search_subjects?' \
                   'type=tv&tag=%E7%BE%8E%E5%89%A7&sort=recommend&page_limit=20&page_start={}'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36"
        }
        self.num = 0
        self.writer = None

    def run(self):
        f = open('./Douban-AmericanDrama.csv', 'w')
        self.writer = csv.writer(f)
        self.writer.writerow(['title', 'rate', 'url', 'cover'])
        while True:
            # 发起请求,得到响应
            response = requests.get(self.url.format(self.num))
            # json字符串进行解析,响应数据可以直接使用json()解析
            json_dict = response.json()  # type:dict
            # 拿到数据
            subjects = json_dict.get('subjects')
            # 处理数据
            if not subjects:
                f.close()
                return
            map_res = map(self.write_in_csv, subjects)
            print(list(map_res)[0])

            self.num += 20
            time.sleep(0.5)

    def write_in_csv(self, subject):
        # jsonpath 解析数据
        title = jsonpath.jsonpath(subject, "$.title")[0]
        rate = jsonpath.jsonpath(subject, "$.rate")[0]
        url = jsonpath.jsonpath(subject, "$.url")[0]
        cover = jsonpath.jsonpath(subject, "$.cover")[0]
        # 组织数据
        row = [title, rate, url, cover]
        # csv 录入数据
        self.writer.writerow(row)
        return '第%d页录入完成' % (self.num / 20)


if __name__ == '__main__':
    douban = Douban()
    douban.run()
