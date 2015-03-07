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

    @run_time
    def transform_pairwise(self,x,y):
        x_new = []
        y_new = []
        y = np.asarray(y)
        comb = itertools.combinations(range(x.shape[0]),2)
        for k,(i,j) in enumerate(comb):
            if y[i] == y[j]:
                continue
            x_new.append(x[i] -x[j])
            y_new.append(np.sign(y[i] - y[j]))
            if y_new[-1] != (-1) ** k:
                x_new[-1] = - x_new[-1]
                y_new[-1] = - y_new[-1]

        return np.asarray(x_new),np.asarray(y_new)

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
