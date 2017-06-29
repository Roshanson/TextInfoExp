# -*- coding: utf-8 -*-

from __future__ import division
import re
import jieba
import math
# 这个函数用于预处理文件处理过程中采用unicode编码
import os
import GrobalParament


def fullcut(content):
    cut_content = jieba.cut(content, cut_all=False)
    word_list_temp = list(cut_content)
    word_list = []
    if not GrobalParament.ruler_list:
        r = r'[^/]{2,}'
        temp = '/'.join(word_list_temp)
        word_list = re.findall(r, temp)
    else:
        for word in word_list_temp:
            if word not in GrobalParament.ruler_list:
                word_list.append(word)
    return word_list


def halfcut(content):
    word_list = []
    k = GrobalParament.n
    while True:
        cut_content = jieba.analyse.extract_tags(content, k)
        word_list_temp = cut_content
        if not GrobalParament.ruler_list:
            r = r'[^/\d]{2,}'
            temp = '/'.join(word_list_temp)
            word_list = re.findall(r, temp)
        else:
            for word in word_list_temp:
                if word not in GrobalParament.ruler_list:
                    word_list.append(word)
                    # print len(word_list)
        if (len(word_list) >= GrobalParament.n):
            break
        else:
            word_list = []
            k += 1
    return word_list


def UniToStr_try(str, type_1):
    try:
        str.encode(type_1)
    except LookupError:
        return False
    else:
        return True


def UniToStr(str, *out_Format):
    if not out_Format:
        return str.encode('utf-8')
    else:
        for type_2 in out_Format:
            if UniToStr_try(str, type_2):
                return str.encode(type_2)
            else:
                if type_2 == out_Format[-1]:
                    print ("输入的目标编码格式不正确")


# 多字符串替换函数，对于str_source中的某些字符（从*words传入）用char代替
def str_replace(str_source, char, *words):
    str_temp = str_source
    for word in words:
        str_temp = str_temp.replace(word, char)
    return str_temp


def StrToUni_try(str, type_1):
    try:
        str.decode(type_1)
    except UnicodeDecodeError:
        return False
    else:
        return True


def StrToUni(str, *type_list):
    if not type_list:
        if StrToUni_try(str, 'utf-8'):
            return str.decode('utf-8')
        else:
            print ("输入的源文件的编码格式不是utf-8")
    else:
        for type_2 in type_list:
            if StrToUni_try(str, type_2):
                return str.decode(type_2)
            else:
                if type_2 == type_list[-1]:
                    print ("输入的源文件的编码格式不在您提供的格式列表中")


# 将所有文本分词，结果汇总到pro_res.txt
def prepro_file(fl_in_url, re_out_url, *wd_be_del):
    in_url = fl_in_url.replace('\\', '/')
    out_url = re_out_url.replace('\\', '/')
    fl_in = os.listdir(in_url)
    # out_file=out_url+'/'+GrobalParament.PreprocessResultName
    re_out = open(out_url, 'w')
    i = 0
    for file in fl_in:
        i += 1
        print (i)

        afile_url = fl_in_url + '/' + file
        if os.path.isfile(afile_url):
            afile = open(afile_url, "r")
            content_temp = "".join(afile.readlines())
            if not wd_be_del:
                # content=str_replace("aaiowefhaw","","\t","\n")
                content = str_replace(content_temp, "", "\t", "\n", " ")  # 删除某些特殊字符如\t,\n等以保证是一行的连续的
            else:
                content = str_replace(content_temp, '', *wd_be_del)
            con_unicode = StrToUni(content, *(GrobalParament.InputFormatList))
            if GrobalParament.pattern == "full":
                cut_result = fullcut(con_unicode)
            else:
                cut_result = halfcut(con_unicode)
            s_fl_Name = UniToStr(file, *(GrobalParament.OutputFormatList))
            re_out.write(s_fl_Name + '\t')
            key_word_out = []
            for key_word in cut_result:
                s_key_word = UniToStr(key_word, *(GrobalParament.OutputFormatList))
                key_word_out.append(s_key_word)
            # re_out.write(s_key_word+',')
            out_str = ','.join(key_word_out)
            re_out.write(out_str)
            re_out.write('\n')


def TF_IDF_Compute(file_import_url_temp):
    file_import_url = file_import_url_temp.replace('\\', '/')
    data_source = open(file_import_url, 'r')
    data = data_source.readline()
    word_in_afile_stat = {}
    word_in_allfiles_stat = {}
    files_num = 0
    while (data != ""):  # 对文件pro_res.txt进行处理
        data_temp_1 = []
        data_temp_2 = []
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

    newpath2 = GrobalParament.newpath2
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
            result_temp = []

            result_temp = sorted(TF_IDF_result.iteritems(), key=lambda x: x[1], reverse=True)
            f1 = open(newpath2 + filename, "r")

            line = f1.readline()
            TF_IDF_last_result.append(filename)
            TF_IDF_last_result.extend(result_temp[0:3])

            TF_IDF_last_result.append(line)
            TF_IDF_last_result.append('\n')

    f = open("results.txt", "a+")

    for s in TF_IDF_last_result:
        # print s
        for i in s:
            f.write(str(i))
        f.write("\n")
    f.close()
