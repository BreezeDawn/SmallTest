# -*- coding: utf-8 -*-
import re
from copy import deepcopy

import scrapy


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['suning.com']
    # 第一步:修改起始URL
    start_urls = ['http://book.suning.com/']


    def parse(self, response):
        # 提取大分类/小分类信息
        # 获取包含大分类/小分类的div里欸报
        divs = response.xpath('//div[@class="menu-item"]')
        # 获取子菜单div列表
        sub_divs = response.xpath('//div[contains(@class,"menu-sub")]')

        # 遍历divs,获取大分类/小分类信息
        for div in divs:
            item = {}
            item['b_category_name'] = div.xpath('./dl/dt/h3/a/text()').extract_first()
            item['b_category_url'] = div.xpath('./dl/dt/h3/a/@href').extract_first()

            # 获取包含小分类信息的a标签列表
            a_s = div.xpath('./dl/dd/a')
            # 如果a_s是一个空列表,就要从子菜单中提取小分类信息
            if len(a_s) == 0:
                sub_div = sub_divs[divs.index(div)]
                a_s = sub_div.xpath('./div[1]/ul/li/a')

            # 遍历a_s,提取小分类信息
            for a in a_s:
                item['s_category_name'] = a.xpath('./text()').extract_first()
                item['s_category_url'] = a.xpath('./@href').extract_first()
                # 根据小分类的url,构建列表页请求
                # 当在循环外创建的item对象,传递给下一个解析函数时候,需要进行一个深拷贝,否则数据就会错乱
                yield scrapy.Request(item['s_category_url'], callback=self.parse_book_list,
                                     meta={'item': deepcopy(item)})

    def parse_book_list(self, response):
        item = response.meta['item']
        # # 获取包含图书信息的li标签列表
        lis = response.xpath('//*[@id="filter-results"]/ul/li')
        for li in  lis:
            item['book_name'] = li.xpath('.//p[@class="sell-point"]/a/text()').extract_first()
            item['book_img'] = 'https:' + li.xpath('.//img/@src2').extract_first()
            detail_url = 'https:' + li.xpath('.//p[@class="sell-point"]/a/@href').extract_first()
            yield scrapy.Request(detail_url,callback=self.parse_book_detail,meta={"item":deepcopy(item)})

        # 实现翻页
        current_url = re.sub('(-0)+','-0',response.url)
        current_page = int(re.findall(r'param.currentPage\s*=\s*"(\d+)"', response.text)[0])
        page_numbers = int(re.findall(r'param.pageNumbers\s*=\s*"(\d+)"', response.text)[0])
        # 计算下一页的页号
        next_page = current_page + 1
        # 如果有下一页就生成下一页的url
        if next_page < page_numbers:
            # 构建下一页的URL
            # 生成替换的后缀
            subfix = '-{}.html'.format(next_page)
            next_url = re.sub('-\d+.html',subfix, current_url)
            # 构建下一页的请求
            yield scrapy.Request(next_url,callback=self.parse_book_list,meta={'item':deepcopy(item)})

    def parse_book_detail(self,response):
        item = response.meta['item']
        item['book_publisher'] = response.xpath('//*[@id="productName"]/a/text()').extract_first()

        # 准备价格url模板
        price_url = 'https://pas.suning.com/nspcsale_0_000000000{}_000000000{}_{}_20_021_0210101.html'
        # 从详情页url中提取数据
        datas = re.findall('https://product.suning.com/(\d+)/(\d+).html', response.url)[0]
        # 生成完整价格url
        price_url = price_url.format(datas[1],datas[1],datas[0])
        yield scrapy.Request(price_url,callback=self.parse_price, meta={'item':deepcopy(item)})


    def parse_price(self,response):
        """解析价格信息"""
        item = response.meta['item']
        # 有的商品有推广价格, 那么此时页面展示就是推广价格; 说明: 一般套装书使用的是推广价格
        # 我们先尝试提取推广价格
        # response.text: 响应文本字符串
        promotionPrice = re.findall('"promotionPrice":"(.+?)"', response.text)
        # 如果有推广价格, 就使用推广价格, 作为图书价格
        if promotionPrice and len(promotionPrice) != 0 and promotionPrice[0].strip() != '':
            item['price'] = promotionPrice[0]
        else:
            # 如果没有推广价格, 就使用netPrice做为价格
            item['price'] = re.findall('"netPrice":"(.+?)"', response.text)[0]
        print(item)
