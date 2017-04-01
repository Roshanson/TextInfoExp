# -*- coding: utf-8 -*-
'''
Created on 2014-10-26
@author: zhanghb
'''
import re
from jieba import cut
from TF_IDF import GrobalParament
def fullcut(content):
    cut_content = cut(content, cut_all=False)
    word_list_temp=list(cut_content)
    word_list=[]
    if not GrobalParament.ruler_list:
        r=r'[^/]{2,}'
        temp='/'.join(word_list_temp)
        word_list=re.findall(r,temp)
    else:
        for word in word_list_temp:
            if word not in GrobalParament.ruler_list:
                word_list.append(word)
    return word_list