# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class DangdangPipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(host = '127.0.0.1',user = 'root',passwd = '123456',db = 'dangdang')
        for i in range(0,len('title')):
            title = item["title"][i]
            link = item["link"][i]
            comment = item["comment"][i]
            sql = "insert into book_info(title,link,comment) values('"+title+"','"+link+"','"+comment+"')"
            print(sql)
            conn.query(sql)
            conn.commit()
        conn.close()
        return item