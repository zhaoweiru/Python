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

SQL_RECALL_SOURCE_QUESTIONS = '''select grade_base_id,paper_question_id
                                ,data_center_id,vector,txt_content,txt_content_url
                                ,questtype_id,questtype_name,three_know_code
                                ,three_know_name,batch_id,load_time,txt_content_clean
                                ,par_words_ct,par_words,l_date
                                  from jk_mid_recall_source.fact_paperquestion_basic_content_info
                                 where l_date = '''+L_DATE+''' '''
MAIN_PATH = '/opt/sys/schoolquestion_examresult/wrongquest-V2.2.0.2018.11.27_release/recall/similar'
PATH_XIAOBEN_CLEAN = MAIN_PATH + '/' + 'clean_content/' + 'xiaoben_cleaned_{}.txt'.format(RUN_TIME)
PATH_JIEBA_KEYWORDS = MAIN_PATH + '/' + 'jieba_key_words.txt'
PATH_JIEBA_STOP_WORDS = MAIN_PATH + '/' + 'jieba_stop_words.txt'

'''
从hive获取题的信息数据
input:str
return:str
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
        dictSubject['grade_base_id'] = recomQuest[0]
        dictSubject['paper_question_id'] = recomQuest[1]
        dictSubject['data_center_id'] = recomQuest[2]
        dictSubject['vector'] = ''
        dictSubject['txt_content'] = recomQuest[4]
        dictSubject['txt_content_url'] = recomQuest[5]
        dictSubject['questtype_id'] = recomQuest[6]
        dictSubject['questtype_name'] = recomQuest[7]
        dictSubject['three_know_code'] = recomQuest[8]
        dictSubject['three_know_name'] = recomQuest[9]
        dictSubject['l_date'] = recomQuest[15]
        listQuest.append(dictSubject)
    connGetRecomSubject.close()
    return listQuest
'''
清洗，分词
input:str
return:str
author:roy
dt:2019-05-22
'''
def getCleanSubjiects(listSujects):
    objUtilString = StringUtil()
    #TfIdf的停用词
    jiebaAns.set_stop_words(PATH_JIEBA_STOP_WORDS)
    
    listRetSubjects = []
    for dictSubject in listSujects:
        #开始清洗数据
        oriContent = dictSubject['txt_content']
        if oriContent:
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
        else:
            dictSubject['txt_content_par'] = ''
            dictSubject['txt_content_keywords'] = ''
            dictSubject['txt_content_keywords_len'] = ''
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
input:str
return:str
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
    if os.path.exists(PATH_XIAOBEN_CLEAN) == True:
        os.remove(PATH_XIAOBEN_CLEAN)
        print('删除数据文件')

    fileOut = open(PATH_XIAOBEN_CLEAN,'a+')
    for dictSubject in listCleanSubjects:
        fileOut.write(nullDef(dictSubject['grade_base_id']) + '\t')
        fileOut.write(nullDef(dictSubject['paper_question_id']) + '\t')
        fileOut.write(nullDef(dictSubject['data_center_id']) + '\t')
        fileOut.write(nullDef(dictSubject['vector']) + '\t')
        fileOut.write(nullDef(dictSubject['txt_content']) + '\t')
        fileOut.write(nullDef(dictSubject['txt_content_par']) + '\t')
        fileOut.write(nullDef(dictSubject['txt_content_keywords']) + '\t')
        fileOut.write(str(intNullDef(dictSubject['txt_content_keywords_len'])) + '\t')
        fileOut.write(nullDef(dictSubject['txt_content_url']) + '\t')
        fileOut.write(nullDef(dictSubject['questtype_id']) + '\t')
        fileOut.write(nullDef(dictSubject['questtype_name']) + '\t')
        fileOut.write(nullDef(dictSubject['three_know_code']) + '\t')
        fileOut.write(nullDef(dictSubject['three_know_name']) + '\t')
        fileOut.write(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + '\t')
        fileOut.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '\t')
        fileOut.write('\n')
    fileOut.close()