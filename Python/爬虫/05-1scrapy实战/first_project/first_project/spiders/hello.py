# -*- coding: utf-8 -*-
import scrapy
from first_project.items import FirstProjectItem

class HelloSpider(scrapy.Spider):
    "爬百度标题"
    name = 'hello'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        item = FirstProjectItem()
        item['content'] = response.xpath('/html/head/title/text()').extract()
        yield item

