# -*- coding: utf-8 -*-
import scrapy
from tianshan.items import TianshanItem
from scrapy.http import Request

class LeasonSpider(scrapy.Spider):
    name = 'leason'
    allowed_domains = ['edu.hellobi.com']
    start_urls = ['https://edu.hellobi.com/course/1']

    def parse(self, response):
        item = TianshanItem()
        item['title'] = response.xpath('//ol[@class="breadcrumb"]/li[@class="active"]/text()').extract()
        # print(item['title'])
        item['link'] = response.xpath('//ul[@class="nav nav-tabs"]/li[@class="active"]/a/@href').extract()
        # print(item['link'])
        item['stu'] = response.xpath('//span[@class="course-view"]/text()').extract()
        # print(item['stu'])
        yield item

        for i in range(2,100):
            url = 'https://edu.hellobi.com/course/' + str(i)
            # print(url)
            yield Request(url,callback = self.parse)
