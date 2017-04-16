# encoding:utf-8
import jieba
import logging
import sys
import codecs
import traceback
import pandas as pd
import numpy as np
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from collections import Counter
from sklearn import metrics
import matplotlib.pyplot as plt


class TextCluster(object):
    # 初始化函数,重写父类函数
    def __init__(self):
        pass

    def seg_words(self, sentence):
        seg_list = jieba.cut(sentence)  # 默认是精确模式
        return " ".join(seg_list)       # 分词，然后将结果列表形式转换为字符串

    # 加载用户词典
    def load_userdictfile(self, dict_file):
        jieba.load_userdict(dict_file)

    def load_processfile(self, process_file):
        corpus_list = []
        try:
            fp = open(process_file, "r")
            for line in fp:
                conline = line.strip()
                corpus_list.append(conline)
            return True, corpus_list
        except:
            logging.error(traceback.format_exc())
            return False, "get process file fail"

    def output_file(self, out_file, item):

        try:
            fw = open(out_file, "a")
            fw.write('%s' % (item.encode("utf-8")))
            fw.close()
        except:
            logging.error(traceback.format_exc())
            return False, "out file fail"

    # 释放内存资源
    def __del__(self):
        pass

    def process(self, process_file, tf_ResFileName, tfidf_ResFileName, num_clusters, cluster_ResFileName):
        try:
            sen_seg_list = []
            flag, lines = self.load_processfile(process_file)
            if flag == False:
                logging.error("load error")
                return False, "load error"
            for line in lines:
                sen_seg_list.append(self.seg_words(line))
            # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
            tf_vectorizer = CountVectorizer()

            # fit_transform是将文本转为词频矩阵
            tf_matrix = tf_vectorizer.fit_transform(sen_seg_list)
            tf_weight = tf_matrix.toarray()
            # print tf_weight

            # 该类会统计每个词语的tf-idf权值
            tfidf_transformer = TfidfTransformer()

            # fit_transform是计算tf-idf
            tfidf_matrix = tfidf_transformer.fit_transform(tf_matrix)

            # 获取词袋模型中的所有词语
            word_list = tf_vectorizer.get_feature_names()

            # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
            tfidf_weight = tfidf_matrix.toarray()

            # 打印特征向量文本内容
            # print 'Features length: ' + str(len(word_list))
            tf_Res = codecs.open(tf_ResFileName, 'w', 'utf-8')
            word_list_len = len(word_list)
            for num in range(word_list_len):
                if num == word_list_len - 1:
                    tf_Res.write(word_list[num])
                else:
                    tf_Res.write(word_list[num] + '\t')
            tf_Res.write('\r\n')

            # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
            for i in range(len(tf_weight)):
                # print u"-------这里输出第", i, u"类文本的词语tf-idf权重------"
                for j in range(word_list_len):
                    if j == word_list_len - 1:
                        tf_Res.write(str(tf_weight[i][j]))
                    else:
                        tf_Res.write(str(tf_weight[i][j]) + '\t')
                tf_Res.write('\r\n')
            tf_Res.close()

            # 输出tfidf矩阵
            tfidf_Res = codecs.open(tfidf_ResFileName, 'w', 'utf-8')

            for num in range(word_list_len):
                if num == word_list_len - 1:
                    tfidf_Res.write(word_list[num])
                else:
                    tfidf_Res.write(word_list[num] + '\t')
            tfidf_Res.write('\r\n')

            # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
            for i in range(len(tfidf_weight)):
                for j in range(len(word_list)):
                    if j == word_list_len - 1:
                        tfidf_Res.write(str(tfidf_weight[i][j]))
                    else:
                        tfidf_Res.write(str(tfidf_weight[i][j]) + '\t')
                tfidf_Res.write('\r\n')
            tfidf_Res.close()
            # 聚类分析
            km = KMeans(n_clusters=num_clusters)
            km.fit(tfidf_matrix)
            print (metrics.silhouette_score(tfidf_matrix, km.labels_, metric='euclidean'))
            print (Counter(km.labels_))  # 打印每个类多少人
            # 中心点
            # print(km.cluster_centers_)
            # 每个样本所属的簇
            clusterRes = codecs.open(cluster_ResFileName, 'w', 'utf-8')

            # data_class = pd.read_table('id2class.txt',header=None)
            count = 1
            while count <= len(km.labels_):
                clusterRes.write(str(count) + '\t' + str(km.labels_[count - 1]))
                clusterRes.write('\r\n')
                count = count + 1
            clusterRes.close()
            # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数  958.137281791
            # print(km.inertia_)
        except:
            logging.error(traceback.format_exc())
            return False, "process fail"


# 类似于主函数
if __name__ == "__main__":
    # 获取TextProcess对象
    tc = TextCluster()
    tc.process("../data.txt", "tf_Result.txt", "tfidf_Result.txt", 3, "cluster_Result.txt")
