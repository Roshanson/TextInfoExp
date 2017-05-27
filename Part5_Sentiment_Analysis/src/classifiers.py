# encoding:utf-8
import re
from collections import defaultdict

import jieba
import numpy as np
from jieba import posseg


# ################################################
# classifier based on sentiment f_dict
# ################################################
class DictClassifier:
    def __init__(self):
        self.__root_filepath = "f_dict/"

        jieba.load_userdict("f_dict/user.dict")  # 准备分词词典

        # 准备情感词典词典
        self.__phrase_dict = self.__get_phrase_dict()
        self.__positive_dict = self.__get_dict(self.__root_filepath + "positive_dict.txt")
        self.__negative_dict = self.__get_dict(self.__root_filepath + "negative_dict.txt")
        self.__conjunction_dict = self.__get_dict(self.__root_filepath + "conjunction_dict.txt")
        self.__punctuation_dict = self.__get_dict(self.__root_filepath + "punctuation_dict.txt")
        self.__adverb_dict = self.__get_dict(self.__root_filepath + "adverb_dict.txt")
        self.__denial_dict = self.__get_dict(self.__root_filepath + "denial_dict.txt")

    def classify(self, sentence):
        return self.analyse_sentence(sentence)

    def analysis_file(self, filepath_in, filepath_out, encoding="utf-8", print_show=False, start=0, end=-1):
        open(filepath_out, "w")
        results = []

        with open(filepath_in, "r") as f:
            line_number = 0
            for line in f:
                # 控制分析的语料的开始位置（行数）
                line_number += 1
                if line_number < start:
                    continue

                results.append(self.analyse_sentence(line.strip(), filepath_out, print_show))

                # 控制分析的语料的结束位置（行数）
                if 0 < end <= line_number:
                    break

        return results

    def analyse_sentence(self, sentence, runout_filepath=None, print_show=False):
        # 情感分析整体数据结构
        comment_analysis = {"score": 0}

        # 将评论分句
        the_clauses = self.__divide_sentence_into_clauses(sentence + "%")

        # 对每分句进行情感分析
        for i in range(len(the_clauses)):
            # 情感分析子句的数据结构
            sub_clause = self.__analyse_clause(the_clauses[i].replace("。", "."), runout_filepath, print_show)

            # 将子句分析的数据结果添加到整体数据结构中
            comment_analysis["su-clause" + str(i)] = sub_clause
            comment_analysis['score'] += sub_clause['score']

        if runout_filepath is not None:
            # 将整句写进运行输出文件，以便复查
            self.__write_runout_file(runout_filepath, "\n" + sentence + '\n')
            # 将每个评论的每个分句的分析结果写进运行输出文件，以便复查
            self.__output_analysis(comment_analysis, runout_filepath)
            # 将每个评论的的整体分析结果写进运行输出文件，以便复查
            self.__write_runout_file(runout_filepath, str(comment_analysis) + "\n\n\n\n")
        if print_show:
            print("\n" + sentence)
            self.__output_analysis(comment_analysis)
            print(comment_analysis)

        if comment_analysis["score"] > 0:
            return 1
        else:
            return 0

    def __analyse_clause(self, the_clause, runout_filepath, print_show):
        sub_clause = {"score": 0, "positive": [], "negative": [], "conjunction": [], "punctuation": [], "pattern": []}
        seg_result = posseg.lcut(the_clause)

        # 将分句及分词结果写进运行输出文件，以便复查
        if runout_filepath is not None:
            self.__write_runout_file(runout_filepath, the_clause + '\n')
            self.__write_runout_file(runout_filepath, str(seg_result) + '\n')
        if print_show:
            print(the_clause)
            print(seg_result)

        # 判断句式：如果……就好了
        judgement = self.__is_clause_pattern2(the_clause)
        if judgement != "":
            sub_clause["pattern"].append(judgement)
            sub_clause["score"] -= judgement["value"]
            return sub_clause

        # 判断句式：是…不是…
        judgement = self.__is_clause_pattern1(the_clause)
        if judgement != "":
            sub_clause["pattern"].append(judgement)
            sub_clause["score"] -= judgement["value"]

        # 判断句式：短语
        judgement = self.__is_clause_pattern3(the_clause, seg_result)
        if judgement != "":
            sub_clause["score"] += judgement["score"]
            if judgement["score"] >= 0:
                sub_clause["positive"].append(judgement)
            elif judgement["score"] < 0:
                sub_clause["negative"].append(judgement)
            match_result = judgement["key"].split(":")[-1]
            i = 0
            while i < len(seg_result):
                if seg_result[i].word in match_result:
                    if i + 1 == len(seg_result) or seg_result[i + 1].word in match_result:
                        del (seg_result[i])
                        continue
                i += 1

        # 逐个分析分词
        for i in range(len(seg_result)):
            mark, result = self.__analyse_word(seg_result[i].word, seg_result, i)
            if mark == 0:
                continue
            elif mark == 1:
                sub_clause["conjunction"].append(result)
            elif mark == 2:
                sub_clause["punctuation"].append(result)
            elif mark == 3:
                sub_clause["positive"].append(result)
                sub_clause["score"] += result["score"]
            elif mark == 4:
                sub_clause["negative"].append(result)
                sub_clause["score"] -= result["score"]

        # 综合连词的情感值
        for a_conjunction in sub_clause["conjunction"]:
            sub_clause["score"] *= a_conjunction["value"]

        # 综合标点符号的情感值
        for a_punctuation in sub_clause["punctuation"]:
            sub_clause["score"] *= a_punctuation["value"]

        return sub_clause

    @staticmethod
    def __is_clause_pattern2(the_clause):
        re_pattern = re.compile(r".*(如果|要是|希望).+就[\u4e00-\u9fa5]+(好|完美)了")
        match = re_pattern.match(the_clause)
        if match is not None:
            pattern = {"key": "如果…就好了", "value": 1.0}
            return pattern
        return ""

    def __is_clause_pattern3(self, the_clause, seg_result):
        for a_phrase in self.__phrase_dict:
            keys = a_phrase.keys()
            to_compile = a_phrase["key"].replace("……", "[\u4e00-\u9fa5]*")

            if "start" in keys:
                to_compile = to_compile.replace("*", "{" + a_phrase["start"] + "," + a_phrase["end"] + "}")
            if "head" in keys:
                to_compile = a_phrase["head"] + to_compile

            match = re.compile(to_compile).search(the_clause)
            if match is not None:
                can_continue = True
                pos = [flag for word, flag in posseg.cut(match.group())]
                if "between_tag" in keys:
                    if a_phrase["between_tag"] not in pos and len(pos) > 2:
                        can_continue = False

                if can_continue:
                    for i in range(len(seg_result)):
                        if seg_result[i].word in match.group():
                            try:
                                if seg_result[i + 1].word in match.group():
                                    return self.__emotional_word_analysis(
                                        a_phrase["key"] + ":" + match.group(), a_phrase["value"],
                                        [x for x, y in seg_result], i)
                            except IndexError:
                                return self.__emotional_word_analysis(
                                    a_phrase["key"] + ":" + match.group(), a_phrase["value"],
                                    [x for x, y in seg_result], i)
        return ""

    def __analyse_word(self, the_word, seg_result=None, index=-1):
        # 判断是否是连词
        judgement = self.__is_word_conjunction(the_word)
        if judgement != "":
            return 1, judgement

        # 判断是否是标点符号
        judgement = self.__is_word_punctuation(the_word)
        if judgement != "":
            return 2, judgement

        # 判断是否是正向情感词
        judgement = self.__is_word_positive(the_word, seg_result, index)
        if judgement != "":
            return 3, judgement

        # 判断是否是负向情感词
        judgement = self.__is_word_negative(the_word, seg_result, index)
        if judgement != "":
            return 4, judgement

        return 0, ""

    @staticmethod
    def __is_clause_pattern1(the_clause):
        re_pattern = re.compile(r".*(要|选)的.+(送|给).*")
        match = re_pattern.match(the_clause)
        if match is not None:
            pattern = {"key": "要的是…给的是…", "value": 1}
            return pattern
        return ""

    def __is_word_conjunction(self, the_word):
        if the_word in self.__conjunction_dict:
            conjunction = {"key": the_word, "value": self.__conjunction_dict[the_word]}
            return conjunction
        return ""

    def __is_word_punctuation(self, the_word):
        if the_word in self.__punctuation_dict:
            punctuation = {"key": the_word, "value": self.__punctuation_dict[the_word]}
            return punctuation
        return ""

    def __is_word_positive(self, the_word, seg_result, index):
        # 判断分词是否在情感词典内
        if the_word in self.__positive_dict:
            # 在情感词典内，则构建一个以情感词为中心的字典数据结构
            return self.__emotional_word_analysis(the_word, self.__positive_dict[the_word],
                                                  [x for x, y in seg_result], index)
        # 不在情感词典内，则返回空
        return ""

    def __is_word_negative(self, the_word, seg_result, index):
        # 判断分词是否在情感词典内
        if the_word in self.__negative_dict:
            # 在情感词典内，则构建一个以情感词为中心的字典数据结构
            return self.__emotional_word_analysis(the_word, self.__negative_dict[the_word],
                                                  [x for x, y in seg_result], index)
        # 不在情感词典内，则返回空
        return ""

    def __emotional_word_analysis(self, core_word, value, segments, index):
        # 在情感词典内，则构建一个以情感词为中心的字典数据结构
        orientation = {"key": core_word, "adverb": [], "denial": [], "value": value}
        orientation_score = orientation["value"]  # my_sentiment_dict[segment]

        # 在三个前视窗内，判断是否有否定词、副词
        view_window = index - 1
        if view_window > -1:  # 无越界
            # 判断前一个词是否是情感词
            if segments[view_window] in self.__negative_dict or \
                            segments[view_window] in self.__positive_dict:
                orientation['score'] = orientation_score
                return orientation
            # 判断是否是副词
            if segments[view_window] in self.__adverb_dict:
                # 构建副词字典数据结构
                adverb = {"key": segments[view_window], "position": 1,
                          "value": self.__adverb_dict[segments[view_window]]}
                orientation["adverb"].append(adverb)
                orientation_score *= self.__adverb_dict[segments[view_window]]
            # 判断是否是否定词
            elif segments[view_window] in self.__denial_dict:
                # 构建否定词字典数据结构
                denial = {"key": segments[view_window], "position": 1,
                          "value": self.__denial_dict[segments[view_window]]}
                orientation["denial"].append(denial)
                orientation_score *= -1
        view_window = index - 2
        if view_window > -1:
            # 判断前一个词是否是情感词
            if segments[view_window] in self.__negative_dict or \
                            segments[view_window] in self.__positive_dict:
                orientation['score'] = orientation_score
                return orientation
            if segments[view_window] in self.__adverb_dict:
                adverb = {"key": segments[view_window], "position": 2,
                          "value": self.__adverb_dict[segments[view_window]]}
                orientation_score *= self.__adverb_dict[segments[view_window]]
                orientation["adverb"].insert(0, adverb)
            elif segments[view_window] in self.__denial_dict:
                denial = {"key": segments[view_window], "position": 2,
                          "value": self.__denial_dict[segments[view_window]]}
                orientation["denial"].insert(0, denial)
                orientation_score *= -1
                # 判断是否是“不是很好”的结构（区别于“很不好”）
                if len(orientation["adverb"]) > 0:
                    # 是，则引入调节阈值，0.3
                    orientation_score *= 0.3
        view_window = index - 3
        if view_window > -1:
            # 判断前一个词是否是情感词
            if segments[view_window] in self.__negative_dict or segments[view_window] in self.__positive_dict:
                orientation['score'] = orientation_score
                return orientation
            if segments[view_window] in self.__adverb_dict:
                adverb = {"key": segments[view_window], "position": 3,
                          "value": self.__adverb_dict[segments[view_window]]}
                orientation_score *= self.__adverb_dict[segments[view_window]]
                orientation["adverb"].insert(0, adverb)
            elif segments[view_window] in self.__denial_dict:
                denial = {"key": segments[view_window], "position": 3,
                          "value": self.__denial_dict[segments[view_window]]}
                orientation["denial"].insert(0, denial)
                orientation_score *= -1
                # 判断是否是“不是很好”的结构（区别于“很不好”）
                if len(orientation["adverb"]) > 0 and len(orientation["denial"]) == 0:
                    orientation_score *= 0.3
        # 添加情感分析值。
        orientation['score'] = orientation_score
        # 返回的数据结构
        return orientation

    # 输出comment_analysis分析的数据结构结果
    def __output_analysis(self, comment_analysis, runout_filepath=None):
        output = "Score:" + str(comment_analysis["score"]) + "\n"

        for i in range(len(comment_analysis) - 1):
            output += "Sub-clause" + str(i) + ": "
            clause = comment_analysis["su-clause" + str(i)]
            if len(clause["conjunction"]) > 0:
                output += "conjunction:"
                for punctuation in clause["conjunction"]:
                    output += punctuation["key"] + " "
            if len(clause["positive"]) > 0:
                output += "positive:"
                for positive in clause["positive"]:
                    if len(positive["denial"]) > 0:
                        for denial in positive["denial"]:
                            output += denial["key"] + str(denial["position"]) + "-"
                    if len(positive["adverb"]) > 0:
                        for adverb in positive["adverb"]:
                            output += adverb["key"] + str(adverb["position"]) + "-"
                    output += positive["key"] + " "
            if len(clause["negative"]) > 0:
                output += "negative:"
                for negative in clause["negative"]:
                    if len(negative["denial"]) > 0:
                        for denial in negative["denial"]:
                            output += denial["key"] + str(denial["position"]) + "-"
                    if len(negative["adverb"]) > 0:
                        for adverb in negative["adverb"]:
                            output += adverb["key"] + str(adverb["position"]) + "-"
                    output += negative["key"] + " "
            if len(clause["punctuation"]) > 0:
                output += "punctuation:"
                for punctuation in clause["punctuation"]:
                    output += punctuation["key"] + " "
            if len(clause["pattern"]) > 0:
                output += "pattern:"
                for pattern in clause["pattern"]:
                    output += pattern["key"] + " "
            # if clause["pattern"] is not None:
            #     output += "pattern:" + clause["pattern"]["key"] + " "
            output += "\n"
        if runout_filepath is not None:
            self.__write_runout_file(runout_filepath, output)
        else:
            print(output)

    def __divide_sentence_into_clauses(self, the_sentence):
        the_clauses = self.__split_sentence(the_sentence)

        # 识别“是……不是……”句式
        pattern = re.compile(r"([，、。%！；？?,!～~.… ]*)([\u4e00-\u9fa5]*?(要|选)"
                             r"的.+(送|给)[\u4e00-\u9fa5]+?[，。！%；、？?,!～~.… ]+)")
        match = re.search(pattern, the_sentence.strip())
        if match is not None and len(self.__split_sentence(match.group(2))) <= 2:
            to_delete = []
            for i in range(len(the_clauses)):
                if the_clauses[i] in match.group(2):
                    to_delete.append(i)
            if len(to_delete) > 0:
                for i in range(len(to_delete)):
                    the_clauses.remove(the_clauses[to_delete[0]])
                the_clauses.insert(to_delete[0], match.group(2))

        # 识别“要是|如果……就好了”的假设句式
        pattern = re.compile(r"([，%。、！；？?,!～~.… ]*)([\u4e00-\u9fa5]*?(如果|要是|"
                             r"希望).+就[\u4e00-\u9fa5]+(好|完美)了[，。；！%、？?,!～~.… ]+)")
        match = re.search(pattern, the_sentence.strip())
        if match is not None and len(self.__split_sentence(match.group(2))) <= 3:
            to_delete = []
            for i in range(len(the_clauses)):
                if the_clauses[i] in match.group(2):
                    to_delete.append(i)
            if len(to_delete) > 0:
                for i in range(len(to_delete)):
                    the_clauses.remove(the_clauses[to_delete[0]])
                the_clauses.insert(to_delete[0], match.group(2))

        the_clauses[-1] = the_clauses[-1][:-1]
        return the_clauses

    @staticmethod
    def __split_sentence(sentence):
        pattern = re.compile("[，。%、！!？?,；～~.… ]+")

        split_clauses = pattern.split(sentence.strip())
        punctuations = pattern.findall(sentence.strip())
        try:
            split_clauses.remove("")
        except ValueError:
            pass
        punctuations.append("")

        clauses = [''.join(x) for x in zip(split_clauses, punctuations)]

        return clauses

    def __get_phrase_dict(self):
        sentiment_dict = []
        pattern = re.compile(r"\s+")
        with open(self.__root_filepath + "phrase_dict.txt", "r", encoding="utf-8") as f:
            for line in f:
                a_phrase = {}
                result = pattern.split(line.strip())
                if len(result) >= 2:
                    a_phrase["key"] = result[0]
                    a_phrase["value"] = float(result[1])
                    for i, a_split in enumerate(result):
                        if i < 2:
                            continue
                        else:
                            a, b = a_split.split(":")
                            a_phrase[a] = b
                    sentiment_dict.append(a_phrase)

        return sentiment_dict

    # 情感词典的构建
    @staticmethod
    def __get_dict(path, encoding="utf-8"):
        sentiment_dict = {}
        pattern = re.compile(r"\s+")
        with open(path) as f:
            for line in f:
                result = pattern.split(line.strip())
                if len(result) == 2:
                    sentiment_dict[result[0]] = float(result[1])
        return sentiment_dict

    @staticmethod
    def __write_runout_file(path, info, encoding="utf-8"):
        with open(path, "a") as f:
            f.write("%s" % info)


