#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# 抓取腾讯视频的评论数据

from urllib import request 
import re

headers = ('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36')
opener = request.build_opener()
opener.addheaders = [headers]
request.install_opener(opener)
cursor = '0'
page = 1567678419102

for i in range(0,10):
    url = 'https://video.coral.qq.com/varticle/1922154237/comment/v2?callback=_varticle1922154237commentv2&orinum=10&oriorder=o&pageflag=1&cursor=' + cursor + '&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=132&_=' + str(page)
    # print(url)
    data = request.urlopen(url).read().decode('utf-8')
    # print(data)
    pat_last = '"last":"(.*?)"'
    pat_content = '"content":"(.*?)"'
    pat_flag = '"hasnext":(.*?),"'
    cursor = re.compile(pat_last).findall(data)
    content = re.compile(pat_content).findall(data)
    flag = re.compile(pat_flag).findall(data)
    # print(cursor) 
    # print(content)
    # print(flag)
    for j in range(0,len(content)):
        print("------第" + str(i + 1) + '页，第' + str(j + 1) + "条评论内容是:")
        print(eval('u"'+content[j]+'"'))
        # print(content[j] )
    cursor = cursor[0]
    page += 1
    if flag[0] == 'false':
        break
    # print(cursor)
    # print(page)
