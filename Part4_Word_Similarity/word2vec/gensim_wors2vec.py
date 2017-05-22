# encoding=utf-8

from gensim.models import word2vec
import gensim
import jieba

# 分词
data = jieba.cut(open('corpus.txt').read())
data = " ".join(data)

# 加载语料
open('corpus2.txt','w').write(data.encode('utf-8'))
sentences = word2vec.Text8Corpus("corpus2.txt")

# 也可以直接从文件读取字符串传入
model = word2vec.Word2Vec(sentences, size=100)  # 训练skip-gram模型

# 保存模型，以便重用
model.save("corpus.model")

# 对应的加载方式
# model = word2vec.Word2Vec.load("corpus.model")

# 以一种C语言可以解析的形式存储词向量,也可以保存为txt
model.wv.save_word2vec_format("corpus.model.bin")  # 删除binary=True

# 对应的加载方式
model = gensim.models.KeyedVectors.load_word2vec_format("corpus.model.bin")  # 删除binary=True
print (model[u'经济'])
