
#-*- coding: utf-8 -*-
import pandas as pd
import Levenshtein
import collections
import csv
import time

#------------------- 获得推荐题库的数据

csv_file = csv.reader(open('tuijian_question.txt','r',encoding="utf-8"))   # 读入推荐题库的原始数据

list1 = []
for row_content in csv_file:
     str1 = "".join(row_content)
     list1.append(str1.split('\t', 10))

data1 = pd.DataFrame(list1)
data1.columns = ['试题id','题型id','题型名称','知识点编码','知识点名称','召回源标签','召回题试卷名称','试题来源','txt格式题干','png格式题干','文本题干']

data1 = data1[['试题id','题型名称','知识点名称','召回源标签','试题来源','文本题干']]

data1.columns = ['TID','题型名称','知识点名称','召回源标签','试题来源','题干']

data1 = data1.drop_duplicates(['TID'])

data1 = data1.dropna(subset = ['题干'])

data1['优先标签'] = data1.召回源标签.apply(lambda x: 1 if x == 4 else (2 if x == 3 else (3 if x == 6 else (4 if x == 5 else (5 if x == 2 else (6 if x == 1 else 7))))))

data1 = data1.sort_values(by=['试题来源','优先标签'],ascending= [False,True]).reset_index(drop=True)

print("number of rows is", data1.shape[0])

#------------------- 按题型划分推荐题库数据

data2 = data1[data1['题型名称'].isin(['单选题','判断题','多选题'])]

data3 = data1[data1['题型名称'] == '填空题'] 

data4 = data1[data1['题型名称'] == '解答题'] 

#------------------- 对'单选题','判断题','多选题'题型去除重复题

def quchong(frame):
   
      frame = frame[['TID','题干']] 
      frame.columns = ['TID','Content']
      
      d = zip(frame['TID'],frame['Content'])

      e = collections.OrderedDict(list(d))
      
      for k1 in e:
          
          if isinstance(e[k1], str) == False:
             e[k1] = str(e[k1])
          
          e[k1] = "".join(e[k1].split())
          e[k1] = e[k1].replace('\ufeff', '')
          
          temp = e[k1]
       
          j = 0
          for i, w in enumerate(temp):
              if w == '分' and j < 1:
                 if i >= len(temp) - 1 or i > 11:
                    temp = temp 
                 elif temp[i + 1] == '）' or temp[i + 1] == ')' or temp[i + 1] == '】':   
                    temp = temp[i + 2:]
                    j = j + 1
                 else:
                    temp = temp
          
          for i, w in enumerate(temp):
              if w in {'苏','东','卷','拟','模','北','江','京','建','中','末'}:     # w == '苏' or '东' or '卷' 这样的写法是错误的
                 if i >= len(temp) - 1 or i > 16:
                    temp = temp
                 elif temp[i + 1] == '）' or temp[i + 1] == ')' or temp[i + 1] == '】':
                    temp = temp[i + 2:]
                   
          if len(temp) > 2 and "xmlversion" not in temp:
             if temp[0].isdigit():
                j = 0
                for i, w in enumerate(temp):
                    if w >= u'\u4e00' and w <= u'\u9fa5' and j < 1:
                       temp = temp[i:]
                       j = j + 1      
      
          temp = temp.replace('＝', '=')
          temp = temp.replace('＋', '+')
          temp = temp.replace('－', '-')
          
          temp = temp.replace(',', '，')
          temp = temp.replace(')', '）')
          temp = temp.replace('(', '（')
          
          temp = temp.replace('[', '【')
          temp = temp.replace(']', '】') 
          temp = temp.replace(';', '；')
          
          e[k1] = temp
                 
      str_TID = []
      new_TID = []
      temp_index = set()
      new_content = []
      sim_ratio = []
      i = 0
      
      for k1, v1 in e.items():
          
         i = i + 1
         if i % 50 == 0:
            print("i is", i)
            print("duration is", (time.clock() - start))
        
         if k1 not in temp_index:
             str_TID.append(k1)
             new_TID.append(k1) 
             temp_index.add(k1)
             new_content.append(v1)
             sim_ratio.append(1)
      
             for k2, v2 in e.items():  
      
                 if k2 not in temp_index:
                    temp_ratio = round(Levenshtein.ratio(v2, v1),3) 
                    if temp_ratio >= 0.67:   # 0.7 0.6  0.65  0.85
                       new_TID.append(k1)
                       temp_index.add(k2)
                       str_TID.append(k2)
                       new_content.append(v2)
                       sim_ratio.append(temp_ratio)
       
      df01=pd.DataFrame(str_TID)
      df01.columns = ['TID']
      
      df02=pd.DataFrame(new_TID)
      df02.columns = ['new_TID']
      
      df03=df01.join(df02)
      
      df04=pd.DataFrame(new_content)
      df04.columns = ['new_content']
      
      df03=df03.join(df04)
      
      df044=pd.DataFrame(sim_ratio)
      df044.columns = ['sim_ratio']
      
      df03=df03.join(df044)
      
      datanew = df03.sort_values(by=['new_TID', 'sim_ratio'],ascending= [False,False]).reset_index(drop=True)
      
      datanew = datanew[['TID','new_TID','sim_ratio','new_content']]

      return datanew

