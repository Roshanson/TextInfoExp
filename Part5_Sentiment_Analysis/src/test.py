# encoding:utf-8
import datetime
from multiprocessing import Process

from feature_extraction import ChiSquare
from tools import get_accuracy
from tools import Write2File


class Test:
    def __init__(self, type_, train_num, test_num, feature_num, max_iter, C, k, corpus):
        self.type = type_
        self.train_num = train_num
        self.test_num = test_num
        self.feature_num = feature_num
        self.max_iter = max_iter
        self.C = C
        self.k = k
        self.parameters = [train_num, test_num, feature_num]

        # get the f_corpus
        self.train_data, self.train_labels = corpus.get_train_corpus(train_num)
        self.test_data, self.test_labels = corpus.get_test_corpus(test_num)

        # feature extraction
        fe = ChiSquare(self.train_data, self.train_labels)
        self.best_words = fe.best_words(feature_num)

        self.single_classifiers_got = False

        self.precisions = [[0, 0],  # bayes
                           [0, 0],  # maxent
                           [0, 0]]  # svm

    def set_precisions(self, precisions):
        self.precisions = precisions

    def test_knn(self):
        from classifiers import KNNClassifier

        if type(self.k) == int:
            k = "%s" % self.k
        else:
            k = "-".join([str(i) for i in self.k])

        print("KNNClassifier")
        print("---" * 45)
        print("Train num = %s" % self.train_num)
        print("Test num = %s" % self.test_num)
        print("K = %s" % k)

        # print self.train_data
        print (self.train_labels)
        print (len(self.train_data))
        print (self.train_data[0])

        knn = KNNClassifier(self.train_data, self.train_labels, k=self.k, best_words=self.best_words)
        classify_labels = []

        print("KNNClassifiers is testing ...")

        for data in self.test_data:
            classify_labels.append(knn.classify(data))
        print("KNNClassifiers tests over.")

        filepath = "f_runout/KNN-%s-train-%d-test-%d-f-%d-k-%s-%s.xls" % \
                   (self.type,
                    self.train_num, self.test_num,
                    self.feature_num, k,
                    datetime.datetime.now().strftime(
                        "%Y-%m-%d-%H-%M-%S"))

        self.write(filepath, classify_labels)

    def test_bayes(self):
        print("BayesClassifier")
        print("---" * 45)
        print("Train num = %s" % self.train_num)
        print("Test num = %s" % self.test_num)

        from classifiers import BayesClassifier
        bayes = BayesClassifier(self.train_data, self.train_labels, self.best_words)

        classify_labels = []
        print("BayesClassifier is testing ...")
        for data in self.test_data:
            classify_labels.append(bayes.classify(data))
        print("BayesClassifier tests over.")

        filepath = "f_runout/Bayes-%s-train-%d-test-%d-f-%d-%s.xls" % \
                   (self.type,
                    self.train_num, self.test_num, self.feature_num,
                    datetime.datetime.now().strftime(
                        "%Y-%m-%d-%H-%M-%S"))

        self.write(filepath, classify_labels, 0)

    def write(self, filepath, classify_labels, i=-1):
        results = get_accuracy(self.test_labels, classify_labels, self.parameters)
        if i >= 0:
            self.precisions[i][0] = results[10][1] / 100
            self.precisions[i][1] = results[7][1] / 100

        Write2File.write_contents(filepath, results)

    def test_maxent_iteration(self):
        print("MaxEntClassifier iteration")
        print("---" * 45)
        print("Train num = %s" % self.train_num)
        print("Test num = %s" % self.test_num)
        print("maxiter = %s" % self.max_iter)

        from classifiers import MaxEntClassifier

        m = MaxEntClassifier(self.max_iter)
        iter_results = m.test(self.train_data, self.train_labels, self.best_words, self.test_data)

        filepath = "f_runout/MaxEnt-iteration-%s-train-%d-test-%d-f-%d-maxiter-%d-%s.xls" % \
                   (self.type,
                    self.train_num,
                    self.test_num,
                    self.feature_num,
                    self.max_iter,
                    datetime.datetime.now().strftime(
                        "%Y-%m-%d-%H-%M-%S"))

        results = []
        for i in range(len(iter_results)):
            try:
                results.append(get_accuracy(self.test_labels, iter_results[i], self.parameters))
            except ZeroDivisionError:
                print("ZeroDivisionError")

        Write2File.write_contents(filepath, results)

    def test_maxent(self):
        print("MaxEntClassifier")
        print("---" * 45)
        print("Train num = %s" % self.train_num)
        print("Test num = %s" % self.test_num)
        print("maxiter = %s" % self.max_iter)

        from classifiers import MaxEntClassifier

        m = MaxEntClassifier(self.max_iter)
        m.train(self.train_data, self.train_labels, self.best_words)

        print("MaxEntClassifier is testing ...")
        classify_results = []
        for data in self.test_data:
            classify_results.append(m.classify(data))
        print("MaxEntClassifier tests over.")

        filepath = "f_runout/MaxEnt-%s-train-%d-test-%d-f-%d-maxiter-%d-%s.xls" % \
                   (self.type,
                    self.train_num, self.test_num,
                    self.feature_num, self.max_iter,
                    datetime.datetime.now().strftime(
                        "%Y-%m-%d-%H-%M-%S"))

        self.write(filepath, classify_results, 1)

    def test_svm(self):
        print("SVMClassifier")
        print("---" * 45)
        print("Train num = %s" % self.train_num)
        print("Test num = %s" % self.test_num)
        print("C = %s" % self.C)

        from classifiers import SVMClassifier
        svm = SVMClassifier(self.train_data, self.train_labels, self.best_words, self.C)

        classify_labels = []
        print("SVMClassifier is testing ...")
        for data in self.test_data:
            classify_labels.append(svm.classify(data))
        print("SVMClassifier tests over.")

        filepath = "f_runout/SVM-%s-train-%d-test-%d-f-%d-C-%d-%s-lin.xls" % \
                   (self.type,
                    self.train_num, self.test_num,
                    self.feature_num, self.C,
                    datetime.datetime.now().strftime(
                        "%Y-%m-%d-%H-%M-%S"))

        self.write(filepath, classify_labels, 2)


