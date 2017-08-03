# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class LinkedinItem(scrapy.Item):
  # define the fields for your item here:
	full_name = Field()
	first_name = Field()
	last_name = Field()
	headline_title = Field()
	locality = Field()
	industry = Field()
	current_roles = Field()
	education_institutions = Field()

class NameUrlItem(scrapy.Item):
	name = Field()
	url = Field()
	orig_url = Field()

class NameUrlItemFailed(scrapy.Item):
	orig_url = Field()
	code = Field()
	type = Field()

class ProfileItem(scrapy.Item):
	url = Field()
	name = Field()
	career = Field()
	company = Field()
	location = Field()
	connection = Field()
	school = Field()
	experience = Field()
	education = Field()
	image_urls = scrapy.Field()
	images = scrapy.Field()
