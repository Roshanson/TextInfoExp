import os

import re
import pandas as pd
from sklearn.model_selection import train_test_split

base_path = os.getcwd()


def get_text():
    text_tag = []
    tags = ['Art', 'Computer', 'Sports']
    for tag in tags:
        filelist = os.listdir('./data_train/' + tag)
        for file in filelist:
            f = open('./data_train/' + tag + '/' + file, 'r', encoding='utf-8')
            text = f.read().replace('\n', '')
            data = ''.join(re.findall(u'[\u4e00-\u9fff]+', text))  # 必须为unicode类型，取出所有中文字符 也可去除停用词
            text_tag.append([file.strip('.txt'), data, tag])

    return pd.DataFrame(text_tag, columns=['id', 'text', 'tag'])


def get_feature(row):
    text_id, text, tag = row.id, row.text, row.tag

    # 简单的写两个特征，实际中文本分类可用tf-df  poi  向量等方式构造特征
    text_len = len(text)
    isHasSH = 1 if '上海' in text else 0
    return [text_len, isHasSH]


def load_data():
    df = get_text()
    df['features'] = df.apply(get_feature, axis=1)
    df = df[['tag', 'features']]
    X, Y = df.ix[:, 1:].values, df.ix[:, 0].values
    # print(X[0:10], Y[0:10])
    X = list(map(lambda x: list(x)[0], X))
    print(X[:10])
    print(Y[:10])
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=1, shuffle=True)
    return X_train, X_test, y_train, y_test


pass

