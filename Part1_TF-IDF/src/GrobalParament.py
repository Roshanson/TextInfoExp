# -*- coding: utf-8 -*-
import os

# 定义的一些全局变量
InputFormatList = ['utf-8']  # 输入文件的编码列表
OutputFormatList = ['utf-8']  # 输出文件的编码列表
pattern = "full"  # 搜索模式:"full"为全文搜索模式,"keys"为关键词搜索模式
n = 10  # 关键词搜索时的关键词数量
ruler_list = []  # 不需要的字符
result_file_num = 50  # 需要查找多少个相关文档
out_to_file = True  # 是否需要输出为txt
# PreprocessResultDir="TF_IDF\\data"#预处理文件目录

PreprocessResultDir = 'data_afterprocess'
PreprocessResultName = "pro_res.txt"  # 预处理文件名
ResultFileNameDir = "title_and_abs"  # 搜索结果文件目录
ResultFileName = "result.txt"  # 搜索结果文件名

path = '/home/kaifun/PycharmProjects/TextInfoExp/Part1_TF-IDF/'  # 原始数据
path1 = path + 'data/title_and_abs/'
newpath = path + "data/pro_keyword/"
newpath2 = path

# path1 = 'C:/Users/kaifun/Desktop/ass_TIP/TextInfoProcess/Test_one_TF-IDF/data_afterprocess/title_and_abs/'  # 处理后的标题和摘要
# newpath='C:/Users/kaifun/Desktop/ass_TIP/TextInfoExp/Part3_Text_Cluster/data_afterprocess/pro_keyword/'
# newpath2='C:/Users/kaifun/Desktop/ass_TIP/TextInfoExp/Part3_Text_Cluster/data_afterprocess/keyword/'
