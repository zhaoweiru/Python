import pandas as pd 

# 数据导入
i = pd.read_csv('D:\\Python\\数据分析\\源码\\第5周\\hexun.csv',encoding = 'gb18030')
print(i.describe())