def test_movie():
    from corpus import MovieCorpus as Corpus

    type_ = "movie"
    train_num = 500
    test_num = 200
    feature_num = 4000
    max_iter = 10
    C = 10
    k = 13

    corpus = Corpus()

    test = Test(type_, train_num, test_num, feature_num, max_iter, C, k, corpus)

    # test.test_knn()
    test.test_svm()
    # test.single_multiprocess()
    # test.multiple_multiprocess()


def test_movie2():
    from corpus import Movie2Corpus

    type_ = "movie2"
    train_num = 700
    test_num = 300
    feature_num = 5000
    max_iter = 100
    C = 80
    # k = 1
    k = [1, 3, 5, 7, 9, 11, 13]
    k = [1, 3, 5, 7, 9]

    corpus = Movie2Corpus()

    test = Test(type_, train_num, test_num, feature_num, max_iter, C, k, corpus)

    # test.test_knn()
    # test.test_bayes()
    # test.test_maxent()
    # test.test_maxent_iteration()
    test.test_svm()


def test_waimai():
    from corpus import WaimaiCorpus

    type_ = "waimai"
    train_num = 3000
    test_num = 1000
    feature_num = 5000
    max_iter = 500
    C = 150
    k = 13
    k = [1, 3, 5, 7, 9, 11, 13]
    corpus = WaimaiCorpus()

    test = Test(type_, train_num, test_num, feature_num, max_iter, C, k, corpus)

    # test.single_multiprocess()
    # test.multiple_multiprocess()

    # test.test_knn()
    # test.test_bayes()
    # test.test_maxent()
    # test.test_maxent_iteration()
    test.test_svm()
    # test.test_multiple_classifiers()
    # test.test_multiple_classifiers2()
    # test.test_multiple_classifiers3()
    # test.test_multiple_classifiers4()


def test_waimai2():
    from corpus import Waimai2Corpus

    type_ = "waimai2"
    train_num = 3000
    test_num = 1000
    feature_num = 5000
    max_iter = 100
    C = 50
    k = 1
    corpus = Waimai2Corpus()

    test = Test(type_, train_num, test_num, feature_num, max_iter, C, k, corpus)
    test.test_svm()
    # test.single_multiprocess()
    # test.multiple_multiprocess()


def test_hotel():
    from corpus import HotelCorpus

    type_ = "hotel"
    train_num = 2200
    test_num = 800
    feature_num = 5000
    max_iter = 500
    C = 150
    # k = 13
    k = [1, 3, 5, 7, 9, 11, 13]
    corpus = HotelCorpus()

    test = Test(type_, train_num, test_num, feature_num, max_iter, C, k, corpus)

    # test.test_knn()

    # test.single_multiprocess()
    # test.multiple_multiprocess()

    # test.test_bayes()
    # test.test_maxent()
    # test.test_maxent_iteration()
    test.test_svm()
    # test.test_multiple_classifiers()
    # test.test_multiple_classifiers2()
    # test.test_multiple_classifiers3()
    # test.test_multiple_classifiers4()


def test_dict():
    """
    test the classifier based on Sentiment Dict
    """
    print("DictClassifier")
    print("---" * 45)

    from classifiers import DictClassifier

    ds = DictClassifier()

    # 对一个单句进行情感分析
    a_sentence = "剁椒鸡蛋好咸,土豆丝很好吃"
    result = ds.analyse_sentence(a_sentence)
    print(result)

    # 对一个文件内语料进行情感分析
    # corpus_filepath = "D:/My Data/NLP/SA/waimai/positive_corpus_v1.txt"
    # runout_filepath_ = "f_runout/f_dict-positive_test.txt"
    # pos_results = ds.analysis_file(corpus_filepath, runout_filepath_, start=3000, end=4000-1)
    #
    # corpus_filepath = "D:/My Data/NLP/SA/waimai/negative_corpus_v1.txt"
    # runout_filepath_ = "f_runout/f_dict-negative_test.txt"
    # neg_results = ds.analysis_file(corpus_filepath, runout_filepath_, start=3000, end=4000-1)
    #
    # origin_labels = [1] * 1000 + [0] * 1000
    # classify_labels = pos_results + neg_results
    #
    # print(len(classify_labels))
    #
    # filepath = "f_runout/Dict-waimai-%s.xls" % (
    #     datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    # results = get_accuracy(origin_labels, classify_labels, [1000, 1000, 0])
    #
    # Write2File.write_contents(filepath, results)


if __name__ == "__main__":
    pass
    test_movie()
    test_movie2()
    test_waimai()
    test_waimai2()
    test_hotel()
    # test_dict()
