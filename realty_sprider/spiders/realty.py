# -*- coding: utf-8 -*-
import re
import time
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from realty_sprider.items import CrawUrls


class RealtySpider(CrawlSpider):
    name='realty'
    start_urls=['http://ris.szpl.gov.cn/bol/index.aspx']

    rules = (
        Rule(LinkExtractor(allow=('\.aspx\?')),callback='parse_item',follow=True),
    )

    def parse_item(self,response):
        type=re.findall(r'http://ris.szpl.gov.cn/bol/(.*?)\.aspx\?', response.url)
        table_type=self._get_type(type[0])
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        item=CrawUrls()
        item['url']=response.url
        item['timestamp']=timestamp
        item['table_name']='craw_urls'
        item['table_type']=table_type
        return item


    def _get_type(self, type):
        return {
            'certdetail': '1',
            'projectdetail': '2',
            'hezuo': '3',
            'building': '4',
            'housedetail': '5'
        }.get(type)
