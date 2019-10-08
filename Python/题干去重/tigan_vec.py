# -*- coding: UTF-8 -*-
import os
import time
import numpy as np
import gensim
import sys
from pyhive import hive

global dateInput

#执行文件的时候，第一个参数是日期
try:
    dateInput = sys.argv[1]
except:
    print('=======没有加入时间参数========')

class HiveClient(object):

    def __init__(self, db_host, hdatabase, hport=10000):
        #初始化hive连接
        self.connHive = hive.Connection(host=db_host, port=hport,  database=hdatabase)

    '''
    执行sql查询
    input:sql
    author:roy
    dt:2019-05-14
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
    dt:2019-05-14
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
    dt:2019-05-14
    '''
    def close(self):
        self.connHive.close()

 # 线上hive：192.168.128.69
 # 测试hive: 192.168.97.41
HIVE_ONLINE_IP = '192.168.128.69'
HIVE_ONLINE_ORI_DB_NAME = 'jk_mid_recall_source'
HIVE_ONLINE_PORT = 10000

'''
下面开始算向量
'''
#取校本题干信息的sql，这里要注意，题干字段换成清洗与分词后的
SQL_GET_ORI_SUBJECT = "select paper_question_id,par_words from  fact_paperquestion_basic_content_info where par_words is not NULL and l_date='{v_date}'"
#取推荐题干信息的sql，这里要注意，题干字段换成清洗与分词后的
SQL_GET_RECOMM_SUBJECT = "select questno,par_words from fact_recall_source_question_bank  where par_words  is not NULL and l_date='{v_date}'"



'''
连接hive取题信息，主要是取校本题
author:roy
dt:2019-05-15
'''
def getOriSubInHive():
    connGetOriSubject = HiveClient(HIVE_ONLINE_IP,HIVE_ONLINE_ORI_DB_NAME,HIVE_ONLINE_PORT)
    sqlExecOri = SQL_GET_ORI_SUBJECT.format(v_date=dateInput)
    #打印测试sql拼接变量，上线要去掉
    subjectOriResult = connGetOriSubject.query(sqlExecOri)
    #保存查询结果的list
    #原listOriQuest = subjectOriResult
    listOriQuest = []
    #这是个测试行数的计数器，上线要去掉
    for questOri in subjectOriResult:
        #如果没有题干，跳过不处理
        if  len(questOri[1]) == 0 :
            continue
        dictOriSubject = {}
        dictOriSubject['quest_id'],dictOriSubject['quest_txt'] = questOri[0],questOri[1]
        listOriQuest.append(dictOriSubject)
    connGetOriSubject.close()
    return listOriQuest

'''
连接hive取题信息，主要是取推荐题
author:roy
dt:2019-05-15
'''
def getRecomSubInHive():
    getRecomSubInHive = HiveClient(HIVE_ONLINE_IP,HIVE_ONLINE_ORI_DB_NAME,HIVE_ONLINE_PORT)
    sqlExecRecom = SQL_GET_RECOMM_SUBJECT.format(v_date=dateInput)
    subjectRecomResult = getRecomSubInHive.query(sqlExecRecom)
    #保存查询结果的list
    listRecomQuest = []
    for questRecom in listRecomQuest:
        dictRecomSubject = {}
        dictRecomSubject['quest_id'], dictRecomSubject['quest_txt'] = questRecom[0],questRecom[1]
        listRecomQuest.append(dictRecomSubject)
    getRecomSubInHive.close()
    return listRecomQuest

def outVecToFile(vector,savePath):
    quest_ori_id = vector['quest_id']
    quest_ori_vec = vector['tigan_vec']
    quest_ori_vec_format = str(quest_ori_vec).replace('\n','').replace('\t','')
    with open(savePath,'a+') as objFile:
        objFile.write(quest_ori_id +'\t')
        objFile.write(quest_ori_vec_format +'\t')
        objFile.write('\n')

#获取当前的执行路径
atPath = os.getcwd()
#加载word2vec提前训练好的文件
model = gensim.models.Word2Vec.load(atPath+'/cal_vector_similar_py/words_w2v_0118.model')

#获取关键词
fileKeyWord = open(atPath + '/cal_vector_similar_py/data/math_key_words.txt')
listKeyWords = [keyWord.strip('\n') for keyWord in fileKeyWord]

def getSentenceVector(subContent):
    words = subContent.split(',')
    v = np.zeros(100)
    num=0
    for word in words:
        if word in listKeyWords:
            try:
            	#如果是关键词，权重*2
                v += 2*model[word]
                num+=2
            except KeyError:
                pass
        else:
            try:
                v += model[word]
                num+=1
            except KeyError:
                pass
    v /= (num if num>0 else 1)
    return v

'''
计算vec的向量值
author:roy
dt:2019-05-15
'''
def getSubjectVec(dictSubject):
	#定义一个list存结果，但是每次处理一道题，为啥用list还不知道，暂时不动
    listQuest = []
    #获取数据
    questId = dictSubject['quest_id']
    subContent = dictSubject['quest_txt']
    
    #计算向量值
    dictSubVec = {}
    subVec = getSentenceVector(subContent)
    dictSubVec['tigan_vec'],dictSubVec['quest_id'] = subVec,questId
    listQuest.append(dictSubVec)
    return listQuest


'''
main方法
'''

if __name__ == "__main__":
    #记录开始运行时间
    startTime = time.time()
    #获得校本题的题干
    listOriSubjects = getOriSubInHive()
    saveOriPath = atPath + '/cal_vector_similar_py/data_txt/xiaob/'
    #如果相似度相关文件已经存在就删除
    if os.path.exists(saveOriPath + 'fact_paperquestion_basic_content_info_{}.txt'.format(dateInput)) == True:
        os.remove(saveOriPath + 'fact_paperquestion_basic_content_info_{}.txt'.format(dateInput))
        print('当前存在相似度文件夹已删除')
    #拼接完整的写出文件路径
    saveOriFullPath = saveOriPath + 'fact_paperquestion_basic_content_info_{}.txt'.format(dateInput)
    #开始对校本题生成向量
    for oriSubject in listOriSubjects:
        try:
            listSubVectors = getSubjectVec(oriSubject)
            for dictSubVecs in listSubVectors:
            	#调用outFile方法，数据写入文件
                outVecToFile(dictSubVecs,saveOriFullPath)
        except Exception as e:
            print(e)
    #记录运行结束时间      
    endTime = time.time()
    print('算校本题向量，程序运行时间：%.2fs'%(endTime - startTime))
    
    '''
    下面开始计算推荐题的向量
    '''
    startTime = time.time()
    #获得推荐题的题干
    listRecomSubjects = getRecomSubInHive()
    saveRecomPath = atPath + '/cal_vector_similar_py/data_txt/zhaohy/'
    if os.path.exists(saveRecomPath + 'fact_recall_source_question_bank_{}.txt'.format(dateInput)) == True:
        os.remove(saveRecomPath + 'fact_recall_source_question_bank_{}.txt'.format(dateInput))
        print('当前存在相似度文件夹已删除')
    #拼接完整的写出文件路径
    saveRecomFullPath = saveRecomPath + 'fact_recall_source_question_bank_{}.txt'.format(dateInput)
    
    for recomSuject in listRecomSubjects:
        try:
            listSubVectors = getSubjectVec(recomSuject)
            for dictSubVecs in listSubVectors:
                outVecToFile(dictSubVecs,saveRecomFullPath)
        except Exception as e:
            print (e)
    endTime = time.time()
    print('程序运行时间：%.2fs'%(endTime - startTime))
