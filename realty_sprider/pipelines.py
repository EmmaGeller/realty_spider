# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import time
import scrapy.core.scraper
import six
import psycopg2
import redis

from realty_sprider.items import CrawUrls


class RealtySpriderPipeline(object):


    def __init__(self, settings):
        self.settings = settings
        self.r1 = redis.Redis(host=self.settings .get('REDIS_HOST'), port=self.settings .get('REDIS_PORT'), db=1,
                              decode_responses=True)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        # 连接数据库
        self.connect = psycopg2.connect(
            host=self.settings.get('POSTGRESQL_HOST'),
            port=self.settings.get('POSTGRESQL_PORT'),
            dbname=self.settings.get('POSTGRESQL_DBNAME'),
            user=self.settings.get('POSTGRESQL_USER'),
            password=self.settings.get('POSTGRESQL_PASSWD')
        )
        self.cursor = self.connect.cursor();

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

    def process_item(self, item, spider):
        global sql
        try:
            table_name = item.pop('table_name')
            abs_id = item.pop('abs_id')
            col_str = ''
            row_str = ''
            for key in item.keys():
                col_str = col_str + " " + key + ","
                row_str = "{}'{}',".format(row_str,
                                           item[key] if "'" not in item[key] else item[key].replace("'", "\\'"))
            if abs_id != None:
                sql = "insert INTO {} ({}) VALUES ({}) ON CONFLICT ({}) DO UPDATE SET ".format(table_name,
                                                                                           col_str[1:-1],
                                                                                           row_str[:-1],
                                                                                           abs_id)
                for (key, value) in six.iteritems(item):
                    sql += "{} = '{}', ".format(key, value if "'" not in value else value.replace("'", "\\'"))
                sql = sql[:-2]
            else:
                sql = "insert INTO {} ({}) VALUES ({})".format(table_name,
                                                               col_str[1:-1],
                                                               row_str[:-1])
            self.cursor.execute(sql)
            self.connect.commit()
        except psycopg2.InterfaceError as exc:
            self.connect.rollback()
            self.r1.lpush("erro_url",item['url'])
            logging.ERROR(exc.message)
            # 再次尝试连接数据库
            self.connect = psycopg2.connect(
                host=self.settings.get('POSTGRESQL_HOST'),
                port=self.settings.get('POSTGRESQL_PORT'),
                dbname=self.settings.get('POSTGRESQL_DBNAME'),
                user=self.settings.get('POSTGRESQL_USER'),
                password=self.settings.get('POSTGRESQL_PASSWD')
            )
            self.cursor = self.connect.cursor()
        except Exception as e:
            self.connect.rollback()
            self.r1.lpush("erro_url",item['url'])
            logging.ERROR(e.message)
            raise e


