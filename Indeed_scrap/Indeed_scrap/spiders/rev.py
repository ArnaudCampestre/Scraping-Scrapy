# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import IndeedItem


class RevSpider(CrawlSpider):
    name = 'review'
    allowed_domains = ["indeed.co.uk"]
    start_urls = ['https://www.indeed.co.uk/cmp/Benugo/reviews/']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//li[@data-tn-element="reviews-tab"]/a',)),
             callback="parse_page", follow=True),

        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@data-tn-element="next-page"]',)),
             callback="parse_page", follow=True))

    def parse_page(self, response):
        all_reviews = response.xpath('//div[@class="cmp-Review"]')

        for review in all_reviews:
            job_title = review.xpath('.//a[@class="cmp-ReviewAuthor-link"][1]/text()').extract_first()
            location = review.xpath('.//a[@class="cmp-ReviewAuthor-link"][2]/text()').extract()
            date = review.xpath('.//span[@class="cmp-ReviewAuthor"]/text()')[-1].extract()
            rating = review.xpath('.//div[@class="cmp-ReviewRating-text"]/text()').extract()
            title = review.xpath('.//div[@class="cmp-Review-title"]/a/text()').extract_first()
            comment = review.xpath(
                './/div[@class="cmp-Review-text"]//span[@class="cmp-NewLineToBr-text"]/text()').extract()
            pros = review.xpath(
                './/div[@class="cmp-ReviewProsCons-prosText"]//span[@class="cmp-NewLineToBr-text"]/text()').extract()
            cons = review.xpath(
                './/div[@class="cmp-ReviewProsCons-consText"]//span[@class="cmp-NewLineToBr-text"]/text()').extract()

            indeed = IndeedItem()

            indeed['job_title'] = job_title
            indeed['location'] = location
            indeed['date'] = date
            indeed['rating'] = rating
            indeed['title'] = title
            indeed['comment'] = comment
            indeed['pros'] = pros
            indeed['cons'] = cons

            yield indeed
