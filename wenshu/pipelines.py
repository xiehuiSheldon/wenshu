# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
from .items import WenshuItem
from .items import KeywordItem
from .items import CaseReasonItem
from .items import CourtAreaItem
from .items import CourtItem


class WenshuPipeline(object):
    def process_item(self, item, spider):
        return item
        
        
class MySQLAsyncPipeline:
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'scrapy_default')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', 'root')
        
        self.dbpool = adbapi.ConnectionPool('pymysql', host=host, db=db, port=port,
                                            user=user, passwd=passwd, charset='utf8')
                                            
    def close_spider(self, spider):
        self.dbpool.close()
        
    def process_item(self, item, spider):
        if isinstance(item, WenshuItem):
            self.dbpool.runInteraction(self.insert_wenshu, item)
        elif isinstance(item, KeywordItem):
            self.dbpool.runInteraction(self.insert_keyword, item)
        elif isinstance(item, CaseReasonItem):
            self.dbpool.runInteraction(self.insert_case_reason, item)
        elif isinstance(item, CourtAreaItem):
            self.dbpool.runInteraction(self.insert_court_area, item)
        elif isinstance(item, CourtItem):
            self.dbpool.runInteraction(self.insert_court, item)
        return item
        
    def insert_wenshu(self, tx, item):
        values = (
            item['court_id'],
            item['case_base'],
            item['attached_original'],
            item['judicial_procedure'],
            item['case_number'],
            item['reason_no_open'],
            item['court_city'],
            item['court_province'],
            item['head_original'],
            item['court_area'],
            item['doc_id'],
            item['case_name'],
            item['court'],
            item['gist_original'],
            item['court_county'],
            item['compensation_wenshu'],
            item['doc_content'],
            item['wenshu_text_type'],
            item['litigation_original'],
            item['result_original'],
            item['text_end_original'],
            item['pub_date'],
            item['case_type'],
            item['participant_info'],
            item['wenshu_type'],
            item['judgement_date'],
            item['case_close_way'],
            item['effect_level'],
            item['wenshu'],
        )
        sql = 'insert into wenshu values (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, \
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, \
                %s,FROM_UNIXTIME(%s),%s,%s,%s,%s,%s,%s,%s)'
        # print(sql % values)       
        tx.execute(sql, values)
        
        
    def insert_keyword(self, tx, item):
        values = (
            item['keyword'],
            item['keyword_value'],
            item['case_type_id'],
        )
        sql = 'insert into keyword_table values (null, %s, %s, %s)'
        tx.execute(sql, values)
        
        
    def insert_case_reason(self, tx, item):
        values = (
            item['case_reason'],
            item['case_reason_value'],
            item['case_type_id'],
        )
        sql = 'insert into case_reason_table values (null, %s, %s, %s)'
        tx.execute(sql, values)
        
        
    def insert_court_area(self, tx, item):
        query_sql = 'select * from court_area_table where court_area = %s and case_type_id = %s'
        tx.execute(query_sql, (item['court_area'], item['case_type_id']))
        query_result = tx.fetchall()
        # print(query_result)
        if not query_result:
            values = (
                item['court_area'],
                item['court_area_value'],
                item['case_type_id'],
            )
            sql = 'insert into court_area_table values (null, %s, %s, %s)'
            tx.execute(sql, values)
        
    def insert_court(self, tx, item):
        query_sql = 'select * from court_table where court_name = %s and case_type_id = %s'
        tx.execute(query_sql, (item['court_name'], item['case_type_id']))
        query_result = tx.fetchall()
        # print(query_result)
        if not query_result:
            values = (
                item['court_name'],
                item['court_name_value'],
                item['case_type_id'],
                item['court_level_id'],
            )
            sql = 'insert into court_table values (null, %s, %s, %s, %s)'
            tx.execute(sql, values)
