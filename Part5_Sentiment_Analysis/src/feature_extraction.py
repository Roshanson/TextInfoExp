
class ChiSquare:
    def __init__(self, doc_list, doc_labels):
        self.total_data, self.total_pos_data, self.total_neg_data = {}, {}, {}
        for i, doc in enumerate(doc_list):
            if doc_labels[i] == 1:
                for word in doc:
                    self.total_pos_data[word] = self.total_pos_data.get(word, 0) + 1
                    self.total_data[word] = self.total_data.get(word, 0) + 1
            else:
                for word in doc:
                    self.total_neg_data[word] = self.total_neg_data.get(word, 0) + 1
                    self.total_data[word] = self.total_data.get(word, 0) + 1

        total_freq = sum(self.total_data.values())
        total_pos_freq = sum(self.total_pos_data.values())
        # total_neg_freq = sum(self.total_neg_data.values())

        self.words = {}
        for word, freq in self.total_data.items():
            pos_score = self.__calculate(self.total_pos_data.get(word, 0), freq, total_pos_freq, total_freq)
            # neg_score = self.__calculate(self.total_neg_data.get(word, 0), freq, total_neg_freq, total_freq)
            self.words[word] = pos_score * 2

    @staticmethod
    def __calculate(n_ii, n_ix, n_xi, n_xx):
        n_ii = n_ii
        n_io = n_xi - n_ii
        n_oi = n_ix - n_ii
        n_oo = n_xx - n_ii - n_oi - n_io
        return n_xx * (float((n_ii*n_oo - n_io*n_oi)**2) /
                       ((n_ii + n_io) * (n_ii + n_oi) * (n_io + n_oo) * (n_oi + n_oo)))

    def best_words(self, num, need_score=False):
        words = sorted(self.words.items(), key=lambda word_pair: word_pair[1], reverse=True)
        if need_score:
            return [word for word in words[:num]]
        else:
            return [word[0] for word in words[:num]]







