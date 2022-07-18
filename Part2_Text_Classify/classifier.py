# -*- coding:utf-8 -*-
import pickle
import numpy as np
from sklearn.metrics import classification_report
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, BaggingClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from mlxtend.classifier import StackingClassifier

from xgboost import XGBClassifier

from Part2_Text_Classify.feature import load_data


class Classifier(object):
    """
    LR Bayes SVM XGB  decisian tree random forest ...
    """

    def __init__(self, model_name):
        self.model_name = model_name
        self.model = None

    def save_model(self):
        with open(f'./model/{self.model_name}.pkl', 'wb') as fw:
            pickle.dump(self.model, fw)

    def load_model(self):
        with open(f'./model/{self.model_name}.pkl', 'rb') as fr:
            self.model = pickle.load(self.model, fr)

    def eval_prob(self, X_test):
        return self.model.predict_proba(X_test)

    def cls(self, X_train, X_test, y_train, y_test):
        if self.model_name == 'lr':
            self.model = LogisticRegression()
        elif self.model_name == 'xgb':
            self.model = XGBClassifier()
        elif self.model_name == 'svm':
            self.model = SVC(kernel='linear')
        elif self.model_name == 'bayes':
            # self.model = GaussianNB()
            self.model = BernoulliNB()  # 最好
            # self.model = MultinomialNB()
        elif self.model_name == 'rf':
            """ 在bagging 的基础上,引入特征抽样，即随机抽取若干特征"""
            self.model = RandomForestClassifier()
        elif self.model_name == 'dt':
            self.model = DecisionTreeClassifier()
        elif self.model_name == 'et':
            self.model = ExtraTreesClassifier()
        elif self.model_name == 'ensemble':
            model1 = LogisticRegression()
            model2 = BernoulliNB()
            model3 = RandomForestClassifier()
            model4 = DecisionTreeClassifier()
            model5 = ExtraTreesClassifier()
            model6 = GradientBoostingClassifier()
            # self.model = VotingClassifier(estimators=[('lr', model1), ('dt', model4)])

            # self.model = BaggingClassifier(model4, n_estimators=100, max_samples=0.3)  # dt 进行bag == rf

            self.model = StackingClassifier(classifiers=[model3, model4, model5, model6],
                                            use_probas=True,
                                            average_probas=False,
                                            meta_classifier=model1)
            # self.model = GradientBoostingClassifier()

            #  采用网格搜索参数
            # params = {'lr__C': [1.0, 100.0], 'rf__n_estimators': [20, 200]}
            # self.model = GridSearchCV(estimator=model_ensemble, param_grid=params, cv=5)

        X_train = np.array(X_train)
        y_train = np.array(y_train)
        self.model.fit(X_train, y_train)

        print(self.model.score(X_test, y_test))
        print(classification_report(self.model.predict(X_test), y_test))


if __name__ == '__main__':
    X_train, X_test, y_train, y_test = load_data()
    # lr(X_train, X_test, y_train, y_test)
    # xgb(X_train, X_test, y_train, y_test)
    # svc(X_train, X_test, y_train, y_test)
    model = Classifier('dt')  # dt  bayes(Gaussian Mul Bernoulli)  lr  svm  xgb ensemble
    model.cls(X_train, X_test, y_train, y_test)
    # model.save_model()
