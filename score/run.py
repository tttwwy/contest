# coding=utf-8
# created by WangZhe on 2014/12/25
from contest.util import conf
conf.set_config_path('G:/Program/python/contest/score/src/setting.py')
from contest.util.log import logging
logging.setLevel('ERROR')
from sklearn import linear_model
from sklearn.ensemble import GradientBoostingRegressor
from src.mycontest import MyContest
from contest.model.sklearn.sklearn import Sklearn
model = MyContest()


feature_list = [
                # 'uid_term[0-9]_score[1-3]',
                '.*',
]
train_fdata = model.features_to_fdata(r'G:/Program/python/contest/score/feature/train',feature_list)
test_fdata = model.features_to_fdata(r'G:/Program/python/contest/score/feature/test',feature_list)
columns = list(set(train_fdata.columns).intersection(set(test_fdata.columns)))
print columns
train_fdata = train_fdata[columns]
test_fdata = test_fdata[columns]
validation_train_data,validation_test_data = model.divide_data(train_fdata,0.5)


alpha = 0.001
tol = 0.1
RR = Sklearn(linear_model.Ridge)
model.train_fdata(train_fdata, RR, alpha=alpha, copy_X=True, fit_intercept=True, max_iter=None,
                  normalize=True, solver='auto', tol=tol)

model.submit_fdata(test_fdata,file_name = 'G:/Program/python/contest/score/submit/submit.txt')

for alpha in [100,10,1,0.1,0.01,0.001,0.0001]:
    for tol in [0.001,0.01,0.1,0.4,0.8,1.0]:
        # RR = Sklearn(linear_model.Lasso)
        # model.train_fdata(validation_train_data, RR, alpha=alpha, copy_X=True, fit_intercept=True, max_iter=1000,
        #                   normalize=True, positive=True, precompute='auto', tol=tol,
        #                   warm_start=False)

        RR = Sklearn(linear_model.Ridge)
        model.train_fdata(train_fdata, RR, alpha=alpha, copy_X=True, fit_intercept=True, max_iter=None,
        normalize=True, solver='auto', tol=tol)


        # RR = Sklearn(GradientBoostingRegressor)
        # model.train_fdata(train_fdata, RR, n_estimators=100, learning_rate=0.1,
        #                   max_depth=1, random_state=0, loss='ls')
        print alpha,tol,model.evaluate_fdata(validation_test_data)
