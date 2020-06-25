# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GlassdoorItem(scrapy.Item):
    job_title = scrapy.Field()
    location = scrapy.Field()
    date = scrapy.Field()
    rating = scrapy.Field()
    review_title = scrapy.Field()
    pros = scrapy.Field()
    cons = scrapy.Field()