start = time.clock()

datanew2 = quchong(data2)

datanew3 = quchong(data3)

datanew4 = quchong(data4)

#------------------- 把推荐题库中各种题型的查重结果组合起来，进行去除重复，并输出中间结果

frames = [datanew2, datanew3, datanew4]

result = pd.concat(frames)

result_quchong = pd.merge(result, data1, how='left', on=['TID'])

result_quchong = result_quchong[['TID','new_TID','sim_ratio','试题来源','召回源标签','知识点名称','题型名称','题干','new_content']]

result_quchong = result_quchong.sort_values(by=['new_TID', 'sim_ratio'],ascending= [False,False]).reset_index(drop=True)

re_file = 'tuijian_allid_final0516.txt'
result_quchong.to_csv(re_file) 

result = result[result['TID'] == result['new_TID']] 
result = result[['TID','new_content']]

result1 = pd.merge(result, data1, how='left', on=['TID'])

result_save = result1[['TID','试题来源','召回源标签','知识点名称','题型名称','题干','new_content']]

re_file = 'tuijian_quchong_final0516.txt'
result_save.to_csv(re_file) 

result1 = result1[['TID','题型名称','知识点名称','new_content']]

#------------------- 获得校本题库数据

csv_file = csv.reader(open('xiaoben_question.txt','r',encoding="utf-8"))   # 读入校本题库的原始数据

list1 = []
for row_content in csv_file:
     #print(row_content)
     str1 = "".join(row_content)
     list1.append(str1.split('\t', 4))

data_xiaoben = pd.DataFrame(list1)
data_xiaoben.columns = ['校本试题id','题型','知识点编码','知识点名称','题干']

data_xiaoben = data_xiaoben[['校本试题id','题型','知识点名称','题干']]
data_xiaoben.columns = ['校本试题id','题型名称','知识点名称','校本题干']

data_xiaoben = data_xiaoben.dropna(subset = ['校本题干'])

data_xiaoben = data_xiaoben.dropna(subset = ['知识点名称'])

print("number of rows is", data_xiaoben.shape[0])

data_xiaoben.columns = ['TID','Tixin','ZSD','Content']

d = zip(data_xiaoben['TID'],data_xiaoben['Content'])

e = collections.OrderedDict(list(d))

