# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import functools
from selenium import webdriver
from scrapy.http import HtmlResponse
from scrapy import log
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_spider_middleware(method):
    @functools.wraps(method)
    def wrapper(self, request, spider):
        msg = '%%s %s middleware step' % (self.__class__,)
        spider.log(request.meta)
        if self.__class__ in spider.middleware:
            spider.log(msg % 'executing', level=log.DEBUG)
            return method(self, request, spider)
        else:
            spider.log(msg % 'skipping', level=log.DEBUG)
            return None

    return wrapper

class JsDownload(object):

    @check_spider_middleware
    def process_request(self, request, spider):
        driver = spider.driver
        driver.get(request.url)
        # if 'wait' in request.meta:
        #     try:
        #         element = WebDriverWait(driver,5).until(
        #             request.meta['wait']
        #         )
        #     except Exception,e:
        #         spider.log(str(e) % "failed",level = log.WARNING)
        return HtmlResponse(request.url, encoding='utf-8', body=driver.page_source.encode('utf-8'))

class LinkedinSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

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
