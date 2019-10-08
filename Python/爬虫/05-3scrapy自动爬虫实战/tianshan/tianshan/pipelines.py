# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class TianshanPipeline(object):

    def __init__(self):
        self.file = open('D:\\Python\\Project\\爬虫\\05-3scrapy自动爬虫实战\\result.txt','a')

    def process_item(self, item, spider):
        print(item['title'])
        print(item['link'])
        print(item['stu'])
        self.file.write(item["title"][0]+"\n"+item["link"][0]+"\n"+item["stu"][0]+"\n"+"--------------"+"\n")
        return item

    def close_spider(self):
        self.file.close()