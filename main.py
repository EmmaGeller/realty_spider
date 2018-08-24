#!/usr/bin/env python
# -*- coding:utf-8 -*-
import psycopg2
from scrapy import cmdline
import redis

redis_Host = "10.10.1.213"
redis_key = 'realty:start_urls'

rediscli = redis.Redis(host=redis_Host, port=6379, db="0")
connect = psycopg2.connect(
    host='*******',
    port='********',
    dbname='*********',
    user='*********',
    password='************'
)
cursor = connect.cursor();
flushdbRes = rediscli.flushdb()
rediscli.lpush(redis_key, "http://ris.szpl.gov.cn/bol/index.aspx/begin")

rediscli.lpush(redis_key, "http://ris.szpl.gov.cn/credit/showcjgs/xssList.aspx")

rediscli.lpush(redis_key, "http://ris.szpl.gov.cn/credit/showcjgs/xmList.aspx")

rediscli.lpush(redis_key, "http://ris.szpl.gov.cn/credit/showcjgs/ysfcjgs.aspx")

cmdline.execute("scrapy crawl realtySpider".split())
