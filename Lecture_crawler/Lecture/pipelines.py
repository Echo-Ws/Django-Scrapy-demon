# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import json

class LecturePipeline(object):
    def __init__(self):
        self.datacache = []
        self.cachesize = 100
        self.insert_stmt = 'insert into lecture VALUES(?,?,?,?,?,?,?)'

    def process_item(self, item, spider):
        self.insert(item['title'], item['speaker'], item['time'], item['place'], item['university'], item['update_time'], item['link'] )

    def open_spider(self, spider):
        self.conn = sqlite3.connect('../Lecture.db')
        self.createTable()
        # 处理增量
        if spider.name == 'ScutSoftware':
            try:
                dic = json.load(open(spider.name + 'Set'))
                spider.last_max_num = dic['max_num']
                spider.count = dic['count']
            except Exception:
                e = None

    def close_spider(self, spider):
        if spider.name == 'ScutSoftware':
            with open(spider.name+'Set', 'w') as f:
                dic = {}
                dic['count'] = spider.count - 1
                if spider.max_num:
                    dic['max_num'] = spider.max_num
                else:
                    dic['max_num'] = spider.last_max_num

                f.write(json.dumps(dic))

        if self.datacache:
            self.flush()
            self.conn.close()

    def createTable(self):
        stmt = '''CREATE TABLE IF NOT EXISTS`lecture` (
                               `title`	TEXT NOT NULL,
                               `speaker`	TEXT,
                               `time`	DATETIME ,
                               `place`	TEXT ,
                               `university`	TEXT NOT NULL,
                               `update_time`	DATETIME ,
                               `link`	TEXT NOT NULL,
                               PRIMARY KEY ('title','link')
                               );'''
        self.conn.execute(stmt)
        self.conn.commit()

    def insert(self, *item):
        self.datacache.append(item)
        if len(self.datacache) > self.cachesize:
            self.flush()

    def flush(self):

        self.conn.executemany(self.insert_stmt, self.datacache)
        self.conn.commit()
        self.datacache = []