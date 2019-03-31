# -*- coding: utf-8 -*-
import re
import json
import scrapy
from scrapy.selector import Selector
from ..items import KeywordItem
from ..items import CaseReasonItem

class TreeContentSpider(scrapy.Spider):
    name = "tree_content"
    allowed_domains = ['wenshu.court.gov.cn']
    
    def start_requests(self):
        url = 'http://wenshu.court.gov.cn/List/TreeContent'
        formdata = {'Param': '案件类型:行政案件'}
        yield scrapy.FormRequest(url, method='POST', formdata=formdata)
    
    def parse(self, response):
        mytext = response.text

        myjson = json.loads(mytext)
        myjson = json.loads(myjson)
        
        mykeywords = myjson[0]['Child']
        for mykeyword in mykeywords:
            keyword_item = KeywordItem()
            keyword_item['keyword'] = mykeyword['Key']
            keyword_item['keyword_value'] = mykeyword['Value']
            keyword_item['case_type_id'] = 3
            yield keyword_item
            
        url = 'http://wenshu.court.gov.cn/List/ReasonTreeContent'
        formdata = {
            'Param': '案件类型:行政案件,二级案由:行政管理范围',
            'parval': '行政管理范围'
        }
        yield scrapy.FormRequest(url, method='POST', formdata=formdata, callback=self.parse_case_reason)
        
    def parse_case_reason(self, response):
        mytext = response.text

        myjson = json.loads(mytext)
        myjson = json.loads(myjson)
        
        mycase_reasons = myjson[0]['Child']
        for mycase_reason in mycase_reasons:
            case_reason_item = CaseReasonItem()
            case_reason_item['case_reason'] = mycase_reason['Key']
            case_reason_item['case_reason_value'] = mycase_reason['Value']
            case_reason_item['case_type_id'] = 3
            yield case_reason_item