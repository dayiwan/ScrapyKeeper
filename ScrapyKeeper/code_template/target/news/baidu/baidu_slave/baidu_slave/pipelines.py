# -*- coding: utf-8 -*-
import redis
import json
from .items import BaiduSlaveDetailItem
from .mysql_db.tables import Content
from .mysql_db.operate import session
import logging



class BaiduSlaveItemPipeline(object):
    def __init__(self, redis_host, redis_port):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_name = "baidu"

    @classmethod
    def from_crawler(cls, crawler):
        """
        功能: scrapy为我们访问settings提供了这样的一个方法，这里，
        我们需要从需要从settings.py文件中，文件中，取得数据库的URI和数据库名称
        """

        # redis的配置
        REDIS_HOST = crawler.settings.get('REDIS_HOST', None)
        REDIS_PORT = crawler.settings.get('REDIS_PORT', None)

        if all([REDIS_HOST, REDIS_PORT]):
            return cls(redis_host=REDIS_HOST, redis_port=REDIS_PORT)
        else:
            raise ValueError('No param_config Redis connection setting !'
                             ' settings.py 中 Redis 的连接信息未正确配置')

    def open_spider(self, spider):
        """
        爬虫一旦开启，就会实现这个方法，连接到数据库
        :param spider:
        :return:
        """
        try:
            self.rediscli = redis.Redis(host=self.redis_host, port=self.redis_port, db=0)
            self.session = session
        except ConnectionError:
            raise ConnectionError('Cannot connect Redis & MYSQL ! 无法连接Redis和MYSQL')

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        """
        功能: 数据清洗并保存每个实现保存的类里面必须都要有这个方法,且名字固定, 用来具体实现怎么保存
        :param item: item对象
        :param spider: spider对象
        :return: item
        """
        try:
            # 如果为详情页的item，则保存数据至mysql， 同时向redis数据库的详情页集合中添加记录， 用于去重
            if isinstance(item, BaiduSlaveDetailItem):
                obj = Content()
                for k, v in item.items():
                    setattr(obj, k, v)
                self.session.add(obj)
                self.session.commit()
            else:
                info_urls = item.get('url')
                self.rediscli.sadd(self.redis_name, json.dumps({'url': info_urls}))
        except:
            logging.error("数据存储错误！")
            self.session.rollback()

