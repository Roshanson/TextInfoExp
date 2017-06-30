# encoding:utf-8

import os
import pandas as pd
import sys
import jieba
import re
import string
import random
from collections import Counter
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer

reload(sys)
sys.setdefaultencoding("utf-8")

# base_path = "C:/Users/kaifun/Desktop/ass_TIP/TextInfoExp/Part2_Text_Classify/data_valid/"
base_path = '/home/kaifun/PycharmProjects/TextInfoExp/Part2_Text_Classify/'


def data_preprocess():
    cls = ['Art', 'Computer', 'Sports']
    for item in cls:
        get_text(item)


# 将各类文本汇总成一个txt
def get_text(item):
    filelist = os.listdir(base_path + 'data_train/' + item)
    data_dict = {}
    for files in filelist:
        # print (files)
        f = open(base_path + 'data_train/' + item + '/' + files, 'r')
        text = f.read().replace('\n', '')
        data_temp = text.decode('utf-8')  # 转换为unicode编码形式
        data = ''.join(re.findall(u'[\u4e00-\u9fff]+', data_temp))  # 必须为unicode类型，取出所有中文字符
        data2 = jieba.cut(data.encode('utf-8'))  # 分词
        data3 = " ".join(data2)  # 结果转换为字符串（列表转换为字符串）
        data_dict[data3] = item

    f2 = open('%s.txt' % item, 'a+')
    for (k, v) in data_dict.items():
        f2.write(v + ',' + k + ' ' + '\n')
    f2.close()


# 获取数据和标记
def load_data():
    data = pd.read_table('Art.txt', header=None, sep=',')
    data2 = pd.read_table('Computer.txt', header=None, sep=',')
    data3 = pd.read_table('Sports.txt', header=None, sep=',')
    # print (data,data2,data3)

    posting_list = []
    class_list = [] # 方便计算转换为1,2,3

    for i in range(len(data)):
        posting_list.append((data.iloc[i, 1]))
        class_list.append(str(1))
    for i in range(len(data2)):
        posting_list.append((data2.iloc[i, 1]))
        class_list.append(str(2))
    for i in range(len(data3)):
        posting_list.append((data3.iloc[i, 1]))
        class_list.append(str(3))

    # print (posting_list)
    return posting_list, class_list


def jieba_tokenizer(x): return jieba.cut(x, cut_all=True)


# 将文件名进行脱敏化处理
def trans_text():
    # salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    f3 = open('id2class2.txt', 'a')
    filelist = os.listdir(base_path)
    for files in filelist:
        # print (files)
        f = open(base_path + files, 'r')
        text = (f.read().decode('GB2312', 'ignore').encode('utf-8'))
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))  # 产生随机数
        f2 = open("C:/Users/kaifun/Desktop/ass_TIP/TextInfoExp/Part2_Text_Classify/test3/" + salt + '.txt', 'w')
        f2.write(text)
        f3.write(salt + ' ' + 'e' + '\n')
        f.close()
        f2.close()


def get_classify():
    X_train, Y_train = load_data()

    # 定义分类器
    classifier = Pipeline([
        ('counter', CountVectorizer(tokenizer=jieba_tokenizer)),  # 标记和计数，提取特征用 向量化
        ('tfidf', TfidfTransformer()),                            # IF-IDF 权重
        ('clf', OneVsRestClassifier(LinearSVC())),                # 1-rest 多分类(多标签)
    ])
    mlb = MultiLabelBinarizer()
    Y_train = mlb.fit_transform(Y_train)                          # 分类号数值化

    classifier.fit(X_train, Y_train)

    # X_test = ["数据分析"]
    # 把所有的测试文本存到一个list中
    test_list = []
    test_name = []
    filelist2 = os.listdir(base_path + "data_test/")
    for files in filelist2:
        # print (files)
        test_name.append(files)
        f = open(base_path + "data_test/" + files, 'r')
        test_list.append(f.read())

    prediction = classifier.predict(test_list)
    result = mlb.inverse_transform(prediction)

    f = open('result2.txt', 'w')
    for i in range(len(test_name)):
        f.write(str(test_name[i]) + '   ' + str(result[i]) + '\n')

    print (result, len(result))
    num_dict = Counter(result)
    print (len(num_dict))
    print ((num_dict[('1',)] + num_dict[('2',)] + num_dict[('3',)]) / float(len(result)))  # 整数除整数为0，应把其中一个改为浮点数。


if __name__ == '__main__':
    # data_preprocess()
    get_classify()
