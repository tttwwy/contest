# coding=utf-8
# created by WangZhe on 2014/12/25
from contest.util import conf
import platform
import os

if platform.system() == 'Windows':
    conf.set_config_path('G:/Program/python/contest/taobao/src/setting.py')
else:
    conf.set_config_path('/media/172.16.46.8/wangzhe/contest/taobao/src/linux_setting.py')

from contest.util.log import logging

if platform.system() == 'Windows':
    logging.setLevel('DEBUG')
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
# from mycontest import MyContest
from src.mycontest import MyContest
from contest.model.sklearn.sk import Sklearn

from contest.model.sklearn.LogisticRegression import LR
from contest.model.sklearn.sklearn_pairwise import PairWise
from contest.model.sklearn.ranksvm import RankSVM
from contest.model.java.ranklib import Ranklib
import itertools

model = MyContest()
def transform_data(data,uid):
    data = pd.merge(data, df2_2, how='inner')
    uid_bid = ['{0}_{1}'.format(x, y) for x, y in zip(data['uid'], data['bid'])]
    new_data = data.drop(['uid', 'bid'], axis=1)
    new_data['uid'] = uid_bid
    return new_data

feature_list = [

    # 'uid_(buy|visit)_(1|2|3|5|7|10)_[1]',
    # 'bid_(buy|visit)_(1|2|3|5|7|10)_[1]',
    # 'uid_bid_(buy|visit)_(1|2|3|5|7|10)_[1]',
    'uid_(buy|visit)_(3|5)_[1]',
    'bid_(buy|visit)_(1|2)_[1]',
    'uid_bid_(buy|visit)_(1|2)_[1]',
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
train_table_names = ['train_1128_1211',
                     'train_1121_1204',
                     'train_1118_1127',
                     'test_1205_1218']
table_name = 'train_1118_1127'
work_dir = os.path.join(conf.setting.feature_path, table_name)
label_path = os.path.join(conf.setting.feature_path, table_name, 'label.txt')
print label_path
train_fdata = model.features_to_fdata(work_dir, feature_list, label_path)
train_fdata = transform_data(train_fdata)

table_name = 'train_1121_1204'
work_dir = os.path.join(conf.setting.feature_path, table_name)
label_path = os.path.join(conf.setting.feature_path, table_name, 'label.txt')
test_fdata = model.features_to_fdata(work_dir, feature_list, label_path)
test_fdata = transform_data(test_fdata)




LR = Sklearn(linear_model.LogisticRegression)
model.train_data(train_fdata,
                 LR,
                 penalty="l2",
                 max_iter=100
                 )


for scale in [0.008,0.01,0.02,0.03,0.05]:
    model.evaluate_data(test_fdata,scale=scale)
