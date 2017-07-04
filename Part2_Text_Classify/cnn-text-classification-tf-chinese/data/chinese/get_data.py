# encoding:utf-8

import jieba
import re

data = open('neg.txt', 'r')
# data3 = data.read()
data2 = data.readlines()
print len(data2)
fw = open('neg2.txt', 'a')
for line in data2:
  data = ''.join(re.findall(u'[\u4e00-\u9fff]+', line.decode('utf-8', 'ignore')))
  str = jieba.cut(data)
  data3 = " ".join(str).encode('utf-8')
  fw.write(data3 + '\n')
