# coding=utf-8
# created by WangZhe on 2014/12/19



class Sklearn():
    def __init__(self,model):
        self.train_data_type = 'sklearn_dense'
        self.model = model()
        self.model_name = type(self.model).__name__


    def train(self,data,**kwargs):
        uid, y, x = data
        model = self.model.set_params(**kwargs)
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