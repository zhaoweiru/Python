#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
from urllib import request



# 千图网（http://www.58pic.com/）某个频道的所有图片爬下来， 要高清版的



for i in range(0,1):

    home_page = 'https://www.58pic.com/tupian/so-852-0-default-0-0-SO-0_2_524_0_0_0_0-0-' + str(i) + '.html'
    # print('home_page = ' + home_page)

    home_data = request.urlopen(home_page).read().decode('utf-8','ignore')
    # print(home_data)

    home_pattern = '<a href="(.*?)" class="thumb-box"'
    next_page = re.compile(home_pattern).findall(home_data)
    # print(next_page)

    for j in range(0,len(next_page)):
        next_data = request.urlopen('http:' + next_page[j]).read().decode('utf-8','ignore')
        next_pattern = '<meta property="og:image" content="(.*?)"/>'
        image_url = re.compile(next_pattern).findall(next_data)
        image_url = 'http:' + image_url[0]
        print(image_url)
        file = 'D:\\Python\\Project\\爬虫\\result\\03-3\\' + str(i) + str(j) + '.jpg'
        request.urlretrieve(image_url,file)

print('OK')




