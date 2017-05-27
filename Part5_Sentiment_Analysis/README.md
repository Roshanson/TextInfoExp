
### 情感分析可理解问文本分类问题，本数据集采用2分类，即只有正向和负向评价

 核心代码 fork from https://github.com/chaoming0625/SentimentPolarityAnalysis.git
  
 调整代码在当前环境可直接运行，直接晕车test.py即可
  
 f_corpus中有5各数据集，3个中文2个英文。
 
 分类器有 KNN SVM bayes 最大熵 基于字典 5种，但除了使用sklearn的SVM可以调试通过外，
 
 其它几种自己实现的目前还有点问题。
 