#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from urllib import request
from urllib import error
import time
import re

# 微信爬虫编写实战


# 自定义函数，为使用代理服务器爬一个网址
def use_proxy(url,ip):
    "功能为使用代理服务器爬一个网址"
    # 建立异常处理
    try:
        req = request.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36')
        proxy = request.ProxyHandler({'http':ip})
        opener = request.build_opener(proxy,request.HTTPHandler)
        request.install_opener(opener)
        data = request.urlopen(req).read()
        return data 
    except error.URLError as e :
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)
        # 若为 URLError 异常，延时 5 秒执行
        time.sleep(5)
    except Exception as e :
        print('Exception:' + str(e))
        # 若为 Exception 异常，延时 1 秒执行
        time.sleep(1)

# print(use_proxy.__doc__)

# 设置关键字 
key = 'Python'

# 设置代理服务器，该代理服务器有可能失效，读者需要换成新的有效代理服务器
proxy = '127.0.0.1:8888'

# 爬多少页
for i in range(0,3):
    key = request.quote(key)
    cur_page_url = 'https://weixin.sogou.com/weixin?query=' + key + '&_sug_type_=&sut=969&lkt=1%2C1567738302093%2C1567738302093&s_from=input&_sug_=y&type=2&sst0=1567738302197&page=' + str(i) + '&ie=utf8&w=01019900&dr=1'
    cur_page_data = use_proxy(cur_page_url,proxy)
    pattern = '</em>(.*?)</a>'
    rs1 = re.compile(pattern,re.S).findall(str(cur_page_data))
    if(len(rs1) == 0):
        print("此次（" + str(i) + "页）没成功")
        continue
    for j in range(0,len(rs1)):
        thisurl = rs1[j]
        # 已失效
        thisurl = thisurl.replace("amp;","")
        file = "D:\\Python\\Project\\爬虫\\result\\04-2\\第" + str(i) + "页第" + str(j) + "篇文章.html"
        thisdata = use_proxy(thisurl,proxy)
        try:
            fh = open(file,"wb")
            fh.write(thisdata)
            fh.close()
            print("第" + str(i) + "页第" + str(j) + "篇文章成功")
        except Exception as e:
            print(e)
            print("第" + str(i) + "页第" + str(j) + "篇文章失败")
