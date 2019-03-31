# -*- coding: utf-8 -*-
import scrapy

class TestSpider(scrapy.Spider):
    name = "test_spider"
    # start_urls = ['https://www.baidu.com/']
    start_urls = ['https://www.google.com/']
    
    def parse(self, response):
        print(response.text[:1000])