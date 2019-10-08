#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from urllib import request
import re,xlwt,datetime

# 读取网页源代码内容
html = request.urlopen('https://read.douban.com/provider/all').read()
html = html.decode('utf-8')
# print(html)

pattern = '<li><a href="(.*?)" class="provider-item"><div class="col-media"><div class="cm-left avatar"><div class="avatar"><img src=(.*?)"/></div></div><div class="cm-body"><div class="name">(.*?)</div><div class="works-num">(.*?) 部作品在售</div></div></div></a></li>'


# 通过正则表达式匹配在网页源代码中提取所需内容
content = re.compile(pattern).findall(html)
# print(content[0])


# 创建workbook和sheet对象
# 创建一个workbook 设置编码
workbook = xlwt.Workbook(encoding = 'utf-8')
# 创建一个worksheet
sheet1 = workbook.add_sheet('数据',cell_overwrite_ok = True)

# 初始化excel样式
style = xlwt.XFStyle()

# 为样式创建字体
font = xlwt.Font()
font.name = 'Times New Roman'
# 黑体
font.bold = True 
# 下划线
font.underline = False
# 斜体字
font.italic = False 

#设置样式的字体
style.font = font 

#在sheet1表的第1行设置字段名称并写入数据
sheet1.write(0,0,"序号",style)
sheet1.write(0,1,"出版社-URL",style)
sheet1.write(0,2,"LOGO-URL",style)
sheet1.write(0,3,"出版社名称",style)
sheet1.write(0,4,"在售作品数量",style)

# 定义行号初始值
a = 0
# 定义在售数量初始值
h = 0

for i in content:
    # print(str(a+1),i[0])
    # 在第 a+1 行第 1 列写入序号
    sheet1.write(a+1,0,a+1,style)
    # 在第 a+1 行第 2 列写入出版社URL
    sheet1.write(a+1,1,"https://read.douban.com"+str(i[0]),style)
    # 在第 a+1 行第 3 列写入LOGO-URL
    sheet1.write(a+1,2,i[1],style)
    # 在第 a+1 行第 4 列写入出版社名称
    sheet1.write(a+1,3,i[2],style)
    # 在第 a+1 行第 5 列写入在售数量
    sheet1.write(a+1,4,int(i[3]),style)
    # 在售数量累计求和
    h += int(i[3])                                                    
    a += 1

    # 判断 content 列表是否遍历结束，并在 sheet1 表尾行写入在售数量求和的值
    if a==a:                                                        
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dayid = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        # 在sheet1表尾行写入“合计”
        sheet1.write(a+1,3,"合计",style)
        # 在sheet1表尾行写入在售数量累计值
        sheet1.write(a+1,4,h,style)
        # 在sheet1表尾行写入数据采集时间
        sheet1.write(a+2,3,"采集时间",style)
        # 在sheet1表尾行写入数据采集时间
        sheet1.write(a+2,4,time,style)                                 

# 保存该excel文件,有同名文件时无法直接覆盖
workbook.save("D:\\Python\\Project\\爬虫\\result\\01-2\\豆瓣出版社汇总表"+str(dayid)+".xlsx")                 

print("数据写入excel文件完毕！")
print("在售书数量合计："+str(h))
