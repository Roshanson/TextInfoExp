# encoding:utf-8

import os
import sys
import re
import jieba
import random
import string
import pandas as pd
from sklearn import metrics

reload(sys)
sys.setdefaultencoding("utf-8")


# 将文本汇总成一个txt
def get_text():
    base_path = "C:/Users/kaifun/Desktop/ass_TIP/TextInfoExp/Part3_Text_Cluster/data/"
    filelist = os.listdir(base_path)
    data_dict = {}
    with open('../data.txt', 'w') as f2:
        for files in filelist:
            # print (files)
            f = open(base_path + files, 'r')
            text = f.read().replace('\n', '')

            data_temp = text.decode('utf-8')  # 转换为unicode编码形式
            data = ''.join(re.findall(u'[\u4e00-\u9fff]+', data_temp))  # 必须为unicode类型，取出所有中文字符
            f2.write(data.encode('utf-8') + '\n')
            # data2 = jieba.cut(data)  # 分词
            # data3 = " ".join(data2)  # 结果转换为字符串（列表转换为字符串）
            # data_dict[data3] = "Art"


def trans_text(item):
    base_path = f"C:/Users/kaifun/Desktop/ass_TIP/TextInfoExp/Part3_Text_Cluster/data_temp2/{item}/"

    filelist = os.listdir(base_path)
    # salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    f3 = open('id2class2.txt', 'a')
    for files in filelist:
        with open(base_path + files, 'r') as f:
            text = (f.read().decode('GB2312', 'ignore').encode('utf-8'))
            salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))  # 产生随机数
            f2 = open(
                f"C:/Users/kaifun/Desktop/ass_TIP/TextInfoExp/Part3_Text_Cluster/data_test/{salt}.txt",
                'w',
            )

            f2.write(text)
            f3.write(f'{salt} ' + item + '\n')
        f2.close()


def trans_res():
    data = pd.read_table('id2class.txt', header=None, delim_whitespace=True)
    data2 = pd.read_table('cluster_Result.txt', header=None)
    # print (data)
    # print (data2)
    res_dic = {}
    with open('result.txt', 'w') as f:
        for i in range(len(data2)):
            res_dic[data.iloc[i, 0]] = data2.iloc[i, 1]
            # f.write(str(data.iloc[i,0]) +'   ' + str(data2.iloc[i,1]) + '\n' )
        # print (res_dic)
        res = sorted(res_dic.items(), key=lambda e: e[1], reverse=False)
        print (res)
        print (type(res))

        with open('data_abs0.txt', 'w') as ff0:
            ff1 = open('data_abs1.txt', 'w')
            ff2 = open('data_abs2.txt', 'w')
            for (k, v) in res:
                if str(v) == '1':
                    with open(f"C:/Users/kaifun/Desktop/ass_TIP/TextInfoExp/Part3_Text_Cluster/data/{k}.txt", 'r') as fff1:
                        text = fff1.read()
                        data_temp = text.decode('utf-8')  # 转换为unicode编码形式
                        data = ''.join(re.findall(u'[\u4e00-\u9fff]+', data_temp))  # 必须为unicode类型，取出所有中文字符
                    ff1.write(data.encode('utf-8'))
                            # text_list1.append(k)
                if str(v) == '2':
                    with open(f"C:/Users/kaifun/Desktop/ass_TIP/TextInfoExp/Part3_Text_Cluster/data/{k}.txt", 'r') as fff2:
                        text = fff2.read()
                        data_temp = text.decode('utf-8')  # 转换为unicode编码形式
                        data = ''.join(re.findall(u'[\u4e00-\u9fff]+', data_temp))  # 必须为unicode类型，取出所有中文字符
                    ff2.write(data.encode('utf-8'))
                            # text_list2.append(k)
                if str(v) == '0':
                    with open(f"C:/Users/kaifun/Desktop/ass_TIP/TextInfoExp/Part3_Text_Cluster/data/{k}.txt", 'r') as fff0:
                        text = fff0.read()
                        data_temp = text.decode('utf-8')  # 转换为unicode编码形式
                        data = ''.join(re.findall(u'[\u4e00-\u9fff]+', data_temp))  # 必须为unicode类型，取出所有中文字符
                    ff0.write(data.encode('utf-8'))
                            # text_list0.append(k)
                f.write(f'{str(k)}    {str(v)}' + '\n')

        ff1.close()
        ff2.close()


def get_metrics():
    dict_lable = {'eco': 0, 'env': 1, 'sports': 2, 'other': 3}
    data = pd.read_table('id2class.txt', header=None, delim_whitespace=True)
    data2 = pd.read_table('result.txt', header=None, delim_whitespace=True)
    list_true = []
    list_pred = []
    for i in range(len(data)):
        data.iloc[i, 1] = dict_lable[data.iloc[i, 1]]
        list_true.append(data.iloc[i, 1])
        list_pred.append(data2.iloc[i, 1])

    # 文档链接 http://scikit-learn.org/stable/modules/clustering.html#clustering-performance-evaluation
    #  2.3.9.1 Adjusted Rand index （RI）
    #  2.3.9.2. Mutual Information based scores（NMI）
    #  2.3.9.4. Fowlkes-Mallows scores（FMI）
    #  章节号为文档里面的章节号
    print (metrics.adjusted_rand_score(list_true, list_pred))  # RI指数，越接近1越好
    print (metrics.adjusted_mutual_info_score(list_true, list_pred))  # NMI指数，越接近1越好
    print (metrics.fowlkes_mallows_score(list_true, list_pred))  # FMI指数，越接近1越好


if __name__ == '__main__':
    get_metrics()
    # list1 = ['agriculture','history','medical','politics','space','other']
    # for i in list1:
    #     trans_text(i)
    # get_text()
    # trans_res()
