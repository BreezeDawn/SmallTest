import requests


class TiebaSpider:
    def __init__(self):
        self.kw = input('请输入想要获取的贴吧名')
        self.pn = int(input('请输入想要获取多少页数据'))
        self.url = "http://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                          " (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36"
        }
        self.url_list = self.get_url_list()

    def get_url_list(self):
        return [self.url.format(self.kw, pn) for pn in range(0, self.pn * 50, 50)]

    def run(self):
        for url in self.url_list:
            response = requests.get(url, headers=self.headers)
            with open('./' + str(self.url_list.index(url)) + '.html', 'wb') as f:
                f.write(response.content)


if __name__ == '__main__':
    spider = TiebaSpider()
    spider.run()
