# encoding=utf-8
import ctypes

so = ctypes.cdll.LoadLibrary
cilin_lib = so("./libcilin.so")

cilin_lib.read_cilin('../data/dataset.txt')
cilin_lib.similarity.restype = ctypes.c_float

p_word = "人民"
# print lib.similarity(p_word,"国民")
words = ["国民", "群众", "党群", "良民", "同志", "成年人", "市民", "亲属", "志愿者", "先锋"]

for w in words:
    print (w, cilin_lib.similarity(p_word, w))
