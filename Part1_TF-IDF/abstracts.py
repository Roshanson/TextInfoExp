# encoding:utf-8

import os
import sys
from bs4 import BeautifulSoup

abstracts = []
reload(sys)
sys.setdefaultencoding("utf-8")

# path='/home/mbtrec/mhwang/pro/computer/'
path = 'C:/Users/kaifun/Desktop/ass_TIP/TextInfoProcess/Test_one_TF-IDF/data/computer/'  # 原始数据
path1 = 'C:/Users/kaifun/Desktop/ass_TIP/TextInfoProcess/Test_one_TF-IDF/data_afterprocess/title_and_abs/'  # 处理后的标题和摘要
newpath = 'C:/Users/kaifun/Desktop/ass_TIP/TextInfoProcess/Test_one_TF-IDF/data_afterprocess/pro_keyword/'
newpath2 = 'C:/Users/kaifun/Desktop/ass_TIP/TextInfoProcess/Test_one_TF-IDF/data_afterprocess/keyword/'

filelist = os.listdir(path)  # 取得当前路径下的所有文件
for files in filelist:
    filename = os.path.splitext(files)[0]  # 取文件名
    soup = BeautifulSoup(open(path + filename + '.xml'), 'html.parser')
    b = soup.find("p", class_="abstracts")
    if b is None or b.string is None:
        continue
    else:
        abstracts.extend(soup.title.stripped_strings)
        s = b.string
        abstracts.extend(s.encode('utf-8'))
        f = open(path1 + filename + ".txt", "w+")
        for i in abstracts:
            f.write(i)
        f.close()
        abstracts = []

    # getPro_keyword
    links = soup.find_all("dl")
    for link in links:
        s1 = link.get_text()
    f = open(newpath + filename + ".txt", "w+")  # 将得到的未处理的文字放在pro_keyword文件夹中
    for i in s1:
        f.write(i)
    f.close()

# getKeyword
filelist = os.listdir(newpath)
for files in filelist:
    filename = os.path.splitext(files)[0]
    begin = 100000
    end = 10000
    f1 = open(newpath + filename + ".txt", "r")
    f2 = open(newpath2 + filename + '.txt', "w+")
    for (num, value) in enumerate(f1):
        if value.count("关键词") > 0:  # 得到关键词的行号
            begin = num
        if value.count("基金项目") > 0 or value.count("机标分类号") > 0 or value.count("机标关键词") > 0 or value.count(
                "基金项目") > 0 or value.count("DOI") > 0:
            end = num
        if num > begin and num < end and value[:-1].strip():
            f2.write(value.strip())
            f2.write(" ")
    f1.close()
    f2.close()
