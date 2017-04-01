# -*- coding: utf-8 -*-


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
            print "输入的源文件的编码格式不是utf-8"
    else:
        for type_2 in type_list:
            if StrToUni_try(str, type_2):
                return str.decode(type_2)
            else:
                if type_2 == type_list[-1]:
                    print "输入的源文件的编码格式不在您提供的格式列表中"
