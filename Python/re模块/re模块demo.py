#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re

'''
常用正则表达式符号和语法
'''


# 1. '.'匹配所有字符串，除 \n 以外。
pattern = '.python...'
string = 'ipython yyy'
result = re.search(pattern,string)
print(result)


# 2. '\d'：匹配数字，'\w'：匹配字母和数字和下划线，'\s'：匹配空白字符
pattern = '\w\dpython\s\w'
string = 'cadq8python dfcas'
result = re.search(pattern,string)
print(result)


# 3. []：字符集
pattern = 'pyth[abco]n'
string = 'ascdkhtuabpython354nf'
result = re.search(pattern,string)
print(result)


# 4. '|'：代表左右表达式中匹配其中一个。
pattern = 'python|php'
string = 'ascgphpascber82python84vas'
result = re.search(pattern,string)
print(result)


# 5. 修正模式 I 匹配时忽略大小写
pattern = 'python'
string = 'asdcnPYTHONACfe'
result1 = re.search(pattern,string)
result2 = re.search(pattern,string,re.I)
print('result1 = %s , result2 = %s'%(result1,result2))


# 6. 贪婪模式与懒惰模式
pattern_1 = 'p.*y'
pattern_2 = 'p.*?y'
string = 'asdcbpbydne34y'
result_1 = re.search(pattern_1,string)
result_2 = re.search(pattern_2,string)
print('result_1 = %s , result_2 = %s'%(result_1,result_2))


# 7. match search findall
pattern = 'p.*?y'
string = 'asdcpaaaay123pbbbby'
print(re.search(pattern,string))
print(re.match(pattern,string))
print(re.compile(pattern).findall(string))


# 8. 匹配网址
pattern = '[a-zA-Z]+://[^\s]*[.com|.cn]'
string = '<a href="http://www.baidu.com">ffff'
result = re.compile(pattern).findall(string)
print(result)


# 9. 匹配电话号码
pattern = '1\d{10}'
string = 'phone:43413582364523457vsbg'
result = re.compile(pattern).findall(string)
print(result)


# 10. 爬虫 正则提取价格
from urllib import request
import re
pattern = '<dd class="now_price">(.*?)</dd>'
data = request.urlopen('https://edu.csdn.net/combo/detail/367').read()
data = data.decode('utf-8')
result = re.compile(pattern).findall(str(data))
print(result)


# 11. 爬虫 保存网页
from urllib import request
data = request.urlopen('http://baike.baidu.com/fenlei/%E6%91%84%E5%BD%B1').read()
# print(data.decode('utf-8'))
file = open('D:\\Python\\Project\\test.html','wb')
file.write(data)
file.close()
