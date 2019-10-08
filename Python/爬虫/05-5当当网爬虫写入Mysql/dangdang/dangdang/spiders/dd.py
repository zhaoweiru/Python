# -*- coding: utf-8 -*-
import scrapy
from dangdang.items import DangdangItem
from scrapy.http import Request

class DdSpider(scrapy.Spider):
    name = 'dd'
    allowed_domains = ['book.dangdang.com']
    start_urls = ['http://search.dangdang.com/?key=python&ddsale=1&page_index=1']

    def parse(self, response):
        item = DangdangItem()
        item['title'] = response.xpath('//img/@alt').extract()
        item['link'] = response.xpath('//a[@name="itemlist-picture"]/@href').extract()
        item['comment'] = response.xpath('//a[@class="search_comment_num"]/text()').extract()

        # print(item['title'][0])
        # print(item['link'][0])
        # print(item['comment'][0])

        yield item 

        for i in range(2,3):
            url = 'http://search.dangdang.com/?key=python&ddsale=1&page_index=' + str(i)
            # print(url)
            yield Request(url,callback = self.parse,dont_filter = True)


