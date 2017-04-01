# -*- coding: utf-8 -*-
'''
Created on 2014年11月2日

@author: zhanghb
'''
def UniToStr_try(str,type_1):
    try:
        str.encode(type_1)
    except LookupError:
        return False
    else:
        return True
def UniToStr(str,*out_Format):
    if not out_Format:
        return str.encode('utf-8')
    else:
        for type_2 in out_Format:
            if UniToStr_try(str,type_2):
                return str.encode(type_2)
            else:
                if type_2==out_Format[-1]:
                    print "输入的目标编码格式不正确"