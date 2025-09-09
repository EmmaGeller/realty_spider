# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import six

class RealtySpriderPipeline(object):

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        # 连接数据库
        self.connect = pymysql.connect(
            host=self.settings.get('MYSQL_HOST'),
            port=self.settings.get('MYSQL_PORT'),
            db=self.settings.get('MYSQL_DBNAME'),
            user=self.settings.get('MYSQL_USER'),
            passwd=self.settings.get('MYSQL_PASSWD'),
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor();

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

    def process_item(self, item, spider):
        # if isinstance(item,CretDetail):
        table_name = item.pop('table_name')
        col_str = ''
        row_str = ''
        for key in item.keys():
            col_str = col_str + " " + key + ","
            row_str = "{}'{}',".format(row_str,
                                       item[key] if "'" not in item[key] else item[key].replace("'",
                                                                                                "\\'"))
            sql = "insert INTO {} ({}) VALUES ({}) ON DUPLICATE KEY UPDATE ".format(table_name,
                                                                                    col_str[1:-1],
                                                                                    row_str[:-1])
        for (key, value) in six.iteritems(item):
            sql += "{} = '{}', ".format(key, value if "'" not in value else value.replace("'", "\\'"))
        sql = sql[:-2]
        self.cursor.execute(sql)  # 执行SQL
        self.connect.commit()  # 写入操作
