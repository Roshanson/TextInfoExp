#coding:utf-8

#使用libsvm进行模型训练
__author__ = 'hbj'


from svmutil import *
import os
import os.path
import time
def trainwithlibsvm(trainfilepath,modelsavefilepath):

    y,X = svm_read_problem(trainfilepath)
    model = svm_train(y,X,"-t 0 -b 1")
    svm_save_model(modelsavefilepath,model)

if __name__ == "__main__":


    whole = "train_whole_nostudent_withnorelationship_libsvm_feature3_sample8000.txt"
    fbyp = "train_filterbypattern_nostudent_withnorelationship_libsvm_feature3_sample8000.txt"


    # filepath = "d:\\RE\\feature\\split\\libsvm\\"+filename
    # modelname = "_".join(filename.split("_")[0:-1])+".model"

    start1 = time.clock()
    wholemodelfilepath = "train_whole_feature3_sample8000.model"
    trainwithlibsvm(whole,wholemodelfilepath)
    end1 = time.clock()

    print 'whole takes %f s' %(end1-start1)

    #start2 = time.clock()
    #fbypmodelfilepath = "train_filterbypattern_feature2.model"
    #trainwithlibsvm(fbyp,fbypmodelfilepath)
    #end2 = time.clock()
    #print 'fbp takes %f s' %(end2-start2)

    # trainwithlibsvm("d:\\RE\\feature\\split\\libsvm\\train_6_1v1_libsvm.txt","d:\\RE\\feature\\split\\model\\train_6_1v1.model")
    # trainwithlibsvm("d:\\RE\\feature\\split\\libsvm\\train_6_1v1_fword_libsvm.txt","d:\\RE\\feature\\split\\model\\train_6_1v1_fword.model")

    #对D:\RE\feature\split\libsvm下所有的文件进行训练

    # for label in (1,2):
    #     label = (str)(label)
    #     filename = "train_"+label+"_1v1_filterbypattern_libsvm.txt"
    #     filepath = "d:\\RE\\feature\\split\\libsvm\\"+filename
    #     modelname = "_".join(filename.split("_")[0:-1])+".model"
    #     modelfilepath = os.path.join("d:\\RE\\feature\\split\\model",modelname)
    #     trainwithlibsvm(filepath,modelfilepath)
    #
    # for label in (1,2):
    #     label = (str)(label)
    #     filename = "train_"+label+"_1v1_fword_libsvm.txt"
    #     filepath = "d:\\RE\\feature\\split\\libsvm\\"+filename
    #     modelname = "_".join(filename.split("_")[0:-1])+".model"
    #     modelfilepath = os.path.join("d:\\RE\\feature\\split\\model",modelname)
    #     trainwithlibsvm(filepath,modelfilepath)
    #
    # for label in (1,2):
    #     label = (str)(label)
    #     filename = "train_whole_nostudent_"+label+"_1v1_libsvm.txt"
    #     filepath = "d:\\RE\\feature\\split\\libsvm\\"+filename
    #     modelname = "_".join(filename.split("_")[0:-1])+".model"
    #     modelfilepath = os.path.join("d:\\RE\\feature\\split\\model",modelname)
    #     trainwithlibsvm(filepath,modelfilepath)
    # #






            # print filepath
            # print modelfilepath
        #trainwithlibsvm(filepath,modelfilepath)
    # for dirpath, dirnames, filenames in os.walk("home/hbj/DS/feature/libsvm"):
    #     for filename in filenames:
    #         filepath = os.path.join("home/hbj/DS/feature/libsvm",filename)
    #         modelname = "_".join(filename.split("_")[0:-1])+".model"
    #         modelfilepath = os.path.join("home/hbj/DS/feature/model",modelname)
    #         print filepath
    #         print modelfilepath
    #         trainwithlibsvm(filepath,modelfilepath)