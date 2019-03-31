# -*- coding: utf-8 -*-
import re
import json
import scrapy
from ..items import CourtAreaItem, CourtItem

class CourtTreeContentSpider(scrapy.Spider):
    name = "court_tree_content"
    allowed_domains = ['wenshu.court.gov.cn']
    
    def start_requests(self):
        url = 'http://wenshu.court.gov.cn/List/TreeContent'
        formdatas = [
            {'Param': '案件类型:刑事案件'},
            {'Param': '案件类型:民事案件'},
            {'Param': '案件类型:行政案件'},
            {'Param': '案件类型:赔偿案件'},
            {'Param': '案件类型:执行案件'}]
        for i, formdata in enumerate(formdatas):
            meta = {
                'case_type_id': i+1,
                'case_type': formdata['Param'],
            }
            yield scrapy.FormRequest(url, method='POST', formdata=formdata, meta=meta)
            
    def parse(self, response):
        url = 'http://wenshu.court.gov.cn/List/CourtTreeContent'
        meta = response.meta
        
        mytext = response.text

        myjson = json.loads(mytext)
        myjson = json.loads(myjson)
        
        mycourt_areas = myjson[3]['Child']
        for mycourt_area in mycourt_areas:
            court_area_item = CourtAreaItem()
            area_name = mycourt_area['Key']
            if area_name:
                court_area_item['court_area'] = area_name
                court_area_item['court_area_value'] = mycourt_area['Value']
                court_area_item['case_type_id'] = meta.get('case_type_id')
                yield court_area_item
                
                formdata = {
                    'Param': meta.get('case_type') + ',法院地域:' + area_name,
                    'parval': area_name,
                }
                yield scrapy.FormRequest(url, method='POST', formdata=formdata, meta=meta, callback=self.parse_middle_court)
                
                
    def parse_middle_court(self, response):
        url = 'http://wenshu.court.gov.cn/List/CourtTreeContent'
        meta = response.meta
        
        mytext = response.text        

        myjson = json.loads(mytext)
        myjson = json.loads(myjson)
        
        mymiddle_courts = myjson[0]['Child']
        for mymiddle_court in mymiddle_courts:
            court_item = CourtItem()
            court_name = mymiddle_court['Key']
            if court_name:
                court_item['court_name'] = court_name
                court_item['court_name_value'] = mymiddle_court['Value']
                court_item['case_type_id'] = meta.get('case_type_id')
                court_item['court_level_id'] = 3
                yield court_item
                
                formdata = {
                    'Param': meta.get('case_type') + ',中级法院:' + court_name,
                    'parval': court_name,
                }
                yield scrapy.FormRequest(url, method='POST', formdata=formdata, meta=meta, callback=self.parse_base_court)
                
    def parse_base_court(self, response):
        meta = response.meta
        
        mytext = response.text        

        myjson = json.loads(mytext)
        myjson = json.loads(myjson)
        
        mybase_courts = myjson[0]['Child']
        for mybase_court in mybase_courts:
            court_item = CourtItem()
            court_name = mybase_court['Key']
            if court_name:
                court_item['court_name'] = court_name
                court_item['court_name_value'] = mybase_court['Value']
                court_item['case_type_id'] = meta.get('case_type_id')
                court_item['court_level_id'] = 4
                yield court_item