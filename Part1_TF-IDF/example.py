# encoding:utf-8

import sys
import jieba
import string
import re
from collections import Counter

reload(sys)
sys.setdefaultencoding('utf-8')


def com_tf():
    f = open('data/7s.txt')
    data = f.read()

    data_temp = data.decode('utf-8')                            # 转换为unicode编码形式
    data = ''.join(re.findall(u'[\u4e00-\u9fff]+', data_temp))  # 必须为unicode类型。取出所有中文字符

    data2 = jieba.cut(data)  # 分词
    data3 = " ".join(data2)  # 结果转换为字符串

    open('data/7temp.txt', 'w').write(data3)   # 分词结果写入7temp.txt

    wlist = data3.split()        # 将分词结果切割为列表
    num_list = Counter(wlist)    # 统计词频
    # print num_list
    # 统计结果写入result.txt
    for (k, v) in num_list.items():
        open('data/result.txt', 'a+').write(str(k) + ' ' + str(v) + '\n')

if __name__ == '__main__':
    com_tf()