# ################################################
# classifier based on K-Nearest Neighbours
# ################################################
class KNNClassifier:
    def __init__(self, train_data, train_data_labels, k=3, best_words=None, stopwords=None):
        self.__train_data_labels = []
        self.__total_words = []
        self.__k = k
        self.__stopwords = stopwords
        self.__train_data_vectors = None
        self.__total_words_length = 0
        self.train_num = 0
        if train_data is not None:
            self.__train(train_data, train_data_labels, best_words)

    def set_k(self, k):
        self.__k = k

    def __doc2vector(self, doc):
        the_vector = [0] * self.__total_words_length
        for i in range(self.__total_words_length):
            the_vector[i] = doc.count(self.__total_words[i])
        length = sum(the_vector)
        if length == 0:
            return [0 for _ in the_vector]
        return [i / length for i in the_vector]
        # return the_vector

    def __get_total_words(self, train_data, best_words):
        if best_words is not None:
            total_words = best_words[:]
        else:
            total_words = set()
            for doc in train_data:
                total_words |= set(doc)
        if self.__stopwords:                      # 删除停用词
            with open(self.__stopwords) as sw_f:
                for line in sw_f:
                    if line.strip() in total_words:
                        total_words.remove(line.strip())
        return list(total_words)

    @staticmethod
    def __normalize(vectors):
        min_values = vectors.min(axis=0)
        max_values = vectors.max(axis=0)
        ranges = max_values - min_values
        m = vectors.shape[0]
        norm_vectors = vectors - np.tile(min_values, (m, 1))
        norm_vectors = norm_vectors / np.tile(ranges, (m, 1))
        return norm_vectors

    def __train(self, train_data, train_data_labels, best_words=None):
        print("KNNClassifier is training ...... ")

        self.__train_data_labels = train_data_labels[:]
        self.__total_words = self.__get_total_words(train_data, best_words)
        self.__total_words_length = len(self.__total_words)
        vectors = []
        for doc in train_data:
            vectors.append(self.__doc2vector(doc))
            self.train_num += 1

        self.__train_data_vectors = np.array(vectors)
        # self.__train_data_vectors = self.__normalize(np.array(vectors))

        print("KNNClassifier trains over!")

    def __get_sorted_distances(self, input_data):
        size = self.__train_data_vectors.shape
        vector = self.__doc2vector(input_data)
        input_data_vector = np.array(vector)
        diff_mat = np.tile(input_data_vector, (size[0], 1)) - self.__train_data_vectors
        sq_diff_mat = diff_mat ** 2
        sq_distances = sq_diff_mat.sum(axis=1)
        distances = sq_distances ** 0.5
        sorted_distances = distances.argsort()

        return sorted_distances

    def classify(self, input_data):
        if isinstance(self.__k, int):
            return self.single_k_classify(input_data)
        elif isinstance(self.__k, list):
            return self.multiple_k_classify(input_data)
        else:
            print("Wrong k.")

    def multiple_k_classify(self, input_data):
        # get the distance sorted list
        sorted_distances = self.__get_sorted_distances(input_data)

        # some variable
        i = 0
        # class_count[0] records the number of label "0"
        # class_count[1] records the number of label "1"
        class_count = [0, 0]
        # final_record[0] records the number of label "0"
        # final_record[1] records the number of label "1"
        final_record = [0, 0]

        # assert type(k) == list
        assert type(self.__k) == list

        for k in sorted(self.__k):
            while i < k:
                label = self.__train_data_labels[sorted_distances[i]]
                class_count[label] += 1
                i += 1
            if class_count[0] > class_count[1]:
                final_record[0] += 1
            else:
                final_record[1] += 1

        if final_record[0] > final_record[1]:
            return 0
        else:
            return 1

    def single_k_classify(self, input_data):
        # get the distance sorted list
        sorted_distances = self.__get_sorted_distances(input_data)

        # some variable
        i = 0
        # class_count[0] records the number of label "0"
        # class_count[1] records the number of label "1"
        class_count = [0, 0]

        while i < self.__k:
            label = self.__train_data_labels[sorted_distances[i]]
            class_count[label] += 1
            i += 1

        if class_count[0] > class_count[1]:
            return 0
        else:
            return 1


