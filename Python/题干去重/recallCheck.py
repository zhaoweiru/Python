import Levenshtein
import os
from ConnUtile import HiveClient
import time
import datetime
import sys

HIVE_ONLINE_IP = '192.168.128.69'
HIVE_ONLINE_DB_NAME = 'jk_mid_recall_source'
HIVE_ONLINE_PORT = 10000

parameter = None

try:
    parameter = sys.argv[1]
except:
    print('=======没有加入时间参数,默认返回前一天========')

if parameter is not None:
    RUN_TIME = parameter
    L_DATE = "'" + RUN_TIME + "'"
else:
# 获取当前时间
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=-1)
    # 获取想要的日期的时间
    RUN_TIME = (today + offset).strftime('%Y-%m-%d')
    L_DATE = "'" + RUN_TIME + "'"

print('RUN_TIME:%s'%RUN_TIME)


#定义获取数据的sql
SQL_RECALL_SOURCE_QUESTIONS = '''select  distinct 
                                         one_bank.questno
                                        ,two_bank.questno
                                        ,one_bank.three_know_code
                                        ,one_bank.txt_content_clean
                                        ,two_bank.txt_content_clean
                                        ,one_bank.quest_source_id 
                                        ,two_bank.quest_source_id
                                   from (select  * 
                                            from jk_mid_recall_source.fact_recall_source_question_bank
                                           where l_date = '''+L_DATE+'''
                                        ) as one_bank
                             inner join (select  *
                                            from jk_mid_recall_source.fact_recall_source_question_bank
                                           where l_date <= '''+L_DATE+'''  
                                        ) as two_bank 
                                      on two_bank.questtype_id    = one_bank.questtype_id
                                     and two_bank.three_know_code = one_bank.three_know_code '''


def getMatchSubjects():
    #获取一个hive连接
    connGetRecomSubject = HiveClient(HIVE_ONLINE_IP,HIVE_ONLINE_DB_NAME,HIVE_ONLINE_PORT)
    #获得数据
    listSubjects = connGetRecomSubject.query(SQL_RECALL_SOURCE_QUESTIONS)
    #清洗后写入新集合
    listSubjectsCol = []
    for lineSubject in listSubjects:
        dictSubject = {}
        dictSubject['y_id'] = lineSubject[0]
        dictSubject['t_id'] = lineSubject[1]
        dictSubject['three_know_code'] = lineSubject[2]
        dictSubject['y_txt_content_par'] = lineSubject[3]
        dictSubject['t_txt_content_par'] = lineSubject[4]
        dictSubject['y_quest_source_id'] = lineSubject[5]
        dictSubject['t_quest_source_id'] = lineSubject[6]
        listSubjectsCol.append(dictSubject)
    connGetRecomSubject.close()
    return listSubjectsCol


if __name__ == "__main__":
    #查询数据
    listSubjectsCol = getMatchSubjects()
    print('取数完成')
    #开始比对
    print('开始比对')
    #数据文件路径，要输出的文件
    pathOutCheck = '/opt/sys/schoolquestion_examresult/wrongquest-V2.2.0.2018.11.27_release/recall/similar/recall_del_repeat/recall_check_{}.txt'.format(RUN_TIME)
    #如果文件已存在，要先删除
    if os.path.exists(pathOutCheck) == True:
        os.remove(pathOutCheck)
        print('删除数据文件')

    #开始写出数据
    fileCheck = open(pathOutCheck,'a+',encoding='utf-8')
    i = 0
    for dictCheck in listSubjectsCol:
        simlValue = round(Levenshtein.ratio(dictCheck['y_txt_content_par'],dictCheck['t_txt_content_par']),3)
        simlValue = str(simlValue)
        y_quest_source_id = str(dictCheck['y_quest_source_id'])
        t_quest_source_id = str(dictCheck['t_quest_source_id'])
        fileCheck.write(dictCheck['y_id'] + '\t' + dictCheck['t_id'] + '\t' + y_quest_source_id + '\t' + t_quest_source_id + '\t' + simlValue + '\n')
        i = i + 1
        #print(i)
    fileCheck.close()
