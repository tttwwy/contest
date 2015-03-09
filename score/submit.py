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
    # logging.setLevel('ERROR')
    logging.setLevel('DEBUG')

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
import numpy as np
import itertools
model = MyContest()


feature_list = [
    'uid_term1_score1',
    'uid_term2_score1',
    'uid_term3_[1-4]',
    'uid_term3_location_[1-9]',
    'uid_term3_category_2',
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



#
# RR = PairWise(LogisticRegression)
# model.train_fdata(train_fdata, RR, C=0.003, penalty='l1', tol=0.01)


RR = PairWise(LogisticRegression)

uid1,y1,x1 = model.transform_fdata(train_fdata,RR.train_data_type)
uid2,y2,x2 = model.transform_fdata(test_fdata,RR.train_data_type)
x1_num = x1.shape[0]
x2_num = x2.shape[0]
x = np.vstack([x1,x2,x2,x2,x2])
from sklearn.decomposition import PCA
pca = PCA(30)
pca.fit(x)
print pca.explained_variance_ratio_
x = pca.fit_transform(x)
x1 = x[:x1_num]
x2 = x[x1_num:x1_num+x2_num]
model.train_mdata((uid1,y1,x1), RR, C=8, penalty='l1', tol=0.01)

print x.shape
x = pca.fit_transform(x)
print x.shape
model.submit_mdata(mdata = [uid2,y2,x2],file_name = 'G:/Program/python/contest/score/submit/submit.txt')
# model.train_fdata(train_fdata, RR, C=0.1, loss='l2', tol=0.1)

# RR = PairWise(GradientBoostingClassifier)
# model.train_fdata(train_fdata, RR,n_estimators=100, learning_rate=1.0,
#                        max_depth = 1, random_state = 0)

# RR = PairWise(RandomForestClassifier)
# model.train_fdata(train_fdata, RR, n_estimators=100, max_depth=15,
#                        min_samples_split=1, random_state=0,n_jobs=4)
#
# model.submit_mdata(test_fdata,file_name = 'G:/Program/python/contest/score/submit/submit.txt')

