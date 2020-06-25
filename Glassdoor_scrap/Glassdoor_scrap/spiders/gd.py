# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from ..items import GlassdoorItem



class GdSpider(scrapy.Spider):
    name = 'gd'
    allowed_domains = ['www.glassdoor.co.uk']
    start_urls = ['https://www.glassdoor.co.uk/profile/login_input.htm']

    def start_requests(self):
        ''' Transforming javascript into html render '''
        for url in self.start_urls:
            yield SplashRequest(url, self.login,
                                endpoint='render.html',
                                args={'wait': 0.5},
                                )

    def login(self, response):
        token = response.xpath('//form/input[@name="gdToken"]/@value').extract()
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'your username',
                      'password': 'your password',
                      'gdToken': token},
            callback=self.after_login
        )

    def after_login(self, response):
        yield scrapy.Request(url="https://www.glassdoor.co.uk/Reviews/benugo-Reviews-E246250.htm",
                             callback=self.parse_pages)

    def parse_pages(self, response):
        all_reviews = response.xpath('//div[@class= "hreview"]')
        for review in all_reviews:
            job_title = review.xpath('.//span[@class= "authorJobTitle middle"]/text()').extract()
            location = review.xpath('.//span[@class="authorLocation"]/text()').extract()
            date = review.xpath('.//time[@class= "date subtle small"]/text()').extract()
            rating = review.xpath('.//div[contains(@class, "ratingNum")]/text()').extract_first()
            review_title = review.xpath('.//a[@class="reviewLink"]/text()').extract()
            pros = review.xpath('.//*[text() = "Pros"]/following-sibling::p/text()').extract()
            cons = review.xpath('.//*[text() = "Cons"]/following-sibling::p/text()').extract()

            gd = GlassdoorItem()

            gd['job_title'] = job_title
            gd['location'] = location
            gd['date'] = date
            gd['rating'] = rating
            gd['review_title'] = review_title
            gd['pros'] = pros
            gd['cons'] = cons

            yield gd

        next_page_url = response.xpath('//a[@class= "pagination__ArrowStyle__nextArrow  "]/@href')
        for link in next_page_url:
            url = response.urljoin(link.extract())
            yield scrapy.Request(url, callback=self.parse_pages)
