# -*- coding: utf-8 -*-
import scrapy
from first_project.items import FirstProjectItem
from scrapy.http import Request

class WyNewsSpider(scrapy.Spider):
    "爬取网易新闻标题"
    name = 'wy-news'
    allowed_domains = ['news.163.com']
    # start_urls = ['http://news.163.com/']

    def start_requests(self):
        ua = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
        yield Request('https://news.163.com/',headers = ua)

    def parse(self, response):
        item = FirstProjectItem()
        item['content'] = response.xpath('//ul[@class="top_news_ul"]/li/a/text()').extract()
        item['link'] = response.xpath('//ul[@class="top_news_ul"]/li/a/@href').extract()
        yield item
