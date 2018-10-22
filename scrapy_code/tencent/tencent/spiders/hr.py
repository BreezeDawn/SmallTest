# -*- coding: utf-8 -*-
import scrapy

# 爬虫可以通过命令创建, 也可自己手动写
# 使用Item: 1. 导入  2. 创建对象
# 1. 导入
from tencent.items import TencentItem


class HrSpider(scrapy.Spider):
    # 爬虫名称
    name = 'hr'
    # 允许爬取域名
    allowed_domains = ['tencent.com']
    # 起始的URL列表
    start_urls = ['https://hr.tencent.com/position.php']

    def parse(self, response):
        # 获取包含招聘信息的tr列表
        # 注意: 渲染的时候, 浏览器会自动在table和tr之间生成tbody但是我们获取的响应中是没有tbody, 需要在xpath把它驱动
        # 第一行是: 表头, 最后一行是分页, 都不要
        trs = response.xpath('//*[@id="position"]/div[1]/table/tr')[1:-1]
        # print(trs)
        # 遍历 trs, 提取每一个招聘信息
        for tr in trs:
            # item = {}
            # 2. 创建TencentItem对象
            item = TencentItem()
            item['name'] = tr.xpath('./td[1]/a/text()').extract_first()
            item['category'] = tr.xpath('./td[2]/text()').extract_first()
            item['publish_time'] = tr.xpath('./td[last()]/text()').extract_first()

            # print(item)
            # 把数据交给引擎
            # yield item
            # 2. 构建详情页的请求
            # 2.1 获取详情页URL
            detail_url = 'https://hr.tencent.com/' + tr.xpath('./td[1]/a/@href').extract_first()
            # print(detail_url)
            # 2.2 构建详情页的请求, 把请求交给引擎
            # 如何实现把该解析函数中提取出来的数据, 传递到下一个解析函数呢?
            # 解决: 使用meta属性, 是一个字典
            yield scrapy.Request(detail_url, callback=self.parse_detail, meta={'item': item})


        # 实现列表翻页
        # 1. 提取下一页的URL
        next_url = response.xpath('//*[@id="next"]/@href').extract_first()
        # 如果有下一页就构建下一页请求
        if next_url != 'javascript:;':
            # 补全URL
            next_url = 'https://hr.tencent.com/' + next_url
            # print(next_url)
            # 2. 通过下一页的URL, 构建一个请求对象, 交给引擎
            # callback; 该请求对应响应数据, 在spider中解析函数(方法); 如果没有指定callback默认是parse函数
            yield scrapy.Request(next_url, callback=self.parse)

            """
             def __init__(self, url, callback=None, method='GET', headers=None, body=None,
                 cookies=None, meta=None, encoding='utf-8', priority=0,
                 dont_filter=False, errback=None, flags=None):
                 body: post请求的请求体, 格式: name=laowang&age=18
                 cookies: 是一个字典, 用于封装请求的cookie信息的
                 meta: 1. 不同解析函数数据传递 2. 设置代理IP
                 dont_filter: 该请求是否需要过滤: 如果指定为True, 就表示不过滤, 允许爬取域名 和 URL重复都不会过滤该请求
                              如果指定False, 表示该请求要过滤, 域名会过滤, 重复URL只会发送一次请求, 默认False
            """

    def parse_detail(self, response):
        # 从响应中取出, 上一个解析函数中传递过来的数据
        item = response.meta['item']
        # print(item)
        # 提取工作职责
        # 注意: 没有tbody
        item['content'] = ''.join(response.xpath('//*[@id="position_detail"]/div/table/tr[3]/td/ul/li/text()').extract())
        # print(item)
        # 把数据交给引擎
        # 如果解析函数中只有一条数据, 此时可以使用return 返回数据, 也可使用yield返回数据
        yield item
