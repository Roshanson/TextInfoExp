## 使用特征：
  
   实体1、2前后窗口大小为3的词语及词性（不区分顺序，使用one hot编码，词典大小15000）

## 评测：
  
   只评测在test_relation.txt中的关系对的对错情况。

## 运行步骤：

 1、使用feature_extract.py中的align函数对齐得到训练集和测试集

 2、使用feature_extract.py中的generateDic2函数生成字典，后续特征提取使用。
 
 3、使用feature_extract.py中的feature_extract2函数提取训练集、测试集的特征。
 
 4、使用libsvm windows目录下的svm-scale.exe工具对训练集、测试集特征文件进行归一化，并指定最小值是0。命令是
      
      svm-scale -l 0 feature_path > feature_scale_path
   其中feature_path是特征文件的路径，feature_scale_path是特征文件归一化以后的保存路径,-l 0是指定最小值是0
  
 5、使用libsvm windows目录下的svm-train.exe工具进行训练，命令如下：
 
    svm-train -b 1 feature_scale_path model_path 
 
 其中feature_scale_path是训练集特征文件的路径，model_path是模型文件的路径，-b 1指定预测时可以输出概率。还可以指定其他参数，详见libsvm的使用。
 
 6、使用使用libsvm windows目录下的svm-predict.exe工具进行预测，命令如下：
    
    svm-predict -b 1 test_feature_scale_path model_path output_path
 
 其中test_feature_scale_path是测试集特征归一化文件路径，model_path是训练得到的模型文件路径，output_path是预测输出结果。
  
 7、使用feature_extract.py中的handle_libsvm_result函数整理libsvm预测结果。

 8、使用feature_extract.py中的evaluation进行结果评测。