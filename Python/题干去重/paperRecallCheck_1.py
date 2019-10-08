# -*- coding: utf-8 -*-
from StringUtil import StringUtil
from ConnUtile import HiveClient
import os
import time
import Levenshtein

HIVE_ONLINE_IP = '192.168.128.69'
HIVE_ONLINE_DB_NAME = 'jk_mid_recall_source'
HIVE_ONLINE_PORT = 10000

#定义获取数据的sql
SQL_PAPER_RECALL_QUESTIONS = '''select distinct 
                                       paper_quest.paper_question_id
                                       ,recall_quest.questno
                                       ,paper_quest.three_know_code
                                       ,paper_quest.three_know_name
                                       ,paper_quest.txt_content_clean
                                       ,recall_quest.txt_content_clean
                                  from (select * 
                                          from jk_mid_recall_source.fact_paperquestion_basic_content_info 
                                         where txt_content_clean is not NULL 
                                           and three_know_code   is not NULL
                                           and questtype_id = 1 
                                        ) as paper_quest 
                             inner join (select * 
                                           from jk_mid_recall_source.fact_recall_source_question_bank 
                                          where txt_content_clean is not NULL
                                            and three_know_code   is not NULL
                                            and questtype_id = 1 
                                        ) as recall_quest 
                                     on recall_quest.questtype_id = paper_quest.questtype_id 
                                    and recall_quest.three_know_code = paper_quest.three_know_code'''
#定义存储数据的路径
MAIN_PATH = '/opt/sys/schoolquestion_examresult/wrongquest-V2.2.0.2018.11.27_release/recall/similar'
PATH_PAPER_RECALL_CHECK = MAIN_PATH + '/sim_result/paperrecallcheck/' + 'paper_recall_check_1.txt'

'''
从hive获取题的信息数据
input:str
return:list
author:roy
dt:2019-05-27
'''
def getRecomSubjects():
    #获取一个hive连接
    connGetSubjects = HiveClient(HIVE_ONLINE_IP,HIVE_ONLINE_DB_NAME,HIVE_ONLINE_PORT)
    #获得数据
    subjectResult = connGetSubjects.query(SQL_PAPER_RECALL_QUESTIONS)
    #重命名一下字段
    listQuest = []
    for lineSubject in subjectResult:
        dictSubject = {}
        dictSubject['y_id'] = lineSubject[0]
        dictSubject['t_id'] = lineSubject[1]
        dictSubject['y_know_code'] = lineSubject[2]
        dictSubject['y_know_name'] = lineSubject[3]
        dictSubject['y_content'] = lineSubject[4]
        dictSubject['t_content'] = lineSubject[5]
        listQuest.append(dictSubject)
    connGetSubjects.close()
    return listQuest

if __name__ == "__main__":
    #查询数据
    print('开始读取数据')
    listSujects = getRecomSubjects()
    print('读取数据完成')
    
    print('开始计算相似度')
    listCheck = []
    for dictSubject in listSujects:
        dictSubjectCheck = {}
        dictSubjectCheck['y_id'] = dictSubject['y_id']
        dictSubjectCheck['y_know_code'] = dictSubject['y_know_code']
        dictSubjectCheck['y_know_name'] = dictSubject['y_know_name']
        dictSubjectCheck['t_id'] = dictSubject['t_id']
        #计算相似度
        simiValue = 0.0
        simiValue = round(Levenshtein.ratio(dictSubject['y_content'],dictSubject['t_content']),3)
        #相等时，相似度是1
        if dictSubject['y_content'] == dictSubject['t_content']:
            simiValue = 1.0
        dictSubjectCheck['simi_value'] = simiValue
        listCheck.append(dictSubjectCheck)
    print('相似度计算完成')

    #开始写出数据
    if os.path.exists(PATH_PAPER_RECALL_CHECK) == True:
        os.remove(PATH_PAPER_RECALL_CHECK)
        print('删除数据文件')


    fileOut = open(PATH_PAPER_RECALL_CHECK,'a+')
    for dictSubjectCheck in listCheck:
        fileOut.write(dictSubjectCheck['y_id'] + '\t')
        fileOut.write(dictSubjectCheck['y_know_code'] + '\t')
        fileOut.write(dictSubjectCheck['y_know_name'] + '\t')
        fileOut.write(dictSubjectCheck['t_id'] + '\t')
        fileOut.write(str(dictSubjectCheck['simi_value']) + '\t')
        fileOut.write('\n')
    fileOut.close()
