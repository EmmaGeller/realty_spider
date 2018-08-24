# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import re

import redis
import scrapy
from scrapy import signals
from scrapy.http import HtmlResponse

from realty_sprider.useragent import agents
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware  # UserAegent中间件

class RealtySpriderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    # def __init__(self, settings, crawler):
    #     self.r = redis.from_url(settings['REDIS_URL'], db=1, decode_responses=True)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RealtySpriderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self,settings):
        self.rconn = redis.Redis(host=settings.get('REDIS_HOST'), port=settings.get('REDIS_PORT'), db=1,decode_responses=True)
        self.r0 = redis.Redis(host=settings.get('REDIS_HOST'), port=settings.get('REDIS_PORT'), db=0, decode_responses=True)
        self.root_url='http://ris.szpl.gov.cn/bol/index.aspx'
        self.totalpage=settings.get('TOTAL_PAGE')
        super(RealtySpriderDownloaderMiddleware, self).__init__()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(crawler.settings)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class UserAgentmiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent

# class PageMiddleware(object):
#     def __init__(self):
#         self.rconn = redis.from_url(url='localhohst',port=6379, db=1, decode_responses=True)
#         super(PageMiddleware, self).__init__()
#
#         @classmethod
#         def from_crawler(cls, crawler):
#             return cls(crawler.settings, crawler)

class proxiesSpiderMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = 'http://dev.qkgame.com.cn:9802/random'

    def process_response(self, request, response, spider):
            '''对返回的response处理'''
            # 如果返回的response状态不是200，重新生成当前request对象
            if response.status != 200:
                proxy = 'http://dev.qkgame.com.cn:9802/random'
                # 对当前reque加上代理
                request.meta['proxy'] = proxy
                return request
            return response


class seleniumSpider(object):
    # 通过edge请求动态网页，代替scrapy的downloader
    def process_request(self, request, spider):
        # 判断该spider是否为我们的目标
        if spider.browser:
            # browser = webdriver.Edge(
            #     executable_path='F:/PythonProjects/Scrapy_Job/JobSpider/tools/MicrosoftWebDriver.exe')
            spider.browser.get(request.url)
            import time
            time.sleep(3)
            print("访问:{0}".format(request.url))
            # 直接返回给spider，而非再传给downloader
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8",
                                request=request)







