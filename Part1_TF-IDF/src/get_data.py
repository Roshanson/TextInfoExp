# encoding:utf-8

import os
import sys
from bs4 import BeautifulSoup
import os
import GrobalParament

reload(sys)
sys.setdefaultencoding("utf-8")

# base_path = os.getcwd().replace('\\', '/')
# print base_path

# path='/home/mbtrec/mhwang/pro/computer/'
base_path = GrobalParament.path
path = base_path + 'data/computer/'# 原始数据
path1 = base_path + 'data/title_and_abs/'  # 处理后的标题和摘要
newpath = base_path + 'data/pro_keyword/'
newpath2 = base_path + 'data/keyword/'

filelist = os.listdir(path)  # 取得当前路径下的所有文件


# 清洗出xml格式的文件中的标题和摘要信息
def get_text():
    abstracts = []
    for files in filelist:
        filename = os.path.splitext(files)[0]  # 取文件名
        soup = BeautifulSoup(open(path + filename + '.xml'), 'html.parser')  # 解析网页
        b = soup.find("p", class_="abstracts")  # 取得"p", class_="abstracts"为标签的内容
        # print b
        if b is None or b.string is None:
            continue
        else:
            abstracts.extend(soup.title.stripped_strings)
            s = b.string
            abstracts.extend(s.encode('utf-8'))
            f = open(path1 + filename + ".txt", "w+")  # 写入txt文件
            for i in abstracts:
                f.write(i)
            f.close()
            abstracts = []

        # getPro_keyword，清洗出xml文件中dl标签中的文本信息
        links = soup.find_all("dl")
        # print links
        for link in links:
            s1 = link.get_text()
            # print s1
        f = open(newpath + filename + ".txt", "w+")  # 将得到的未处理的文字放在pro_keyword文件夹中
        for i in s1:
            f.write(i)
        f.close()


# 对上一步得到的getPro_keyword文件夹中的文件进行进一步处理，得到每个文件的关键字
def get_keyword():
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


if __name__ == '__main__':
    get_text()
    # get_keyword()
