# -*- coding: utf-8 -*-

BOT_NAME = 'weiboceshi_slave'

SPIDER_MODULES = ['weiboceshi_slave.spiders']
NEWSPIDER_MODULE = 'weiboceshi_slave.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32
# DOWNLOAD_DELAY = 1

DOWNLOADER_MIDDLEWARES = {
   'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None,
}

ITEM_PIPELINES = {
   'weiboceshi_slave.pipelines.WeiboceshiSlavePipeline': 300,
}

MYEXT_ENABLED = True      # 开启扩展
IDLE_NUMBER = 10           # 配置空闲持续时间单位为 360个 ，一个时间单位为5s
# 开启slave爬虫关闭扩展
EXTENSIONS = {
   'weiboceshi_slave.extensions.RedisSpiderSmartIdleClosedExensions': 500
}

REDIS_HOST = '172.16.119.6'
REDIS_PORT = 6379
REDIS_START_URLS_AS_SET = True

# # 去重类，要使用Bloom Filter请替换DUPEFILTER_CLASS
DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"
# # 散列函数的个数，默认为6，可以自行修改
BLOOMFILTER_HASH_NUMBER = 6
# # Bloom Filter的bit5数，默认30，2^30 = 10亿位=10亿/8 字节=128MB空间，去重量级1亿
BLOOMFILTER_BIT = 25
SCHEDULER = "scrapy_redis_bloomfilter.scheduler.Scheduler"
SCHEDULER_DUPEFILTER_KEY = 'weiboceshi:dupefilter'  # 去重规则，在redis中保存时对应的key

