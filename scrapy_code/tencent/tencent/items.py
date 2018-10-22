# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

"""
Item: 用于定义爬虫提取哪些字段

1. 提高代码可读性
2. 避免低级错误 : 只有定义的字段才能使用

使用与字典基本是一致. 

"""

class TencentItem(scrapy.Item):
    # define the fields for your item here like:
    # 用于定义Item中包含的字段, 只有定义的字段才能使用
    name = scrapy.Field() # 职位名称
    category = scrapy.Field()  # 分类
    publish_time = scrapy.Field() # 发布时间
    # 1. 增加工作职责
    content = scrapy.Field()

