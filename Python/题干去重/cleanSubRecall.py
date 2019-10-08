# -*- coding: utf-8 -*-
from StringUtil import StringUtil
from ConnUtile import HiveClient
import jieba
import jieba.analyse as jiebaAns
import os
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
SQL_RECALL_SOURCE_QUESTIONS = '''select id,questno               
                                 ,txt_content,txt_content_url,txt_answer_url,txt_analysis_url
                                 ,png_content_url,png_answer_url,png_analysis_url      
                                 ,html_content_url,html_answer_url,html_analysis_url
                                 ,three_know_code,three_know_name       
                                 ,questtype_id,questtype_name,question_time
                                 ,difficulty_val,recall_papername,quest_source
                                 ,l_date,recall_label
                                  from jk_mid_recall_source.fact_recall_source_question_bank
                                 where l_date = '''+L_DATE+''' '''
#定义存储数据的路径
MAIN_PATH = '/opt/sys/schoolquestion_examresult/wrongquest-V2.2.0.2018.11.27_release/recall/similar'
PATH_RECALL_CLEAN = MAIN_PATH + '/' + 'clean_content/' + 'recall_cleaned_{}.txt'.format(RUN_TIME)
PATH_JIEBA_KEYWORDS = MAIN_PATH + '/' + 'jieba_key_words.txt'
PATH_JIEBA_STOP_WORDS = MAIN_PATH + '/' + 'jieba_stop_words.txt'

'''
从hive获取题的信息数据
input:str
return:list
author:roy
dt:2019-05-22
'''
def getRecomSubjects():
    #获取一个hive连接
    connGetRecomSubject = HiveClient(HIVE_ONLINE_IP,HIVE_ONLINE_DB_NAME,HIVE_ONLINE_PORT)
    #获得数据
    recomResult = connGetRecomSubject.query(SQL_RECALL_SOURCE_QUESTIONS)
    #清洗后写入新集合
    listQuest = []
    for recomQuest in recomResult:
        dictSubject = {}
        dictSubject['id'] = recomQuest[0]
        dictSubject['questno'] = recomQuest[1]
        dictSubject['txt_content'] = recomQuest[2]
        dictSubject['txt_content_url'] = recomQuest[3]
        dictSubject['txt_answer_url'] = recomQuest[4]
        dictSubject['txt_analysis_url'] = recomQuest[5]
        dictSubject['png_content_url'] = recomQuest[6]
        dictSubject['png_answer_url'] = recomQuest[7]
        dictSubject['png_analysis_url'] = recomQuest[8]
        dictSubject['html_content_url'] = recomQuest[9]
        dictSubject['html_answer_url'] = recomQuest[10]
        dictSubject['html_analysis_url'] = recomQuest[11]
        dictSubject['three_know_code'] = recomQuest[12]
        dictSubject['three_know_name'] = recomQuest[13]
        dictSubject['questtype_id'] = recomQuest[14]
        dictSubject['questtype_name'] = recomQuest[15]
        dictSubject['question_time'] = recomQuest[16]
        dictSubject['difficulty_val'] = recomQuest[17]
        dictSubject['recall_papername'] = recomQuest[18]
        dictSubject['quest_source'] = recomQuest[19]
        dictSubject['l_date'] = recomQuest[20]
        dictSubject['recall_label'] = recomQuest[21]
        listQuest.append(dictSubject)
    connGetRecomSubject.close()
    return listQuest
'''
清洗，分词
input:str
return:list
author:roy
dt:2019-05-22
'''
def getCleanSubjiects(listSujects):
    objUtilString = StringUtil()
    #加载TfIdf的停用词
    jiebaAns.set_stop_words(PATH_JIEBA_STOP_WORDS)
    #集合存储返回数据
    listRetSubjects = []

    for dictSubject in listSujects:
        #开始清洗数据
        oriContent = dictSubject['txt_content']
        #全角转半角
        cleanContent = objUtilString.tfQ2B(oriContent)
        #去掉符号
        cleanContent = objUtilString.replaceSubjectTag(cleanContent)
        #存回到集合中
        dictSubject['txt_content_par'] = cleanContent
        #添加关键词字段
        listContentKeywords = jiebaAns.extract_tags(cleanContent.lower(),topK=20,withWeight=False)
        dictSubject['txt_content_keywords'] = ','.join(listContentKeywords)
        #添加关键词词数字段
        dictSubject['txt_content_keywords_len'] = len(listContentKeywords)
        listRetSubjects.append(dictSubject)
    return listRetSubjects

'''
处理空字符串
input:str
return:str
author:roy
dt:2019-05-22
'''
def nullDef(strNull):
    if strNull is None:
        return 'Null'
    return strNull

'''
处理空数字
input:int
return:int
author:roy
dt:2019-05-22
'''
def intNullDef(intNull):
    if intNull is None:
        return 999999999
    return intNull

if __name__ == "__main__":
    #查询数据
    listRecomSujects = getRecomSubjects()
    print('取数完成')
    listCleanSubjects = getCleanSubjiects(listRecomSujects)
    print('清洗完成')
    #开始写出数据
    if os.path.exists(PATH_RECALL_CLEAN) == True:
        os.remove(PATH_RECALL_CLEAN)
        print('删除数据文件')

    fileOut = open(PATH_RECALL_CLEAN,'a+')
    for dictSubject in listCleanSubjects:
        fileOut.write(nullDef(dictSubject['id']) + '\t')
        fileOut.write(nullDef(dictSubject['questno']) + '\t')
        fileOut.write(nullDef(dictSubject['txt_content']) + '\t')
        fileOut.write(nullDef(dictSubject['txt_content_par']) + '\t')
        fileOut.write(nullDef(dictSubject['txt_content_keywords']) + '\t')
        fileOut.write(str(intNullDef(dictSubject['txt_content_keywords_len'])) + '\t')
        fileOut.write(nullDef(dictSubject['txt_content_url']) + '\t')
        fileOut.write(nullDef(dictSubject['txt_answer_url']) + '\t')
        fileOut.write(nullDef(dictSubject['txt_analysis_url']) + '\t')
        fileOut.write(nullDef(dictSubject['png_content_url']) + '\t')
        fileOut.write(nullDef(dictSubject['png_answer_url']) + '\t')
        fileOut.write(nullDef(dictSubject['png_analysis_url']) + '\t')
        fileOut.write(nullDef(dictSubject['html_content_url']) + '\t')
        fileOut.write(nullDef(dictSubject['html_answer_url']) + '\t')
        fileOut.write(nullDef(dictSubject['html_analysis_url']) + '\t')
        fileOut.write(nullDef(dictSubject['three_know_code']) + '\t')
        fileOut.write(nullDef(dictSubject['three_know_name']) + '\t')
        fileOut.write(nullDef(dictSubject['questtype_id']) + '\t')
        fileOut.write(nullDef(dictSubject['questtype_name']) + '\t')
        fileOut.write(nullDef(dictSubject['question_time']) + '\t')
        fileOut.write(nullDef(dictSubject['difficulty_val']) + '\t')
        fileOut.write(nullDef(dictSubject['recall_papername']) + '\t')
        fileOut.write(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + '\t')
        fileOut.write(nullDef(dictSubject['quest_source']) + '\t')
        fileOut.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '\t')
        fileOut.write(nullDef(dictSubject['l_date']) + '\t')
        fileOut.write(nullDef(dictSubject['recall_label']) + '\t')
        fileOut.write('\n')
    fileOut.close()
