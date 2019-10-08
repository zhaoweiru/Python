# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from newsauto.items import NewsautoItem
from scrapy.http import Request
import re


class GetNewsSpider(CrawlSpider):
    name = 'get-news'
    allowed_domains = ['news.163.com']
    # start_urls = ['https://news.163.com/']

    def start_requests(self):
        ua = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
        yield Request('https://news.163.com/',headers = ua)

    rules = (
        Rule(LinkExtractor(allow = '19/0927/10'), callback = 'parse_item', follow = True),
    )

    def parse_item(self, response):
        pattern = '"docId" : "(.*?)",'
        item = NewsautoItem()
        item['content'] = response.xpath('//head/title/text()').extract()
        item['link'] = response.xpath('//script/text()').extract()
        url = re.compile(pattern).findall(str(item['link']))
        print('https://news.163.com/19/0927/10/' + url[0] + '.html')
        print(item['content'])
        # print(item['link'])
        return item,url



        # item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()