# ################################################
# classifier based on Naive bayes
# ################################################
class BayesClassifier:
    def __init__(self, train_data, train_data_labels, best_words):
        self._pos_word_p = {}
        self._neg_word_p = {}
        self._pos_p = 0.
        self._neg_p = 1.
        self._train(train_data, train_data_labels, best_words)

    def _train(self, train_data, train_data_labels, best_words=None):
        """
        this method is different from the the method self.train()
        we use the training data, do some feature selection, then train,
        get some import values
        :param train_data:
        :param train_data_labels:
        :param best_words:
        """
        print("BayesClassifier is training ...... ")

        # get the frequency information of each word
        total_pos_data, total_neg_data = {}, {}
        total_pos_length, total_neg_length = 0, 0
        total_word = set()
        for i, doc in enumerate(train_data):
            if train_data_labels[i] == 1:
                for word in doc:
                    if best_words is None or word in best_words:
                        total_pos_data[word] = total_pos_data.get(word, 0) + 1
                        total_pos_length += 1
                        total_word.add(word)
            else:
                for word in doc:
                    if best_words is None or word in best_words:
                        total_neg_data[word] = total_neg_data.get(word, 0) + 1
                        total_neg_length += 1
                        total_word.add(word)
        self._pos_p = total_pos_length / (total_pos_length + total_neg_length)
        self._neg_p = total_neg_length / (total_pos_length + total_neg_length)

        # get each word's probability
        for word in total_word:
            self._pos_word_p[word] = np.log(total_pos_data.get(word, 1e-100) / total_pos_length)
            self._neg_word_p[word] = np.log(total_neg_data.get(word, 1e-100) / total_neg_length)

        print("BayesClassifier trains over!")

    def classify(self, input_data):
        """
        according to the input data, calculate the probability of the each class
        :param input_data:
        """
        pos_score = 0.
        for word in input_data:
            pos_score += self._pos_word_p.get(word, 0.)
        pos_score += np.log(self._pos_p)

        neg_score = 0.
        for word in input_data:
            neg_score += self._neg_word_p.get(word, 0.)
        neg_score += np.log(self._neg_p)

        if pos_score > neg_score:
            return 1
        else:
            return 0


