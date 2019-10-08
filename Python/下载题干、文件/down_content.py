# -*- coding: UTF-8 -*-
import time
import threading
import os
import sys
import requests

#ll定义队列
# filename = time.strftime('%Y-%m-%d', time.localtime()) + "-zwr.txt"  # 将指定格式的当前时间以字符串输出
# print("要写入的文件名："+filename)


def download(txt_content_url):
    imageUrl = 'http://image.fclassroom.com/' + txt_content_url
    # print(imageUrl)
    try:
    	strTest = requests.get(url=imageUrl)
    except:
        pass
    strTest.encoding = 'gbk'
    # print(strTest.text)
    content = strTest.text
    content = content.replace('\n','').replace('\n','').replace('\r','').replace('\r\n','').replace(' ','').replace('\t','')
    return content


#从文件读取数据
pathSource = '/opt/sys/schoolquestion_examresult/wrongquest-V2.2.0.2018.11.27_release/test/xkb_content_url_1.txt'
fileRead = open(pathSource, 'r', encoding='utf-8')
listdates = fileRead.readlines()

#print(listdates)
i = 0
for listdate in listdates:
    arrdate = listdate.split('^.^')
    questno = arrdate[0]
    questno = questno.replace('\n','').replace('\n','').replace('\r','').replace('\r\n','').replace(' ','').replace('\t','')
    txt_content_url = arrdate[1]
    txt_content = download(txt_content_url.replace('\n',''))

    output = questno + '^.^' + txt_content
    # print(questno)
    # print(txt_content)
    # print(output)

    pathOutCheck = '/opt/sys/schoolquestion_examresult/wrongquest-V2.2.0.2018.11.27_release/test/xkb_content_result_1.txt'
    fileCheck = open(pathOutCheck,'a+',encoding='utf-8')
    fileCheck.write(output + '\n')
    time.sleep(0.1)
    i += 1
    print(i)
