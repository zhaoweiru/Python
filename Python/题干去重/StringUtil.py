# -*- coding: utf-8 -*-
import jieba
import re

class StringUtil(object):
    #声明正则模板
    templSubjectSerial = '(^[0-9]+)[.，、]'    #去除题号，如：1.
    templSubjectScore = '(^[\（\(])([0-9]+)(分)([\)\）])'    #去除分数 如(14分)
    templSubjectFrom = '(^[\（\(])(.+?)([苏东卷拟模北江京建中末省市])([\)\）])'    #去掉来源
    templSubjectFlag = '[,.;:\"!?，。 _　：；！？、．（）]'
    
    '''
    格式化字符串，替换不需要的符号
    input:str
    return:str
    author:roy
    dt:2019-05-18
    '''
    def replaceSubjectTag(self,strOri):
        #先处理序号
        strReplaced = re.sub(self.templSubjectSerial,'',strOri)
        strReplaced = re.sub(self.templSubjectScore,'',strReplaced)
        strReplaced = re.sub(self.templSubjectFrom,'',strReplaced)
        strReplaced = re.sub(self.templSubjectScore,'',strReplaced)
        #先处理来源
        strReplaced = re.sub(self.templSubjectFrom,'',strReplaced)
        strReplaced = re.sub(self.templSubjectSerial,'',strReplaced)
        strReplaced = re.sub(self.templSubjectScore,'',strReplaced)
        strReplaced = re.sub(self.templSubjectSerial,'',strReplaced)
        #先处理分
        strReplaced = re.sub(self.templSubjectScore,'',strReplaced)
        strReplaced = re.sub(self.templSubjectFrom,'',strReplaced)
        strReplaced = re.sub(self.templSubjectSerial,'',strReplaced)
        strReplaced = re.sub(self.templSubjectFrom,'',strReplaced)
        strReplaced = re.sub(self.templSubjectFlag,'',strReplaced)
        strReplaced = strReplaced.replace('\n','').replace('\n','').replace('\r','').replace('\r\n','').replace(' ','').replace('\t','')
        #strReplaced = strReplaced.replace('dfrac','').replace('\\','').replace('{','').replace('}','').replace('(','').replace(')','').replace('&gt','>').replace('&lt','<').replace('begin','').replace('cases','').replace('geqslant','>=').replace('leqslant','<=')
        return strReplaced
    
    '''
    格式化字符串，全角转半角
    input:str
    return:str
    author:roy
    dt:2019-05-18
    '''
    def tfQ2B(self,strOri):
        strB = ''
        #遍历所有字母
        for letter in strOri:
            charCode = ord(letter)
            #全角空格直接转换
            if charCode == 12288:
                charCode = 32
            elif charCode >= 65281 and charCode <= 65374:
                charCode = charCode - 65248
            strB = strB + chr(charCode)
        return strB

    '''
    格式化字符串，半角转全角
    input:str
    return:str
    author:roy
    dt:2019-05-18
    '''
    def tfB2Q(self,strOri):
        strQ = ''
        #遍历所有字母
        for letter in strOri:
            charCode = ord(letter)
            #全角空格直接转换
            if charCode == 32:
                charCode = 12288
            elif charCode >= 33 and charCode <= 126:
                charCode = charCode + 65248
            strQ = strQ + chr(charCode)
        return strQ

    '''
    加载停用词，用于jieba分词
    input:停用词词表的路径
    return:list
    author:roy
    dt:2018-11-19
    '''
    def getCutStopWords(self,dtFilePath):
        listMyCutStopWords = [line.split('\n')[0] for line in open(dtFilePath, 'r', encoding='utf-8').readlines()]
        return listMyCutStopWords
