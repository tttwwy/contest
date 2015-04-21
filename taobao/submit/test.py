# coding=utf-8
# created by WangZhe on 2015/3/7
import numpy as np
from contest.model.sklearn.sklearn_pairwise import PairWise
from sklearn import svm
y = np.array([3, 2, 4, 1])
x = np.array([[3, 3], [2, 2], [5, 4], [2, 2]])
data = [y, y, x]

model = PairWise(svm.SVC)
model.train(data)
print model.predict_values(x)
if __name__ == "__main__":
    pass
