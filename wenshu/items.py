# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WenshuItem(scrapy.Item):
    id = scrapy.Field()
    court_id = scrapy.Field()
    case_base = scrapy.Field()
    attached_original = scrapy.Field()
    judicial_procedure = scrapy.Field()
    case_number = scrapy.Field()
    reason_no_open = scrapy.Field()
    court_city = scrapy.Field()
    court_province = scrapy.Field()
    head_original = scrapy.Field()
    court_area = scrapy.Field()
    doc_id = scrapy.Field()
    case_name = scrapy.Field()
    court = scrapy.Field()
    gist_original = scrapy.Field()
    court_county = scrapy.Field()
    compensation_wenshu = scrapy.Field()
    doc_content = scrapy.Field()
    wenshu_text_type = scrapy.Field()
    litigation_original = scrapy.Field()
    result_original = scrapy.Field()
    text_end_original = scrapy.Field()
    pub_date = scrapy.Field()
    case_type = scrapy.Field()
    participant_info = scrapy.Field()
    wenshu_type = scrapy.Field()
    judgement_date = scrapy.Field()
    case_close_way = scrapy.Field()
    effect_level = scrapy.Field()
    wenshu = scrapy.Field()

class KeywordItem(scrapy.Item):
    id = scrapy.Field()
    keyword = scrapy.Field()
    keyword_value = scrapy.Field()
    case_type_id = scrapy.Field()
    
class CaseReasonItem(scrapy.Item):
    id = scrapy.Field()
    case_reason = scrapy.Field()
    case_reason_value = scrapy.Field()
    case_type_id = scrapy.Field()
    
class CourtAreaItem(scrapy.Item):
    id = scrapy.Field()
    court_area = scrapy.Field()
    court_area_value = scrapy.Field()
    case_type_id = scrapy.Field()
    
class CourtItem(scrapy.Item):
    id = scrapy.Field()
    court_name = scrapy.Field()
    court_name_value = scrapy.Field()
    case_type_id = scrapy.Field()
    court_level_id = scrapy.Field()