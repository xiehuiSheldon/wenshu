# -*- coding: utf-8 -*-
import re
import random
import requests
import logging
import pickle
from urllib.parse import unquote
from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.python import global_object_name

from ip_port.get_zhima import get_zhima_proxy

from wenshu.spiders.court_tree_content import CourtTreeContentSpider

logger = logging.getLogger(__name__)


class MyRetryMiddleware(RetryMiddleware):
    def __init__(self, settings):
        RetryMiddleware.__init__(self, settings)
        self.cant_retry_formdata_set = set()
        
    def delete_proxy(self, proxy):
        # return requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
        # print("我删除的是：" + proxy)
        if re.search('\d+\.\d+\.\d+\.\d+:\d+', proxy):
            proxy = re.search('\d+\.\d+\.\d+\.\d+:\d+', proxy).group()
            return requests.get("http://118.24.52.95:5010/delete/?proxy={}".format(proxy))
        
    @classmethod
    def from_crawler(cls, crawler):
        s = cls(crawler.settings)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s
            
    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1

        retry_times = self.max_retry_times

        if 'max_retry_times' in request.meta:
            retry_times = request.meta['max_retry_times']

        stats = spider.crawler.stats
        if retries <= retry_times:
            logger.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            # 修改2
            # http_proxy = request.meta.get('http_proxy')
            # self.delete_proxy(http_proxy)
            
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust

            if isinstance(reason, Exception):
                reason = global_object_name(reason.__class__)

            stats.inc_value('retry/count')
            stats.inc_value('retry/reason_count/%s' % reason)
            return retryreq
        else:
            # 修改1
            formdata = unquote(request.body.decode('utf-8'))
            http_proxy = request.meta.get('http_proxy')
            self.cant_retry_formdata_set.add(formdata + ' ' + http_proxy)
            # print(formdata + ' ' + http_proxy)
            
            stats.inc_value('retry/max_reached')
            logger.debug("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
        
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
        
    def spider_closed(self, spider):
        with open("formdata/cant_retry_formdata_set.pkl", "wb") as pkl_file:
            pickle.dump(self.cant_retry_formdata_set, pkl_file)
        



class MyHttpProxyMiddleware(object):

    def get_proxy(self):
        # ip_port = requests.get("http://127.0.0.1:5010/get/").content.decode('utf-8')
        ip_port = requests.get("http://118.24.52.95:5010/get/").content.decode('utf-8')
        if re.search('\d+\.\d+\.\d+\.\d+:\d+', ip_port):
            return re.search('\d+\.\d+\.\d+\.\d+:\d+', ip_port).group()
        else:
            return None
    
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s       
        
    def process_request(self, request, spider):
        ip_port = random.choice(get_zhima_proxy('ip_port/zhima.txt'))
        if ip_port:
            request.meta['http_proxy'] = "http://{}".format(ip_port)
            # print(request.meta['http_proxy'])
        return None
               
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
        
        
        


class DedupDownloaderMiddleware(object):

    def __init__(self):
        self.formdata_set = set()

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s
                

    def process_request(self, request, spider):
        if isinstance(spider, CourtTreeContentSpider):
            formdata = unquote(request.body.decode('utf-8'))
            if formdata in self.formdata_set and not request.meta.get('retry_times', 0):
                raise IgnoreRequest("这个请求已经爬过了：" + formdata)
                
            self.formdata_set.add(formdata)
        return None
        

    def process_exception(self, request, exception, spider):
        return None

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)