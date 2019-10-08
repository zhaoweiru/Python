# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest

class DbSpider(scrapy.Spider):
    name = 'db'
    allowed_domains = ['douban.com']
    # start_urls = ['http://douban.com/']

    header={"User-Agent:":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}
    
    url = 'https://accounts.douban.com/passport/login'

    def start_requests(self):
        header={"User-Agent:":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}
        url = 'https://accounts.douban.com/passport/login'
        return [Request(url,headers = header,callback = self.parse,meta = {"cookiejar":1})]


    def parse(self, response):
        url = 'https://accounts.douban.com/passport/login'
        print('此时没有验证码')

        data = {'username':'17600660311',
                'password':'zwr19950304aaa'}

        print('登陆中……')

        return [FormRequest.from_response(response,
                                              meta = {"cookiejar":response.meta["cookiejar"]},
                                              headers = self.header,
                                              formdata = data,
                                              callback = self.next,
                                              )]

    def next(self,response):
        print("此时已经登陆完成")
        title = response.xpath("/html/head/title/text()").extract()
        # note = response.xpath("//div[@class='note']/text()").extract()
        print(title[0])
        # print(note[0])









