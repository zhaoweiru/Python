#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from urllib import request
import re

pattern = '<div class="name">(.*?)</div>' 
data = request.urlopen('https://read.douban.com/provider/all').read()
# print(data)
data = data.decode('utf-8')
# print(data)
result = re.compile(pattern).findall(data)
# print(type(result))

file = open('D:\\Python\\Project\\爬虫\\result\\01-1\\publishing_name.txt','w')
for i in set(result):
    file.write(i)
    file.write('\r')
file.close()

print('提取成功')