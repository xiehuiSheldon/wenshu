# -*- coding: utf-8 -*-
import datetime

BOT_NAME = 'wenshu'

SPIDER_MODULES = ['wenshu.spiders']
NEWSPIDER_MODULE = 'wenshu.spiders'


# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# HTTPERROR_ALLOWED_CODES = [400]

MYSQL_DB_NAME = 'wenshu_web'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '666666'

ITEM_PIPELINES = {
    'wenshu.pipelines.MySQLAsyncPipeline': 300,
}

DOWNLOAD_DELAY = 5
RETRY_TIMES = 4
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'

DOWNLOADER_MIDDLEWARES = {   
    'wenshu.middlewares.DedupDownloaderMiddleware': 200,
    'wenshu.middlewares.MyHttpProxyMiddleware': 1,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'wenshu.middlewares.MyRetryMiddleware': 500,
}

t = datetime.datetime.now()
LOG_FILE = 'log_files/log' + str(t)[:10] + '_' + str(t)[11:13] + '_' + str(t)[14:16] + '.txt'