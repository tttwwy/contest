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
from contest.model.sklearn.sklearn import Sklearn
from contest.model.sklearn.sklearn_pairwise import PairWise
import itertools
model = MyContest()


feature_list = [
    'uid_term[0-9]_score[1-3]',
    # 'uid_term3_[1-4]'
    # '.*',
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


RR = PairWise(LogisticRegression)
model.train_fdata(train_fdata, RR, C=1, penalty='l1', tol=0.01)
model.submit_fdata(test_fdata,file_name = 'G:/Program/python/contest/score/submit/submit.txt')

