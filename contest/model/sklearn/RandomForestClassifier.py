# coding=utf-8
# created by WangZhe on 2014/12/19
from scipy.sparse import lil_matrix,vstack

from sklearn import ensemble


class RF():
    def __init__(self):
        self.train_data_type = 'sklearn'
        self.model_name = 'RF'

    def train(self,data,**kwargs):
        uid, y, x = data
        model = ensemble.RandomForestClassifier(**kwargs)
        model.fit(x, y)
        self.model = model

    def predict_value(self,data):
        # uid, y, x = fdata
        prob = self.model.predict_proba(data)[0][1]
        return prob

    def predict_values(self,data):
        uid,y,x = data
        probs = self.model.predict_proba(x)
        return probs[:][1]



if __name__ == "__main__":
    pass