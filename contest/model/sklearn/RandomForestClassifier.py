# coding=utf-8
# created by WangZhe on 2014/12/19
from scipy.sparse import lil_matrix,vstack

from sklearn import ensemble


class RF():
    def __init__(self):
        self.train_data_type = 'sklearn'
        self.train_args = {}

    def train_fdata(self,fdata,**kwargs):
        uid, y, x = fdata
        model = ensemble.RandomForestClassifier(**kwargs)
        model.fit(x, y)
        self.model = model
        self.train_args.update(kwargs)

    def predict_value(self,fdata):
        # uid, y, x = fdata
        prob = self.model.predict_proba(fdata)[0][1]
        return prob

    def predict_values(self,fdata):
        uid,y,x = fdata
        probs = self.model.predict_proba(x)
        return probs[:][1]



if __name__ == "__main__":
    pass