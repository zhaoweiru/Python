#!/usr/bin/python
# -*- coding:UTF-8 -*-
import datetime
import sys

def getDay(operFlag,operNum):
    dayNum = int(operNum)
    #获取当天日期
    currDate = datetime.datetime.now()
    #处理向前取日期
    if operFlag == '-':
        dayNum = dayNum * (-1)
    #获得日期类型的增量
    increDay = datetime.timedelta(days=dayNum)
    #返回目标日期
    retDay = (currDate + increDay).strftime("%Y-%m-%d")
    return retDay

if __name__ == '__main__':
    '''
    处理日期时，三个参数。第一个固定是day，表示处理类型是天；第二个用+或者-，表示向前或向后计算；第三个是日期，表示天数。
    执行时要用反引号把python命令和脚本括起来
    '''
    retnDt = '1900-01-01'
    #判断入参
    if(len(sys.argv) != 4):
        print('parameters error,for example [day,-,1]')
        sys.exit(0)

    dateType = sys.argv[1]
    dateOper = sys.argv[2]
    dateNum = sys.argv[3]
    #处理天为单位的日期
    if dateType == 'day':
        retnDt = getDay(dateOper,dateNum)
        print(retnDt)