# ################################################
# classifier based on Maximum Entropy
# ################################################
class MaxEntClassifier:
    def __init__(self, max_iter=500):
        self.feats = defaultdict(int)
        self.labels = {0, 1}
        self.weight = []
        self.max_iter = max_iter

    def prob_weight(self, features, label):
        weight = 0.0
        for feature in features:
            if (label, feature) in self.feats:
                weight += self.weight[self.feats[(label, feature)]]
        return np.exp(weight)

    def calculate_probability(self, features):
        weights = [(self.prob_weight(features, label), label) for label in self.labels]
        try:
            z = sum([weight for weight, label in weights])
            prob = [(weight / z, label) for weight, label in weights]
        except ZeroDivisionError:
            return "collapse"
        return prob

    def convergence(self, last_weight):
        for w1, w2 in zip(last_weight, self.weight):
            if abs(w1 - w2) >= 0.001:
                return False
        return True

    def train(self, train_data, train_data_labels, best_words=None):
        print("MaxEntClassifier is training ...... ")

        # init the parameters
        train_data_length = len(train_data_labels)
        if best_words is None:
            for i in range(train_data_length):
                for word in set(train_data[i]):
                    self.feats[(train_data_labels[i], word)] += 1
        else:
            for i in range(train_data_length):
                for word in set(train_data[i]):
                    if word in best_words:
                        self.feats[(train_data_labels[i], word)] += 1

        the_max = max([len(record) - 1 for record in train_data])  # the_max param for GIS training algorithm
        self.weight = [0.0] * len(self.feats)  # init weight for each feature
        ep_empirical = [0.0] * len(self.feats)  # init the feature expectation on empirical distribution
        for i, f in enumerate(self.feats):
            ep_empirical[i] = self.feats[f] / train_data_length  # feature expectation on empirical distribution
            self.feats[f] = i  # each feature function correspond to id

        for i in range(self.max_iter):
            ep_model = [0.0] * len(self.feats)  # feature expectation on model distribution
            for doc in train_data:
                prob = self.calculate_probability(doc)  # calculate p(y|x)
                if prob == "collapse":
                    print("The program collapse. The iter number: %d." % (i + 1))
                    return
                for feature in doc:
                    for weight, label in prob:
                        if (label, feature) in self.feats:  # only focus on features from training data.
                            idx = self.feats[(label, feature)]  # get feature id
                            ep_model[idx] += weight * (1.0 / train_data_length)  # sum(1/N * f(y,x)*p(y|x)), p(x) = 1/N

            last_weight = self.weight[:]
            for j, win in enumerate(self.weight):
                delta = 1.0 / the_max * np.log(ep_empirical[j] / ep_model[j])
                self.weight[j] += delta  # update weight

            # test if the algorithm is convergence
            if self.convergence(last_weight):
                print("The program convergence. The iter number: %d." % (i + 1))
                break

        print("MaxEntClassifier trains over!")

    def test(self, train_data, train_labels, best_words, test_data):
        classify_results = []

        # init the parameters
        train_data_length = len(train_labels)
        if best_words is None:
            for i in range(train_data_length):
                for word in set(train_data[i]):
                    self.feats[(train_labels[i], word)] += 1
        else:
            for i in range(train_data_length):
                for word in set(train_data[i]):
                    if word in best_words:
                        self.feats[(train_labels[i], word)] += 1

        the_max = max([len(record) - 1 for record in train_data])  # the_max param for GIS training algorithm
        self.weight = [0.0] * len(self.feats)  # init weight for each feature
        ep_empirical = [0.0] * len(self.feats)  # init the feature expectation on empirical distribution
        for i, f in enumerate(self.feats):
            ep_empirical[i] = self.feats[f] / train_data_length  # feature expectation on empirical distribution
            self.feats[f] = i  # each feature function correspond to id

        for i in range(self.max_iter):
            print("MaxEntClassifier is training ...... ")

            ep_model = [0.0] * len(self.feats)  # feature expectation on model distribution
            for doc in train_data:
                prob = self.calculate_probability(doc)  # calculate p(y|x)
                if prob == "collapse":
                    print("The program collapse. The iter number: %d." % (i + 1))
                    return
                for feature in doc:
                    for weight, label in prob:
                        if (label, feature) in self.feats:  # only focus on features from training data.
                            idx = self.feats[(label, feature)]  # get feature id
                            ep_model[idx] += weight * (1.0 / train_data_length)  # sum(1/N * f(y,x)*p(y|x)), p(x) = 1/N

            last_weight = self.weight[:]
            for j, win in enumerate(self.weight):
                delta = 1.0 / the_max * np.log(ep_empirical[j] / ep_model[j])
                self.weight[j] += delta  # update weight

            print("MaxEntClassifier is testing ...")
            classify_labels = []
            for data in test_data:
                classify_labels.append(self.classify(data))
            classify_results.append(classify_labels)

            # test if the algorithm is convergence
            if self.convergence(last_weight):
                print("The program convergence. The iter number: %d." % (i + 1))
                break

        print("MaxEntClassifier trains over!")

        return classify_results

    def classify(self, the_input_features):
        prob = self.calculate_probability(the_input_features)
        prob.sort(reverse=True)
        if prob[0][0] > prob[1][0]:
            return prob[0][1]
        else:
            return prob[1][1]


# ################################################
# classifier based on Support Vector Machine
# ################################################
from sklearn.svm import SVC


class SVMClassifier:
    def __init__(self, train_data, train_labels, best_words, C):
        train_data = np.array(train_data)
        train_labels = np.array(train_labels)

        self.best_words = best_words
        self.clf = SVC(C=C)
        self.__train(train_data, train_labels)

    def words2vector(self, all_data):
        vectors = []
        for data in all_data:
            vector = []
            for feature in self.best_words:
                vector.append(data.count(feature))
            vectors.append(vector)

        vectors = np.array(vectors)
        return vectors

    def __train(self, train_data, train_labels):
        print("SVMClassifier is training ...... ")

        train_vectors = self.words2vector(train_data)

        self.clf.fit(train_vectors, np.array(train_labels))

        print("SVMClassifier trains over!")

    def classify(self, data):
        vector = self.words2vector([data])

        prediction = self.clf.predict(vector)

        return prediction[0]
