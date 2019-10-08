import Levenshtein
import time
import datetime
import sys


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


if __name__ == "__main__":
    MAIN_PATH = '/opt/sys/schoolquestion_examresult/wrongquest-V2.2.0.2018.11.27_release/recall/similar'
    pathSource = MAIN_PATH + '/recall_del_repeat/' + 'recall_check_{}.txt'.format(RUN_TIME)
    print('开始load数据')
    #从文件读取数据
    fileRead = open(pathSource, 'r', encoding='utf-8')
    listSubjects = fileRead.readlines()
    #数据重名一下
    listSubjectsCol = []
    #listSubjects.remove('\r\n')
    for lineSubject in listSubjects:
        arrSubjict = lineSubject.split('\t')
        dictSubject = {}
        dictSubject['y_id'] = arrSubjict[0]
        dictSubject['t_id'] = arrSubjict[1]
        dictSubject['y_quest_source_id'] = arrSubjict[2]
        dictSubject['t_quest_source_id'] = arrSubjict[3]
        dictSubject['simil_value'] = arrSubjict[4]
        listSubjectsCol.append(dictSubject)
    print('结束load数据')
    #开始比对
    print('开始比对')
    listRepeat = []
    listRepeatCheck = []
    i = 0
    for dictSubject in listSubjectsCol:
        if float(dictSubject['simil_value']) >= 0.67 and dictSubject['y_id'] not in listRepeat and dictSubject['t_id'] not in listRepeat and dictSubject['y_id'] != dictSubject['t_id']:
            if dictSubject['y_quest_source_id'] <= dictSubject['t_quest_source_id']:
                listRepeat.append(dictSubject['t_id'])
                listRepeatCheck.append(dictSubject['t_id'] + '|' + dictSubject['y_id'])
            else:
                listRepeat.append(dictSubject['y_id'])
                listRepeatCheck.append(dictSubject['y_id'] + '|' + dictSubject['t_id'])
        i = i + 1
        print(i)

    pathOutRepeat = MAIN_PATH + '/recall_del_repeat/' + 'recall_repeats_{}.txt'.format(RUN_TIME)
    fileRepeat = open(pathOutRepeat,'a+',encoding='utf-8')
    for tid in listRepeat:
        fileRepeat.write(tid + '\n')
    fileRepeat.close()

    pathOutRepeatCheck = MAIN_PATH + '/recall_del_repeat/' + 'recall_repeats_check_{}.txt'.format(RUN_TIME)
    fileRepeatCheck = open(pathOutRepeatCheck,'a+',encoding='utf-8')
    for tid in listRepeatCheck:
        fileRepeatCheck.write(tid + '\n')
    fileRepeatCheck.close()
