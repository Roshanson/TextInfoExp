# -*- coding: utf-8 -*-

# 这个函数用于预处理文件处理过程中采用unicode编码
import os
from str_replace import str_replace
from TF_IDF.StrToUni import StrToUni
import GrobalParament
from full_word_cut import fullcut
from half_word_cut import halfcut
from UniToStr import UniToStr

#  将所有文本分词，结果汇总到pro_res.txt
def prepro_file(fl_in_url, re_out_url, *wd_be_del):
    in_url = fl_in_url.replace('\\', '/')
    out_url = re_out_url.replace('\\', '/')
    try:
        try:
            fl_in = os.listdir(in_url)
        except WindowsError:
            print "您输入的预处理文档目录有误"
        try:
            # out_file=out_url+'/'+GrobalParament.PreprocessResultName
            re_out = open(out_url, 'w')
        except WindowsError:
            print "您输入的结果文档输出目录有误"
    except NameError:
        pass
    else:
        i = 0
        for file in fl_in:
            i += 1
            print i

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
