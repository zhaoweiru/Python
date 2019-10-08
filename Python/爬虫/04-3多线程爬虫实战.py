#!/usr/bin/python3
# -*- coding: UTF-8 -*-



# 1. 单线程爬虫实战
from urllib import request 
import re 

headers = ('User_Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36')
opener = request.build_opener()
opener.addheaders = [headers]
request.install_opener(opener)

for i in range(1,5):
    url = 'https://www.qiushibaike.com/hot/page/' + str(i) + '/'
    # print(url)
    data = request.urlopen(url).read().decode('utf-8')
    # print(data)
    pattern = '<div class="text-box">(.*?)</div>'
    # 让 . 匹配包括换行符，即用了该模式修正后，"." 匹配就可以匹配任意的字符了
    content = re.compile(pattern,re.S).findall(data)
    # print(content)
    for j in range(0,len(content)):
        print("第" + str(i) + "页第" + str(j) + "个段子的内容是：")
        print(content[j])
    i += 1 




# 2. 多线程爬虫实战Demo
import threading
class A(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        for i in range(0,100):
            print("我是线程A")

class B(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        for i in range(0,100):
            print('我是线程B')

a = A()
a.start()
b = B()
b.start()





# 3. 多线程爬虫实战

from urllib import request 
from urllib import error 
import threading
import re 

headers = ('User_Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36')
opener = request.build_opener()
opener.addheaders = [headers]
request.install_opener(opener)
pattern = '<div class="text-box">(.*?)</div>'

class run_a(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        "奇数页"
        for i in range(1,10,2):
            url = 'https://www.qiushibaike.com/hot/page/' + str(i) + '/'
            # print(url)
            data = request.urlopen(url).read().decode('utf-8')
            # print(data)
            # 让 . 匹配包括换行符，即用了该模式修正后，"." 匹配就可以匹配任意的字符了
            content = re.compile(pattern,re.S).findall(data)
            # print(content)
            for j in range(0,len(content)):
                print("第" + str(i) + "页第" + str(j) + "个段子的内容是：")
                print(content[j])
            i += 1 

class run_b(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        "偶数页"
        for i in range(0,10,2):
            url = 'https://www.qiushibaike.com/hot/page/' + str(i) + '/'
            # print(url)
            data = request.urlopen(url).read().decode('utf-8')
            # print(data)
            # 让 . 匹配包括换行符，即用了该模式修正后，"." 匹配就可以匹配任意的字符了
            content = re.compile(pattern,re.S).findall(data)
            # print(content)
            for j in range(0,len(content)):
                print("第" + str(i) + "页第" + str(j) + "个段子的内容是：")
                print(content[j])
            i += 1 
# 实例化线程
a = run_a()
b = run_b()
# 启动线程
a.start()
b.start()

