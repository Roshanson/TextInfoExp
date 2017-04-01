# -*- coding: utf-8 -*-
'''
Created on 2014-10-26
@author: zhanghb
'''
from jieba.analyse import extract_tags
from TF_IDF import GrobalParament
import re
def halfcut(content):
    word_list=[]
    k=GrobalParament.n
    while True:
        cut_content = extract_tags(content, k)
        word_list_temp=cut_content
        if not GrobalParament.ruler_list:
            r=r'[^/\d]{2,}'
            temp='/'.join(word_list_temp)
            word_list=re.findall(r,temp)
        else:
            for word in word_list_temp:
                if word not in GrobalParament.ruler_list:
                    word_list.append(word)
            #print len(word_list)
        if (len(word_list)>=GrobalParament.n):
            break
        else:
            word_list=[]
            k+=1
    return word_list