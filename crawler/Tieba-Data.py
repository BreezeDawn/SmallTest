# 获取贴吧数据,并使用xpath提取期望数据
from lxml import etree
import requests


class TiebaSpider:
    def __init__(self):
        self.kw = input('请输入想要获取的贴吧名')
        self.pn = int(input('请输入想要获取多少页数据'))
        self.url = "http://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}"
        self.headers = {
            "Referer": "https: // tieba.baidu.com",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36"
        }
        self.url_list = self.get_url_list()

    def get_url_list(self):
        # 生成链接列表
        return [self.url.format(self.kw, pn) for pn in range(0, self.pn * 50, 50)]

    def run(self):
        prev_last = ''
        # 获取数据
        for url in self.url_list:
            # 获取响应
            response = requests.get(url, headers=self.headers)
            html = response.content.decode()

            # 提取本页数据
            e = etree.HTML(html)
            li_elements = e.xpath("//li[@class='tl_shadow tl_shadow_new']")

            # 判断是否尾页
            now_last = li_elements[-1].xpath(".//div[@class='ti_title']/span/text()")[0]
            if now_last == prev_last:
                print('不好意思,只有%d页' % (self.url_list.index(url)))
                return
            prev_last = now_last

            # 细分数据
            for li in li_elements:
                title = li.xpath(".//div[@class='ti_title']/span/text()")[0] if li.xpath(
                    ".//div[@class='ti_title']/span/text()") else '空标题'
                author = li.xpath(".//span[@class='ti_author']/text()|.//span[@class='ti_author ti_vip']/text()")[
                    0].replace(' ', '')
                last_reply_time = li.xpath(".//span[@class='ti_time']/text()")[0]
                relpys_num = li.xpath(".//span[@class='btn_icon']/text()")[0]
                print('标题:' + title, '作者:' + author, '最后动态时间:' + last_reply_time, '评论数:' + relpys_num)


if __name__ == '__main__':
    spider = TiebaSpider()
    spider.run()
