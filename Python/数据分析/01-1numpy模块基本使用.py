import numpy

# 创建一维数组格式      --numpy.array
x = numpy.array(['a','1','b','2'])
print(x)

# 创建二维数组格式      --numpy.array
y = numpy.array([[3,2,1],[6,5,4],[9,8,7]])
print(y)

# 查看数组类型        --.dtype
print('x的数组类型：' + str(x.dtype))
print('y的数组类型：' + str(y.dtype))

# 查看数组维度        --.shape
print('x的数组维度：' + str(x.shape))
print('y的数组维度：' + str(y.shape))

# 取出数组中的某个值
print(x[2])
print(y[1][2])

# 对数组进行排序       --.sort()
x.sort()
y.sort()
print(x)
print(y)

# 取数组中 最大值、最小值      --.max()  \  .min()
y_max = y.max()
y_min = y.min()
print(y_max)
print(y_min)

# 切片
# 一位数组切片
x1 = x[0:2]
# 取所有二维数组下的每个二维数组的第0个元素
y1 = y[:,0]
print('x1 = ' + str(x1))
print('y1 = ' + str(y1))
