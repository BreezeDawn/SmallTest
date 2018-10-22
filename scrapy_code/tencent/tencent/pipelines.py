# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TencentPipeline(object):
    def process_item(self, item, spider):

        print(item)

        return item

# 1. 使用jsonlines格式来保存数据
# 2. 使用mongodb来存储数据

"""
1. 定义管道类
2. 在setting.py文件开启
"""

# 1. 使用jsonlines格式来保存数据
import json

class TencentPipelineFile(object):

    def open_spider(self, spider):
        """
        当爬虫启动时候, 只调用一次, 在该方法中: 1. 打开文件, 建立数据连接
        :param spider:  爬虫
        :return:
        """
        if spider.name == 'hr':
            self.file = open('hr.jsonlines', 'a', encoding='utf-8')



    def process_item(self, item, spider):
        # 该方法, 引擎获取的每一条数据, 都会调用该方法, 该方法调用非常频繁
        # 如果该方法中 , 打开, 关闭文件, 非常消耗系统资源, 降低效率, 怎么办?
        # 我们希望只打开一次文件: open_spider

        # with open('hr.jsonlinse', 'a', encoding='utf8') as f:
        #     f.write()
        # 要以jsonlines写入文件, 每一行是一个json数据
        # TypeError: Object of type 'TencentItem' is not JSON serializable
        # 解决: TencentItem => dict
        if spider.name == 'hr':
            json.dump(dict(item), self.file, ensure_ascii=False)
            # 每写一条数据, 写一个换行
            self.file.write('\n')
            # print(item)
        # 注意: 一定把item数据返回, 否则后面的解析函数就获取不到数据了
        return item

    def close_spider(self, spider):
        # 当爬虫结束时候, 会执行, 只执行一次
        if spider.name == 'hr':
            self.file.close()

from tencent.spiders.hr import HrSpider
from pymongo import MongoClient

class TencentPipelineMongoDB(object):

    def open_spider(self, spider):

        if spider.name == HrSpider.name:
            # 建立MongoDB数据库连接
            self.client = MongoClient('127.0.0.1', 27017)
            # 获取要操作的集合
            self.collection = self.client['tencent']['hr']

    def process_item(self, item, spider):

        # 如果该爬虫对象, 是HrSpider
        if isinstance(spider, HrSpider):
            self.collection.insert(dict(item))
        return item

    def close_spider(self, spider):
        if spider.name == HrSpider.name:
            # 关闭数据库连接
            self.client.close()