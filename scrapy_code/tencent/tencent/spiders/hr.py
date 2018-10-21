# -*- coding: utf-8 -*-
import scrapy


class HrSpider(scrapy.Spider):
    name = 'hr'  # "爬虫名字" <爬虫启用时候使用:scrapy crawl hr>
    allowed_domains = ['tencent.com']  # 允许爬取的范围,防止爬虫爬到了别的网站
    start_urls = ['https://hr.tencent.com/position.php']  # 开始爬取的地址

    def parse(self, response):  # 数据提取方法,接收下载中间件传过来的response
        trs = response.xpath('//*[@id="position"]/div[1]/table/tr')[1:-1]
        for tr in trs:
            item = {}
            item['name'] = tr.xpath('./td[1]/a/text()').extract_first()
            item['category'] = tr.xpath('./td[2]/text()').extract_first()
            item['publish_time'] = tr.xpath('./td[last()]/text()').extract_first()
            print(item)  # 返回包含选择器的列表
