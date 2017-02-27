#####文件说明
     data文件夹存放源数据
     data_afterprocess文件夹存放各种中间结果


###1  对于原始数据(data/computer中的xml文件)进行预处理
       通过运行abstracts.py,将源数据进行清洗，得到每个数据的标题和摘要（生成title_and_abstracts文件）。
       此外，也取出每个文件的关键词，保存在keyword文件夹，后期用于和TF-IFDF的结果进行对比。

###2  对abstracts.py得到的数据（title_and_abstracts）文件进行TF_IDF计算，提取得分排名前三的关键词
      运行TF_IDF.py，首先对步骤一得到的数据进行分词（采用jieba分词工具），文件汇总得到pro_res.txt。
      然后使用TF_IDF-Compute.py进行计算，取前三排名的词。

###3  最终得到的结果： results.txt