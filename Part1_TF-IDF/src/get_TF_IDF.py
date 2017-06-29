# -*- coding: utf-8 -*-

from __future__ import division
import GrobalParament
from utils import prepro_file
import math


def TF_IDF_Compute(file_import_url_temp):
    file_import_url = file_import_url_temp.replace('\\', '/')
    data_source = open(file_import_url, 'r')
    data = data_source.readline()
    word_in_afile_stat = {}
    word_in_allfiles_stat = {}
    files_num = 0
    while (data != ""):  # 对文件pro_res.txt进行处理
        data_temp_1 = data.strip("\n").split("\t")  # file name and key words of a file
        data_temp_2 = data_temp_1[1].split(",")  # key words of a file
        file_name = data_temp_1[0]
        data_temp_len = len(data_temp_2)
        files_num += 1
        data_dict = {}
        data_dict.clear()
        for word in data_temp_2:
            if word not in word_in_allfiles_stat:
                word_in_allfiles_stat[word] = 1
                data_dict[word] = 1
            else:
                if word not in data_dict:  # 如果这个单词在这个文件中之前没有出现过
                    word_in_allfiles_stat[word] += 1
                    data_dict[word] = 1

            if not word_in_afile_stat.has_key(file_name):
                word_in_afile_stat[file_name] = {}
            if not word_in_afile_stat[file_name].has_key(word):
                word_in_afile_stat[file_name][word] = []
                word_in_afile_stat[file_name][word].append(data_temp_2.count(word))
                word_in_afile_stat[file_name][word].append(data_temp_len)
        data = data_source.readline()
    data_source.close()

    # filelist = os.listdir(newpath2)  # 取得当前路径下的所有文件
    TF_IDF_last_result = []
    if (word_in_afile_stat) and (word_in_allfiles_stat) and (files_num != 0):
        for filename in word_in_afile_stat.keys():
            TF_IDF_result = {}
            TF_IDF_result.clear()
            for word in word_in_afile_stat[filename].keys():
                word_n = word_in_afile_stat[filename][word][0]
                word_sum = word_in_afile_stat[filename][word][1]
                with_word_sum = word_in_allfiles_stat[word]
                TF_IDF_result[word] = ((word_n / word_sum)) * (math.log10(files_num / with_word_sum))

            result_temp = sorted(TF_IDF_result.iteritems(), key=lambda x: x[1], reverse=True)
            # f1 = open(newpath2 + filename, "r")

            # line = f1.readline()
            TF_IDF_last_result.append(filename)
            TF_IDF_last_result.extend(result_temp[0:10])

            # TF_IDF_last_result.append(line)
            TF_IDF_last_result.append('\n')

    f = open("results.txt", "a+")

    for s in TF_IDF_last_result:
        # print s
        for i in s:
            f.write(str(i))
        f.write("\n")
    f.close()


if __name__ == '__main__':
    PreResUrl = "pro_res.txt"
    prepro_file(GrobalParament.path1, PreResUrl)  # 将所有文本分词，结果汇总到pro_res.txt
    TF_IDF_Compute(PreResUrl)  # 获得TF_IDF结果
