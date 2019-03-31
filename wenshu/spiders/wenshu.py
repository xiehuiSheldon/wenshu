# -*- coding: utf-8 -*-
import re
import json
import scrapy
from scrapy.selector import Selector
from ..items import WenshuItem

class WenshuSpider(scrapy.Spider):
    name = "wenshu"
    allowed_domains = ['wenshu.court.gov.cn']
    
    def start_requests(self):
        first_url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={doc_id}'       
        doc_id = '029bb843-b458-4d1c-8928-fe80da403cfe'
        url = first_url.format(doc_id=doc_id)
        yield scrapy.Request(url, method='POST')
        
    def parse(self, response):
        mytext = response.text

        caseinfo_pattern = re.compile('JSON.stringify\(({.*?})\)')

        case_info = re.search(caseinfo_pattern, mytext).group(1)

        case_info_json = json.loads(case_info)
        # case_info_json['案件名称']

        jsonHtmlData_pattern = re.compile('jsonHtmlData.+?({.+?})')

        jsonHtmlData = re.search(jsonHtmlData_pattern, mytext).group(1)

        html_text_pattern = re.compile('\\\\"Html\\\\":\\\\"(.+?)\\\\"')

        html_text = re.search(html_text_pattern, jsonHtmlData).group(1)
  
        selector = Selector(text=html_text)

        html_t = selector.xpath('//text()')
        
        wenshu = ''
        for each in html_t.extract():
            wenshu += each + '\n'
            
        wenshu_item = self.generate_wenshu(case_info_json, wenshu)
        yield wenshu_item
            
            
    def generate_wenshu(self, case_info_json, wenshu):
        wenshu_item = WenshuItem()
        wenshu_item['court_id'] = case_info_json['法院ID']
        wenshu_item['case_base'] = case_info_json['案件基本情况段原文']
        wenshu_item['attached_original'] = case_info_json['附加原文']
        wenshu_item['judicial_procedure'] = case_info_json['审判程序']
        wenshu_item['case_number'] = case_info_json['案号']
        wenshu_item['reason_no_open'] = case_info_json['不公开理由']
        wenshu_item['court_city'] = case_info_json['法院地市']
        wenshu_item['court_province'] = case_info_json['法院省份']
        wenshu_item['head_original'] = case_info_json['文本首部段落原文']
        wenshu_item['court_area'] = case_info_json['法院区域']
        wenshu_item['doc_id'] = case_info_json['文书ID']
        wenshu_item['case_name'] = case_info_json['案件名称']
        wenshu_item['court'] = case_info_json['法院名称']
        wenshu_item['gist_original'] = case_info_json['裁判要旨段原文']
        wenshu_item['court_county'] = case_info_json['法院区县']
        wenshu_item['compensation_wenshu'] = case_info_json['补正文书']
        wenshu_item['doc_content'] = case_info_json['DocContent']
        wenshu_item['wenshu_text_type'] = case_info_json['文书全文类型']
        wenshu_item['litigation_original'] = case_info_json['诉讼记录段原文']
        wenshu_item['result_original'] = case_info_json['判决结果段原文']
        wenshu_item['text_end_original'] = case_info_json['文本尾部原文']
        wenshu_item['pub_date'] = re.search('\d{10}', case_info_json['上传日期']).group(0)
        wenshu_item['case_type'] = case_info_json['案件类型']
        wenshu_item['participant_info'] = case_info_json['诉讼参与人信息部分原文']
        wenshu_item['wenshu_type'] = case_info_json['文书类型']
        wenshu_item['judgement_date'] = case_info_json['裁判日期']
        wenshu_item['case_close_way'] = case_info_json['结案方式']
        wenshu_item['effect_level'] = case_info_json['效力层级']
        wenshu_item['wenshu'] = wenshu
        return wenshu_item