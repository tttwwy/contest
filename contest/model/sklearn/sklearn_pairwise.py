# coding=utf-8
# created by WangZhe on 2014/12/19

import numpy as np
import itertools
from contest.util.log import logging,run_time

class PairWise():
    def __init__(self,model):
        self.train_data_type = 'sklearn_dense'
        self.model = model()
        self.model_name = type(self.model).__name__ + "_Pairwise"

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
        """Transforms data into pairs with balanced labels for ranking

        Transforms a n-class ranking problem into a two-class classification
        problem. Subclasses implementing particular strategies for choosing
        pairs should override this method.

        In this method, all pairs are choosen, except for those that have the
        same target value. The output is an array of balanced classes, i.e.
        there are the same number of -1 as +1

        Parameters
        ----------
        X : array, shape (n_samples, n_features)
            The data
        y : array, shape (n_samples,) or (n_samples, 2)
            Target labels. If it's a 2D array, the second column represents
            the grouping of samples, i.e., samples with different groups will
            not be considered.

        Returns
        -------
        X_trans : array, shape (k, n_feaures)
            Data as pairs
        y_trans : array, shape (k,)
            Output class labels, where classes have values {-1, +1}
        """
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
        model = self.model.set_params(**kwargs)
        logging.info('{x[0]},{x[1]}'.format(x = new_x.shape))
        model.fit(new_x, new_y)
        self.model = model

    def predict_value(self,data):
        value = self.model.predict(data)[0]
        return value

    @run_time
    def predict_values(self,x):
        values = range(x.shape[0])


        result = sorted(values,cmp=lambda a,b:cmp(self.predict_value(x[a] - x[b]),0))
        result = {x:index for index,x in enumerate(result)}
        new_result =  [result[index] for index in values]
        return new_result



if __name__ == "__main__":
    pass
