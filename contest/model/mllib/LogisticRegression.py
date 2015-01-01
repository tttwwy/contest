# coding=utf-8
# created by WangZhe on 2014/12/19
from scipy.sparse import lil_matrix,vstack
from sklearn import linear_model
from pyspark.mllib.classification import LogisticRegressionWithLBFGS
from pyspark.mllib.tree import RandomForest

class LR():
    def __init__(self):
        self.train_data_type = 'mllib'
        self.model_name = 'LR'

    def train(self,data,**kwargs):
        model = LogisticRegressionWithLBFGS.train(data=data,**kwargs)
        model.clearThreshold()
        self.model = model

    def predict_value(self,data):
        # uid, y, x = fdata
        prob = self.model.predict(data)
        return prob

    def predict_values(self,data):
        probs = self.model.predict(data)
        return probs



if __name__ == "__main__":
    pass