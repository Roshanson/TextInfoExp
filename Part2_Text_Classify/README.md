# 文本分类

## 
    预处理，分类步骤可参见main函数下面的各个函数。
    id2class.py为data_test文件夹中各个文件的类别号。

##   
  基于自定义特征的分类器可见 classifier.py   使用sklearn比较简易的接口，包括boost、bagging、stack三种集成学习的方式
   
## 
   使用神经网络可自动提取特征，当前一般使用cnn，即cnntext。
   
   cnn做文本分类源码参考自 https://github.com/dennybritz/cnn-text-classification-tf.git
  
   解决原项目环境不适配tensorflow1.0以上版本的问题。 