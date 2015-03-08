# coding=utf-8
# created by WangZhe on 2014/12/19
from scipy.sparse import lil_matrix,vstack
from sk import linear_model



class Lasso():
    def __init__(self):
        self.train_data_type = 'sklearn_dense'
        self.model_name = 'Lasso'

    def train(self,data,**kwargs):
        uid, y, x = data
        model = linear_model.Lasso(**kwargs)
        model.fit(x, y)
        self.model = model

    def predict_value(self,data):
        value = self.model.predict(data)[0][1]
        return value

    def predict_values(self,data):
        values = self.model.predict(data)
        return values



if __name__ == "__main__":
    pass