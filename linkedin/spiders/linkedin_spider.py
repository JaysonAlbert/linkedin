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
import numpy as np

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
                  # "https://www.linkedin.com/in/linlin97/",
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
        time.sleep(1)
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
        # open_in_browser(response)
        # inspect_response(response, self)
        # if response.status != 200:
        #     item = NameUrlItemFailed()
        #     item['orig_url'] = response.url
        #     item['code'] = response.code
        #     item['type'] = 'url-item'
        # else:
        #     urls = response.xpath('//ul[@class="column dual-column"]/li[@class="content"]/a/@href').extract()
        #     names = response.xpath('//ul[@class="column dual-column"]/li[@class="content"]/a/text()').extract()
        #     item = NameUrlItem()
        #     item['name'] = names
        #     item['url'] = urls
        #     item['orig_url'] = response.url
        #     yield item

        item = ProfileItem()
        item['url'] = response.url
        item['name'] = response.xpath('//h1[@class="pv-top-card-section__name Sans-26px-black-85%"]/text()').extract_first()
        item['career'] = response.xpath('//h2[@class="pv-top-card-section__headline Sans-19px-black-85%"]/text()').extract_first()
        try:
            item['company'] = response.xpath('//h3[@class="pv-top-card-section__company Sans-17px-black-70% mb1 inline-block"]/text()').extract_first()
        except Exception,e:
            pass
        item['location'] = response.xpath('//h3[@class="pv-top-card-section__location Sans-17px-black-70% mb1 inline-block"]/text()').extract_first()
        item['connection'] = response.xpath('//h3[@class="pv-top-card-section__connections pv-top-card-section__connections--with-separator Sans-17px-black-70% mb1 inline-block"]/text()').extract_first()
        item['school'] = response.xpath('//h3[@class="pv-top-card-section__school pv-top-card-section__school--with-separator Sans-17px-black-70% mb1 inline-block"]/text()').extract_first()
        exps = response.xpath('//section[@class="pv-profile-section experience-section ember-view"]/ul/li')
        education = response.xpath('//section[@class = "pv-profile-section education-section ember-view"]/ul/li')
        item['experience'] = self.process_experience(exps)
        item['education'] = self.process_edu(education)
        try:
            item['image_urls'] = response.xpath('//button[@class="pv-top-card-section__photo"]/img/@src').extract()
        except Exception,e:
            pass

        inspect_response(response, self)
        yield item




        # for name,url in zip(names,urls):
        #     item['name'] = name
        #     item['url'] = url
        #     item['orig_url'] = response.url
        #     yield item

    def process_experience(self,response):
        rt = []
        for index, experience in enumerate(response):
            ii = {}
            try:
                ii['job'] = experience.xpath('.//h3/text()').extract_first()
            except Exception,e:
                pass

            try:
                detail = experience.xpath('.//h4/span/text()').extract()
                for item in np.array(detail).reshape(-1,2):
                    ii[item[0]] = item[1]
            except Exception,e:
                pass

            try:
                ii['extra'] = experience.xpath('.//div[@class="pv-entity__extra-details"]/p/text()').extract_first()
            except Exception,e:
                pass

            rt.append(ii)

        return rt

    def process_edu(self,response):
        rt = []
        for index, school in enumerate(response):
            ii = {}
            try:
                ii['school_name'] = school.xpath('.//h3[@class="pv-entity__school-name Sans-17px-black-85%-semibold"]/text()').extract_first()
            except Exception,e:
                pass

            try:
                degree = school.xpath('.//div[@class="pv-entity__degree-info"]/p/span/text()').extract()
                for item in np.array(degree).reshape(-1,2):
                    ii[item[0]] = item[1]
            except Exception,e:
                pass

            try:
                extra = school.xpath('.//p[@class="pv-entity__secondary-title Sans-15px-black-70%"]/span/text()').extract()
                ii[extra[0]] = extra[1]
            except Exception,e:
                pass

            rt.append(ii)

        return rt




    def process_eduction(self,pv):
        school = pv.xpath('/a/div[@class="pv-entity__summary-info"]/div/h3').extract()
        # school_name =
