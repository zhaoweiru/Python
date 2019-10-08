#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from urllib import request


# 1. urlretrieve方法,可以将网站网址直接爬取到本地中
file = 'D:\\Python\\Project\\爬虫\\result\\02\\02-1.html'
url = 'http://www.cnblogs.com/qqhfeng/p/5785373.html'
request.urlretrieve(url,file)
print('OK')


# 2. urlcleanup()的应用，可以将urlretrieve()中的缓存清理掉
request.urlcleanup()


# 3. info() 可以将当前的基本环境信息显示出来
url = 'https://blog.csdn.net/weixin_41167340/article/details/79762058'
data = request.urlopen(url)
print(data.info())


# 4. getcode()获取当前的网页的状态码，geturl()获取当前的网页的网址。
# getcode = 200 状态码表示网页正常，403表示不正常。
url = 'https://blog.csdn.net/weixin_41167340/article/details/79762058'
data = request.urlopen(url)
print(data.getcode())
print(data.geturl())


# 5. 超时设置
url = 'https://blog.csdn.net/weixin_41167340/article/details/79762058'
data = request.urlopen(url,timeout = 1)
print(data.read().decode('utf-8'))


# 6. 异常处理
url = 'https://blog.csdn.net/weixin_41167340/article/details/79762058'

for i in range(0,100):
    try:
        data = request.urlopen(url,timeout = 0.1).read()
        print(len(data))
    except Exception as e:
        print(str(e))


# 7. request.Request的用法
keyword = 'python'
url = 'http://www.baidu.com/s?wd=' + keyword
req = request.Request(url)
data = request.urlopen(req).read()
file = open('D:\\Python\\Project\\爬虫\\result\\02\\02-2.html','bw')
file.write(data)
file.close()
print('OK')


# 8. request.Request的用法(中文)
keyword = '极课'
# 将中文进行urlencode编码使用函数
keyword = request.quote(keyword)        
url = 'http://www.baidu.com/s?wd=' + keyword
req = request.Request(url)
data = request.urlopen(req).read()
file = open('D:\\Python\\Project\\爬虫\\result\\02\\02-3.html','bw')
file.write(data)
file.close()
print('OK')


# 9. post请求登录
from urllib import parse
url = 'http://www.iqianyue.com/mypost/'
mydata = parse.urlencode({'name':'admin','pass':'123456'}).encode('utf-8')
print(mydata)
req = request.Request(url,mydata)
data = request.urlopen(req).read()
file = open('D:\\Python\\Project\\爬虫\\result\\02\\02-4.html','wb')
file.write(data)
file.close()
print('OK')


# 10. 爬虫的异常处理
from urllib import error 
try:
    request.urlopen('https://ai.csdn.net')
    print('OK')
except error.URLError as e:
    if hasattr(e,'code'):
        print(e.code)
    if hasattr(e,'reason'):
        print(e,'reason')


# 11. 浏览器伪装爬虫
url = 'https://blog.csdn.net/qq_42322103/article/details/99089546'
headers = ('User_Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36')
# print(type(headers))
opener = request.build_opener()
opener.addheaders = [headers]
data = opener.open(url).read()
file = open('D:\\Python\\Project\\爬虫\\result\\02\\02-5.html','wb')
file.write(data)
file.close()
print('OK')


# 12. 爬取新闻标题
import re 
from urllib import error 
data = request.urlopen('https://news.baidu.com/').read().decode('utf-8','ignore')
# data = data.decode('utf-8')
pattern = 'target="_blank">(.*?)</a></li>'
all_title = re.compile(pattern).findall(data)
# print(all_title)
file = open('D:\\Python\\Project\\爬虫\\result\\02\\02-6.txt','w')
for i in range(0,len(all_title)):
    try:
        # print("第" + str(i) + "次爬取")
        cur_title = all_title[i]
        if cur_title != '#{title}':
            # print(cur_title)
            file.write(cur_title + '\r')
    except error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)
file.close()
print('OK')


# 13-1 . 爬取CSDN博客http://blog.csdn.net/首页显示的所有文章，每个文章 内容单独生成一个本地网页存到本地中。
import re
from urllib import error 

url = 'http://blog.csdn.net/'
headers = ('User_Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36')
opener = request.build_opener()
opener.addheaders = [headers]
data = opener.open(url).read().decode('utf-8')
# print(data)

pattern = '<a href="(https://blog.csdn.net/.*?) target='
all_url = re.compile(pattern).findall(data)
# print(all_url)

for i in range(0,len(all_url)):
    try:
        print("第" + str(i) + "次爬取")
        cur_url = all_url[i]
        data = opener.open(url).read()
        file = open('D:\\Python\\Project\\爬虫\\result\\02\\02-7-' + str(i) + '.html','wb')
        file.write(data)
        file.close()
        print('成功')
    except error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)

print('全部完成')


# 13-2 . 爬取CSDN博客http://blog.csdn.net/首页显示的所有文章，每个文章 内容单独生成一个本地网页存到本地中。
import re
from urllib import error 

url = 'http://blog.csdn.net/'
headers = ('User_Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36')
opener = request.build_opener()
opener.addheaders = [headers]
request.install_opener(opener)      # 将自定义的 opener 对象定义为全局 opener
# data = opener.open(url).read()
data = request.urlopen(url).read()
data = data.decode('utf-8')
# print(data)

pattern = '<a href="(https://blog.csdn.net/.*?) target='
all_url = re.compile(pattern).findall(data)
# print(all_url)

for i in range(0,len(all_url)):
    try:
        print("第" + str(i) + "次爬取")
        cur_url = all_url[i]
        print('当前url = ' + cur_url)
        data = request.urlopen(url).read()
        # print(data)
        file = open('D:\\Python\\Project\\爬虫\\test\\' + str(i) + '.html','wb')
        file.write(data)
        file.close()


        # 不可行
        # file = 'D:\\Python\\Project\\爬虫\\test\\' + str(i) + '.html'
        # request.urlretrieve(cur_url,file)


        print('成功')
    except error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)

print('全部完成')

