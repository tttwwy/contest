# coding=utf-8
# created by WangZhe on 2014/12/19
from scipy.sparse import lil_matrix,vstack
from sklearn import linear_model
from pyspark.mllib.classification import LogisticRegressionWithLBFGS


class LR():
    def __init__(self):
        self.train_data_type = 'mllib'
        self.train_args = {}

    def train_fdata(self,fdata,**kwargs):

        model = LogisticRegressionWithLBFGS.train(data=fdata,**kwargs)
        model.clearThreshold()
        # model = linear_model.LogisticRegression(**kwargs)
        # model.fit(x, y)
        self.model = model
        self.train_args.update(kwargs)

    def predict_value(self,fdata):
        # uid, y, x = fdata
        prob = self.model.predict(fdata)
        return prob

    def predict_values(self,fdata):        
        probs = self.model.predict(fdata)
        return probs



if __name__ == "__main__":
    pass