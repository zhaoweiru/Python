# -*- coding: UTF-8 -*-
from impala.dbapi import connect
import ConfigParser
import time
import threading
import os
import requests
import sys
import Queue
reload(sys)
sys.setdefaultencoding('utf-8')

#ll定义队列
filename = time.strftime('%Y-%m-%d', time.localtime()) + "-zwr.txt"  # 将指定格式的当前时间以字符串输出
print("要写入的文件名："+filename)

##多线程读取txt文件内容
def read_txtfile():
    prefix = 'http://image.fclassroom.com/'
    while True:
        try:
            str = queue_data.get_nowait()
        except:
            return
        questno = str[0]
        txturl = prefix + str[1]
        # 访问url
        try:
            quest_info = requests.get(txturl, timeout=3)
        except Exception as ex:
            continue
        # 读取txt内容
        try:
            quest_txt = quest_info.content.decode(encoding="utf-8").replace('\n','')
            str1 = quest_txt.replace('\xef\xbb\xbf', '')
            line = str1.strip('\r')
        except:
            try:
                quest_txt = quest_info.content.decode(encoding="gbk").replace('\n', '')
                str1 = quest_txt.replace('\xef\xbb\xbf', '')
                line = str1.strip('\r')
            except:
                continue

        # 内容写入指定文件
        with open(filename, 'a+') as r:
             r.write(questno)
             r.write('^-^')
             r.write(line)
             r.write('\n')

# 处理数据主程序
def data2hive():
    # 读取配置文件
    conf = ConfigParser.ConfigParser()
    conf.read('config.ini')
    ip = conf.get("hive", "ip")
    tablename = conf.get("hive", "tablename")
    db = conf.get("hive", "db")

    # 创建数据库连接
    conn = connect(host=ip, port=10000, database=db, auth_mechanism='PLAIN')
    # 创建cursor
    cursor = conn.cursor()

    try:
        sql = "select distinct questno,txt_content_url from " + tablename
        cursor.execute(sql)
        result = cursor.fetchall()
        count = 0
        if result is None:
            print("hive dose not have data!")
            return
        for row in result:
            queue_data.put(row)
            count += 1
            print('count:'+str(count))
    except Exception as ex:
        print(ex)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    queue_data = Queue.Queue()
    data2hive()
    #多线程执行
    thrs = [threading.Thread(target=read_txtfile) for i in range(50)]
    [thr.start() for thr in thrs]
    [thr.join() for thr in thrs]

