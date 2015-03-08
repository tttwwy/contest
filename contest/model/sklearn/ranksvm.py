# coding=utf-8
# created by WangZhe on 2014/12/19

import numpy as np
import itertools
from contest.util.log import logging,run_time
from sklearn.svm import LinearSVC
class RankSVM():
    def __init__(self):
        self.train_data_type = 'sklearn_dense'
        self.model_name = "RankSVM"

    # @run_time
    # def transform_pairwise(self,x,y):
    #     x_new = []
    #     y_new = []
    #     y = np.asarray(y)
    #     comb = itertools.combinations(range(x.shape[0]),2)
    #     for k,(i,j) in enumerate(comb):
    #         if y[i] == y[j]:
    #             continue
    #         x_new.append(x[i] -x[j])
    #         y_new.append(np.sign(y[i] - y[j]))
    #         if y_new[-1] != (-1) ** k:
    #             x_new[-1] = - x_new[-1]
    #             y_new[-1] = - y_new[-1]
    #
    #     return np.asarray(x_new),np.asarray(y_new)

    @run_time
    def transform_pairwise(self,X, y):
        X_new = []
        y_new = []
        y = np.asarray(y)
        if y.ndim == 1:
            y = np.c_[y, np.ones(y.shape[0])]
        comb = itertools.combinations(range(X.shape[0]), 2)
        for k, (i, j) in enumerate(comb):
            if y[i, 0] == y[j, 0] or y[i, 1] != y[j, 1]:
                # skip if same target or different group
                continue
            X_new.append(X[i] - X[j])
            y_new.append(np.sign(y[i, 0] - y[j, 0]))
            # output balanced classes
            if y_new[-1] != (-1) ** k:
                y_new[-1] = - y_new[-1]
                X_new[-1] = - X_new[-1]
        return np.asarray(X_new), np.asarray(y_new).ravel()


    @run_time
    def train(self,data,**kwargs):
        uid, y, x = data
        new_x,new_y = self.transform_pairwise(x,y)
        model = LinearSVC(**kwargs)
        logging.info('{x[0]},{x[1]}'.format(x = new_x.shape))
        model.fit(new_x, new_y)
        self.model = model

    def predict_value(self,data):
        value = self.model.predict(data)[0]
        return value

    @run_time
    def predict_values(self,x):

        if hasattr(self.model, 'coef_'):
            return np.dot(x, self.model.coef_.T)

        else:
            raise ValueError("Must call fit() prior to predict()")



if __name__ == "__main__":
    pass
