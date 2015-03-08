# coding=utf-8
# created by WangZhe on 2014/12/25
from contest.util import conf
import platform
import os
if platform.system() == 'Windows':
    conf.set_config_path('G:/Program/python/contest/score/src/setting.py')
else:
    conf.set_config_path('/media/172.16.46.8/wangzhe/contest/score/src/linux_setting.py')

from contest.util.log import logging
if platform.system() == 'Windows':
    logging.setLevel('ERROR')
    # logging.setLevel('DEBUG')

else:
    logging.setLevel('DEBUG')
from sklearn import linear_model
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from src.mycontest import MyContest
from contest.model.sklearn.sk import Sklearn
from contest.model.sklearn.sklearn_pairwise import PairWise
from contest.model.sklearn.ranksvm import RankSVM
import itertools
model = MyContest()


feature_list = [
    # 'uid_term1_score1',
    # 'uid_term2_score1',
    # 'uid_term3_[1-4]',
    'uid_term3_month_3',
    # 'uid_term3_3'
]
if platform.system() == 'Windows':
    work_dir = r'G:/Program/python/contest/score/feature'
else:
    work_dir = r'/media/172.16.46.8/wangzhe/contest/score/feature'

train_fdata = model.features_to_fdata(os.path.join(work_dir,'train'),feature_list)
test_fdata = model.features_to_fdata(os.path.join(work_dir,'test'),feature_list)
columns = list(set(train_fdata.columns).intersection(set(test_fdata.columns)))
train_fdata = train_fdata[columns]
test_fdata = test_fdata[columns]

# validation_train_data,validation_test_data = model.divide_data(train_fdata,0.8)


# RR = Sklearn(linear_model.Ridge)
# model.train_fdata(validation_train_data, RR, alpha=alpha, copy_X=True, fit_intercept=True, max_iter=None,
#                   normalize=True, solver='auto', tol=tol)
# model.submit_fdata(test_fdata,file_name = 'G:/Program/python/contest/score/submit/submit.txt')


# RR = Sklearn(linear_model.Lasso)

# model.gird_search(validation_train_data, validation_test_data,RR, alpha=[0.0001,0.001,0.01,0.1,1,10,100,1000], copy_X=False, fit_intercept=[True,False], max_iter=1000,
#                   normalize=True, positive=True, precompute='auto', tol=[0.0001,0.01,0.1,1,3,5,7,10,100],
#                   warm_start=[True,False])

# print model.cross_validation(train_fdata, RR,scale=0.83,times=4, alpha=[0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000],
#                   copy_X=False, fit_intercept=[True, False], max_iter=1000,
#                   normalize=True, positive=True, precompute='auto', tol=[0.0001, 0.01, 0.1, 1, 3, 5, 7, 10, 100],
#                   warm_start=[True, False])

# print model.cross_validation(train_fdata, RR, scale=0.09, times=4, alpha=[0.01, 10],
#                              copy_X=False, fit_intercept=True, max_iter=1000,
#                              normalize=True, positive=True, precompute='auto',
#                              tol=[0.01, 10],
#                              warm_start=True)

# RR = Sklearn(linear_model.Ridge)
# result =  model.gird_search(validation_train_data,validation_test_data,RR, alpha=[0.01,0.1,1], copy_X=True, fit_intercept=True,
#                   max_iter=None,
#                   normalize=True, solver='auto', tol=[0.1,0.01]
# )


# RR = Sklearn(GradientBoostingRegressor)
# model.gird_search(validation_train_data, validation_test_data,RR, n_estimators=[10,100,1000,5000], learning_rate=0.1,
#                   max_depth=[1,2,3,4,10], random_state=0, loss='ls')

# RR = Sklearn(RandomForestRegressor)
# model.gird_search(validation_train_data, validation_test_data,RR, n_jobs =-1,n_estimators=[10,50,100,150,200,300,500,1000,3000],max_features =['auto',0.01,0.03,0.05,0.07,0.1,0.2,0.3,0.4,0.5],max_depth=[None,1,2,3,4,10,13])

# RR = PairWise(GradientBoostingClassifier)
# model.cross_validation(train_fdata, RR, scale=0.81, times=4,n_estimators=[100,200,400,1000], learning_rate=1.0,
#                        max_depth=[1,2], random_state=0)


# RR = PairWise(LogisticRegression)
RR = RankSVM()
print model.cross_validation(train_fdata, RR, scale=0.3, times=5,show_detail=True,C=[0.1,0.5,1.0,3,5,10,100], loss=['l1','l2'], tol=[0.01,0.1,1])
