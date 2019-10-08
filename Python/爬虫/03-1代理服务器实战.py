#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# 1. 使用代理服务器进行爬取网页
from urllib import request

def use_proxy(url,ip):
    proxy = request.ProxyHandler({'http':ip})
    opener = request.build_opener(proxy,request.HTTPHandler)
    request.install_opener(opener)
    # data = request.urlopen(url).read().decode('utf-8')
    data = request.urlopen(url,timeout = 3).read()
    return data 

# 代理服务器网址:https://www.xicidaili.com/nn/
# ip = '163.204.242.43:9999'
# ip = '163.204.246.150:9999'
# ip = '183.165.41.97:61234'
# ip = '113.121.38.66:9999'
# ip = '59.57.149.112:9999'
# ip = '1.197.204.242:9999'
ip = '110.86.138.233:9999'
url = 'http://www.baidu.com'
data = use_proxy(url,ip)
file = open('D:\\Python\\Project\\爬虫\\03-1\\proxy.html','wb')
file.write(data)
file.close()
print('OK')
