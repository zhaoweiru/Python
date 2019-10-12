import pandas as pd 

# Series
# DataFrame

# 通过数组的形式创建数据框
# 默认索引      --.Series
a = pd.Series([3,6,9,23])
print(a)

# 指定索引      --.Series
b = pd.Series([3,6,9,23],['one','tow','three','four'])
print(b)

# 默认列名
c = pd.DataFrame([[4,7,12,8],[78,3,2,9],[47,2,98,1]])
print(c)

# 指定列名      --columns
d = pd.DataFrame([[4,7,12,8],[78,3,2,9],[47,2,98,1]],columns = ['one','tow','three','four'])
print(d)

# 通过字典的形式创建数据框
e = pd.DataFrame({
    'one':0,
    'two':[4,5,6],
    'three':list('abc')
    })
print(e)

# 显示数据框头部数据前 n 行，默认为 5      --.head()
print('d.head():')
print(str(d.head()))
print('d.head(2):')
print(d.head(2))

# 显示数据框尾部数据前 n 行，默认为 5      --.tail()
print('d.tail():')
print(str(d.tail()))
print('d.tail(2):')
print(d.tail(2))

# 展示所有数据统计情况        --describe()
# count:行数,mean:平均数,std:标准差,min:最小值,25%:分位数,50%:分位数,75%:分位数,max:最大值
print(d.describe())

# 转置        -T
print(d.T)
