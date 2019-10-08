# -*- coding: utf-8 -*-
# hive util with hive server2
from pyhive import hive

'''
定义一个类，用于获得hive连接对象
author:roy
dt:2019-05-14
'''
class HiveClient(object):
    def __init__(self, db_host, hdatabase, hport=10000):
        #初始化hive连接
        self.connHive = hive.Connection(host=db_host, port=hport,  database=hdatabase)

    '''
    执行sql查询
    input:sql
    author:roy
    dt:2019-05-21
    '''
    def query(self,sql):
        cursor = self.connHive.cursor()
        cursor.execute(sql)
        dataResult = cursor.fetchall()
        cursor.close()
        return dataResult

    '''
    插入数据
    input:sql
    author:roy
    dt:2019-05-21
    '''
    def insert(self,sql):
        cursor = self.connHive.cursor()
        cursor.execute(sql)
        cursor.close()
        self.connHive.commit()

    '''
    关闭连接
    input:连接对象
    author:roy
    dt:2019-05-21
    '''
    def close(self):
        self.connHive.close()
