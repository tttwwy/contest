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
import numpy as np
from contest.util.log import train_logging
import pandas as pd
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
from contest.model.java.ranklib import Ranklib
import itertools
model = MyContest()

#
feature_list = [

    'uid_term1_score1',
    'uid_term2_score1',
    'uid_term3_[1-4]',
    'uid_term3_location_[1-9]',
    # 'uid_term3_category_2',




    # 'uid_term1_score1',
    # 'uid_term2_score1',
    # 'uid_term[2-3]_[1-5]',
    # 'uid_term[2-3]_month_[1-4]',
    # 'uid_term[2-3]_location_(1|3)',
    # 'uid_term[2-3]_month_location_[1-9]',
    # # 'uid_term3_category_1',
    # # 'uid_term3_category_2',
    # # 'uid_term3_book_1',
    # # '.*'
]

if platform.system() == 'Windows':
    work_dir = r'G:/Program/python/contest/score/feature'
else:
    work_dir = r'/media/172.16.46.8/wangzhe/contest/score/feature'

train_fdata = model.features_to_fdata(os.path.join(work_dir,'train'),feature_list)
print len(train_fdata + train_fdata)
test_fdata = model.features_to_fdata(os.path.join(work_dir,'test'),feature_list)
columns = list(set(train_fdata.columns).intersection(set(test_fdata.columns)))
train_fdata = train_fdata[columns]
test_fdata = test_fdata[columns]
# validation_train,validation_test = model.divide_data(train_fdata,0.7)
print train_fdata.shape
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


RR = PairWise(LogisticRegression)
# RR = Ranklib()
# uid,y,x = model.transform_fdata(train_fdata,RR.train_data_type)
# from sklearn.decomposition import PCA
# pca = PCA(0.9)
#
# pca.fit(x)
# print pca.explained_variance_ratio_
#
#
# model.cross_validation(train_fdata, RR, times=3,show_detail=True,C=[8], penalty=['l1'], tol=[0.01])
# print x.shape
# x = pca.fit_transform(x)
# print x.shape
# model.cross_validation([uid,y,x], RR, times=6,show_detail=False,C=[8], penalty=['l1'], tol=[0.01])


# model.cross_validation(train_fdata,RR,times=4,show_detail=True,ranker=6,gmax=402,metric2t='NDCG@10',tree=200,leaf=30)



#
# sort_index = np.argsort(-RR.model.coef_)
#
# columns = list(train_fdata.columns.drop(['uid','label'])[sort_index][0][:100])
# # for index in sort_index:
# #     print index
# #     train_logging.info('{0}:{1}'.format(columns[index],RR.model.coef_[0][index]))
# # for index,column in enumerate(columns):
# #     train_logging.info('{0}:{1}'.format(column,RR.model.coef_[0][index]))
#
# columns = columns + ['uid','label']
# # print columns
# # columns = [x for x in columns] +  ['uid','label']
# # print columns
#
#
# train_fdata = train_fdata[columns]
# model.cross_validation(train_fdata, RR, times=4,show_detail=False,C=[0.01], penalty=['l1'], tol=[0.01])
#
# # for index in range(len(result)):
# #     train_logging.info("{0}:{1}".format(result[index],RR.model.coef_[index]))
# # model.train_fdata(train_fdata,RR,C=0.01,tol=0.01,penalty='l1')
#
# # print RR.model.coef_
# # sort_index  = np.argsort(RR.model.coef_)
# #
# # print train_fdata.columns[]
#
#
RR = PairWise(svm.SVC)
model.cross_validation(train_fdata, RR, times=3,show_detail=True, C=[1,8,100], cache_size=200, class_weight=None, coef0=[0], degree=3,
                       gamma=[0], kernel='rbf', max_iter=[-1], probability=False,
                       shrinking=True, tol=[0.1,0.01], verbose=False)
# #
# # RR = PairWise(GradientBoostingClassifier)
# # model.cross_validation(train_fdata, RR, scale=0.73, times=3,show_detail=False, n_estimators=[100,300,500,1000], learning_rate=1.0,
# #                        max_depth = 1, random_state = 0
# # )
#
# # RR = PairWise(RandomForestClassifier)
# # model.cross_validation(train_fdata, RR, scale=0.73, times=2,show_detail=False,n_estimators=[20,50,100], max_depth=[5,10,20],
# #                       min_samples_split=1, random_state=0,n_jobs=20,)
#
#
#
# # RR = RankSVM()
# # model.cross_validation(train_fdata, RR, scale=0.73, times=3,show_detail=False,C=[1e-6,1e-5,1e-4,1e-3,], loss=['l1'], tol=[0.01,0.1,1])
