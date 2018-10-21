# 获取腾讯社招数据,并使用beautifulsoup4提取期望数据
import bs4
import requests


class Tencent:
    def __init__(self):
        self.pn = int(input('请输入想要获取多少页数据'))
        self.url = 'https://hr.tencent.com/position.php?start={}'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36"
        }
        self.url_list = self.get_url_list()

    def get_url_list(self):
        # 生成链接列表
        return [self.url.format(pn) for pn in range(0, self.pn * 10, 10)]

    def run(self):
        # 获取每页数据
        for url in self.url_list:
            response = requests.get(url, headers=self.headers)
            html = response.text
            soup = bs4.BeautifulSoup(html, 'lxml')
            data_list = soup.select('.even, .odd')
            # 获取每条数据
            for data in data_list:
                # 拼接数据
                print(*([data.a.get_text()] + [td.get_text() for td in data.select('td')[1:]]))


if __name__ == '__main__':
    tencent = Tencent()
    tencent.run()
