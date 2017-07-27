from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.spiders.init import InitSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest
from linkedin.items import *


class LinkedinSpider(InitSpider):

    """
    Define the crawler's start URIs, set its follow rules, parse HTML
    and assign values to an item. Processing occurs in ../pipelines.py
    """

    name = "linkedin"
    allowed_domains = ["linkedin.com"]

    # Uncomment the following lines for full spidering
    start_urls = ["http://www.linkedin.com/directory/people-%s-%d-%d-%d"
                  % (alphanum, num_one, num_two, num_three)
                    # for alphanum in "abcdefghijklmnopqrstuvwxyz"
                    for alphanum in "c"
                    for num_one in xrange(1,101)
                    for num_two in xrange(1,101)
                    for num_three in xrange(1,101)
                  ]

    # Temporary start_urls for testing; remove and use the above start_urls in production
    # start_urls = ["http://www.linkedin.com/directory/people-a-23-23-2"]
    login_page = 'https://www.linkedin.com/uas/login'
    # TODO: allow /in/name urls too?
    rules = (
        Rule(SgmlLinkExtractor(allow=('\/pub\/.+')),
             callback='parse_item'),
    )

    def init_request(self):
        return Request(url=self.login_page,callback=self.login)

    def login(self,response):
        return FormRequest.from_response(response,formdata={
            'session_key':'momeijw@gmail.com','session_password':'Love@Princess#13'
        },
                                         callback = self.check_login_response)

    def check_login_response(self,response):
        return self.initialized()

    def parse(self, response):
        urls = response.xpath('//ul[@class="column dual-column"]/li[@class="content"]/a/@href').extract()
        if not urls:
            yield  Request(url=response.url,dont_filter=True)
        names = response.xpath('//ul[@class="column dual-column"]/li[@class="content"]/a/text()').extract()
        item = NameUrlItem()
        item['name'] = names
        item['url'] = urls
        item['orig_url'] = response.url
        yield item
        # for name,url in zip(names,urls):
        #     item['name'] = name
        #     item['url'] = url
        #     item['orig_url'] = response.url
        #     yield item


        # if response:
        #     hxs = HtmlXPathSelector(response)
        #     item = LinkedinItem()
        #     # TODO: is this the best way to check that we're scraping the right page?
        #     item['full_name'] = hxs.select('//*[@id="name"]/span/span/text()').extract()
        #     if not item['full_name']:
        #
        #         # recursively parse list of duplicate profiles
        #         # NOTE: Results page only displays 25 of possibly many more names;
        #         # LinkedIn requests authentication to see the rest. Need to resolve
        #
        #         # TODO: add error checking here to ensure I'm getting the right links
        #         # and links from "next>>" pages
        #         multi_profile_urls = hxs.select('//*[@id="result-set"]/li/h2/strong/ \
        #                                   a/@href').extract()
        #         for profile_url in multi_profile_urls:
        #             yield Request(profile_url, callback=self.parse_item)
        #     else:
        #         pass
        #         # item['first_name'],
        #         # item['last_name'],
        #         # item['full_name'],
        #         # item['headline_title'],
        #         # item['locality'],
        #         # item['industry'],
        #         # item['current_roles'] = item['full_name'][0],
        #         #                         item['full_name'][1],
        #         #                         hxs.select('//*[@id="name"]/span/span/text()').extract(),
        #         #                         hxs.select('//*[@id="member-1"]/p/text()').extract(),
        #         #                         hxs.select('//*[@id="headline"]/dd[1]/span/text()').extract(),
        #         #                         hxs.select('//*[@id="headline"]/dd[2]/text()').extract(),
        #         #                         hxs.select('//*[@id="overview"]/dd[1]/ul/li/text()').extract()
        #         # TODO: add metadata fields
        #
        #         if hxs.select('//*[@id="overview"]/dt[2]/text()').extract() == [u' \n       Education\n    ']:
        #             item['education_institutions'] = hxs.select('//*[@id="overview"]/dd[2]/ul/li/text()').extract()
        #         print item
        # else:
        #     print "Uh oh, no response."
        #     return
