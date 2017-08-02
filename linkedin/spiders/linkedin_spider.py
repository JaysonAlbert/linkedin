from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.spiders.init import InitSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest
from linkedin.items import *
import linkedin
from scrapy.shell import inspect_response
from scrapy.utils.response import open_in_browser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy import log

import time


class LinkedinSpider(InitSpider):

    """
    Define the crawler's start URIs, set its follow rules, parse HTML
    and assign values to an item. Processing occurs in ../pipelines.py
    """

    name = "linkedin"
    allowed_domains = ["linkedin.com"]
    middleware = set([linkedin.middlewares.JsDownload])
    driver = webdriver.Chrome()

    # Uncomment the following lines for full spidering
    # start_urls = ["http://www.linkedin.com/directory/people-%s-%d-%d-%d"
    #               % (alphanum, num_one, num_two, num_three)
    #                 for alphanum in "abcdefghijklmnopqrstuvwxyz"
    #                 for num_one in xrange(1,11)
    #                 for num_two in xrange(1,11)
    #                 for num_three in xrange(1,11)
    #               ]

    # Temporary start_urls for testing; remove and use the above start_urls in production
    # start_urls = ["http://www.linkedin.com/directory/people-a-23-23-2"]
    start_urls = ["https://www.linkedin.com/in/zhenworldwide/",
                  "https://www.linkedin.com/in/linlin97/",
                  ]
    login_page = 'https://www.linkedin.com/uas/login'
    # TODO: allow /in/name urls too?
    # rules = (
    #     Rule(SgmlLinkExtractor(allow=('\/pub\/.+')),
    #          callback='parse_item'),
    # )

    def init_request(self):
        self.driver.get("https://www.linkedin.com/uas/login")
        # try:
        #     element = WebDriverWait(self.driver,5).until(
        #         EC.presence_of_element_located((By.NAME,"session_key"))
        #         )
        # except Exception,e:
        #     self.log(str(e) % "failed",level = log.WARNING)
        #     return
        element = self.driver.find_element_by_name("session_key")
        element.send_keys("momeijw@gmail.com")
        element =  self.driver.find_element_by_name("session_password")
        element.send_keys("Love@Princess#13")
        element = self.driver.find_element_by_name("signin")
        element.click()
        time.sleep(2)
        return self.initialized()
        # return Request(url=self.login_page,callback=self.login)

    def login(self,response):
        return FormRequest.from_response(response,formdata={
            'session_key':'momeijw@gmail.com','session_password':'Love@Princess#13'
        },
                                         callback = self.check_login_response)

    def check_login_response(self,response):
        return self.initialized()

    # def start_requests(self):
    #     meta = {'wait':EC.presence_of_element_located((By.CLASS_NAME,"pv-top-card-section__name Sans-26px-black-85%"))}
    #     for url in self.start_urls:
    #         yield scrapy.Request(url = url, callback = self.parse, meta = meta)

    def parse(self, response):
        open_in_browser(response)
        # inspect_response(response, self)
        if response.status != 200:
            item = NameUrlItemFailed()
            item['orig_url'] = response.url
            item['code'] = response.code
            item['type'] = 'url-item'
        else:
            urls = response.xpath('//ul[@class="column dual-column"]/li[@class="content"]/a/@href').extract()
            # if not urls:
            #     yield  Request(url=response.url,dont_filter=True)
            names = response.xpath('//ul[@class="column dual-column"]/li[@class="content"]/a/text()').extract()
            item = NameUrlItem()
            item['name'] = names
            item['url'] = urls
            item['orig_url'] = response.url
            yield item

        ## //ul/li[@class="pv-profile-section__card-item pv-position-entity ember-view"]
        pv = response.xpath('//ul/li[@class="pv-profile-section__card-item pv-position-entity ember-view"]')
        edu = response.xpath('//section[@class = "pv-profile-section education-section ember-view"]/ul/li')
        school_name = response.xpath('//h3[@class="pv-entity__school-name Sans-17px-black-85%-semibold"]')
        degre_name = response.xpath('//span[@class="pv-entity__comma-item"]')


        # for name,url in zip(names,urls):
        #     item['name'] = name
        #     item['url'] = url
        #     item['orig_url'] = response.url
        #     yield item

    def process_profile(self,pv):
        pass

    def process_eduction(self,pv):
        school = pv.xpath('/a/div[@class="pv-entity__summary-info"]/div/h3').extract()
        # school_name =
