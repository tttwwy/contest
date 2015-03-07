# coding=utf-8
# created by WangZhe on 2014/12/25
from contest.util import conf
conf.set_config_path('G:/Program/python/contest/score/src/setting.py')
from contest.util.log import logging
logging.setLevel('ERROR')
from sklearn import linear_model
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from src.mycontest import MyContest
from contest.model.sklearn.sklearn import Sklearn
import itertools
model = MyContest()


feature_list = [
                # 'uid_term[0-9]_score[1-3]',
                '.*',
]
train_fdata = model.features_to_fdata(r'G:/Program/python/contest/score/feature/train',feature_list)
test_fdata = model.features_to_fdata(r'G:/Program/python/contest/score/feature/test',feature_list)
columns = list(set(train_fdata.columns).intersection(set(test_fdata.columns)))
train_fdata = train_fdata[columns]
test_fdata = test_fdata[columns]
validation_train_data,validation_test_data = model.divide_data(train_fdata,0.5)


# RR = Sklearn(linear_model.Ridge)
# model.train_fdata(validation_train_data, RR, alpha=alpha, copy_X=True, fit_intercept=True, max_iter=None,
#                   normalize=True, solver='auto', tol=tol)
# model.submit_fdata(test_fdata,file_name = 'G:/Program/python/contest/score/submit/submit.txt')


        # RR = Sklearn(linear_model.Lasso)
        # model.train_fdata(validation_train_data, RR, alpha=alpha, copy_X=True, fit_intercept=True, max_iter=1000,
        #                   normalize=True, positive=True, precompute='auto', tol=tol,
        #                   warm_start=False)

RR = Sklearn(linear_model.Ridge)

result =  model.gird_search(validation_train_data,validation_test_data,RR, alpha=[0.01,0.1,1], copy_X=True, fit_intercept=True,
                  max_iter=None,
                  normalize=True, solver='auto', tol=[0.1,0.01]
)
for param,score in result:
    print param,score['score']

        #
RR = Sklearn(GradientBoostingRegressor)
model.train_fdata(validation_train_data, RR, n_estimators=1000, learning_rate=0.1,
                  max_depth=1, random_state=0, loss='ls')

        # RR = Sklearn(RandomForestRegressor)
        # model.train_fdata(train_fdata, RR, n_estimators=100,max_features ='auto',max_depth=3)

        # print alpha,tol,model.evaluate_fdata(validation_test_data)