for k1 in e:
    
    if isinstance(e[k1], str) == False:
       e[k1] = str(e[k1])
    
    e[k1] = "".join(e[k1].split())
    e[k1] = e[k1].replace('\ufeff', '')
    
    temp = e[k1]
 
    j = 0
    for i, w in enumerate(temp):
        if w == '分' and j < 1:
           if i >= len(temp) - 1 or i > 11:
              temp = temp 
           elif temp[i + 1] == '）' or temp[i + 1] == ')' or temp[i + 1] == '】':   
              temp = temp[i + 2:]
              j = j + 1
           else:
              temp = temp
    
    for i, w in enumerate(temp):
        if w in {'苏','东','卷','拟','模','北','江','京','建','中','末'}:
           if i >= len(temp) - 1 or i > 16:
              temp = temp
           elif temp[i + 1] == '）' or temp[i + 1] == ')' or temp[i + 1] == '】':
              temp = temp[i + 2:]
             
    if len(temp) > 2 and "xmlversion" not in temp:
       if temp[0].isdigit():
          j = 0
          for i, w in enumerate(temp):
              if w >= u'\u4e00' and w <= u'\u9fa5' and j < 1:
                 temp = temp[i:]
                 j = j + 1      
    
    temp = temp.replace('＝', '=')
    temp = temp.replace('＋', '+')
    temp = temp.replace('－', '-')
  
    temp = temp.replace(',', '，')
    temp = temp.replace(')', '）')
    temp = temp.replace('(', '（')  
        
    temp = temp.replace('[', '【')
    temp = temp.replace(']', '】') 
    temp = temp.replace(';', '；')
    
    e[k1] = temp
              
dict1 = pd.DataFrame.from_dict(e,orient='index',columns=['Content'])
dict1 = dict1.reset_index().rename(columns = {'index':'TID'})

dict1.columns = ['TID','New_XiaobenContent']

data22 = pd.merge(data_xiaoben, dict1, on = 'TID', how='left')

data22 = data22[['Content','TID','New_XiaobenContent','ZSD','Tixin']]

data22.columns = ['Content','Xiaoben_TID','New_XiaobenContent','知识点名称','题型名称']

#-------------------  校本题库与查重后的推荐题库，根据 '题型名称' 和'知识点名称' 这两个字段 join，并计算校本题与推荐题之间的相关度

result2 = pd.merge(data22, result1, how='inner', on=['题型名称','知识点名称'])

result2 = result2[['Xiaoben_TID','题型名称','知识点名称','New_XiaobenContent','TID','new_content']]

sim_ratio = []
xiaoben_id = []
TID = []
xiaoben_content = []
tuijian_content = []
tixing = []
zsd = []

for index1, data_str1 in result2.iterrows():
    sim_ratio.append(round(Levenshtein.ratio(data_str1[3], data_str1[5]),3))

    xiaoben_id.append(data_str1[0])
    tixing.append(data_str1[1])
    zsd.append(data_str1[2])
    xiaoben_content.append(data_str1[3])
    TID.append(data_str1[4])
    tuijian_content.append(data_str1[5])

df01=pd.DataFrame(sim_ratio)
df01.columns = ['sim_ratio']

df02=pd.DataFrame(xiaoben_id)
df02.columns = ['xiaoben_id']

df03=df01.join(df02)

df05=pd.DataFrame(tixing)
df05.columns = ['tixing']

df03=df03.join(df05)

df06=pd.DataFrame(zsd)
df06.columns = ['zsd']

df03=df03.join(df06)

df07=pd.DataFrame(xiaoben_content)
df07.columns = ['xiaoben_content']

df03=df03.join(df07)

df08=pd.DataFrame(TID)
df08.columns = ['TID']

df03=df03.join(df08)

df09=pd.DataFrame(tuijian_content)
df09.columns = ['tuijian_content']

df03=df03.join(df09)

df03 = df03[['xiaoben_id','sim_ratio','zsd','tixing','xiaoben_content','TID','tuijian_content']]

df03 = df03.sort_values(by=['xiaoben_id', 'sim_ratio'],ascending= [False,False]).reset_index(drop=True)
      
#-------------------  输出推荐相关度的样例数据以及最终的结果数据

df03_save = df03[0:30000]
re_file = 'tuijian_example_final0516.txt'
df03_save.to_csv(re_file) 

df03 = df03[['xiaoben_id','sim_ratio','TID','tixing','zsd']]
#re_file = 'tuijian_sim_final0516.txt'                               # 算法组可选择的数据格式：有字段名，并且以逗号分隔
#df03.to_csv(re_file)

re_file = 'tuijian_shuju_final0516.txt'                              # 数据组需要的数据格式：没有字段名，并且以TAB分隔  
df03.to_csv(re_file, sep = '\t',encoding = 'utf-8', header = None)

elapsed = (time.clock() - start)
print("Time used:",elapsed)
