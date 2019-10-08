# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class FirstProjectPipeline(object):
    def process_item(self, item, spider):
        for i in range(0,len(item['content'])):
            # print("len(item['content']) =" + str(len(item['content'])))
            # print("len(item['link']) = " + str(len(item['link'])))
            print(item['content'][i])
            print(item['link'][i])
        return item
