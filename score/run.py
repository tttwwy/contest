# coding=utf-8
# created by WangZhe on 2014/12/25
from contest.util import conf
conf.set_config_path('src/setting.py')
print conf.setting.log_path
from src.mycontest import MyContest
from contest.model.sklearn.RidgeRegression import RidgeRegression

model = MyContest()
feature_list = ['uid_term1_1','uid_term2_1']
train_fdata = model.features_to_fdata('G:/Program/python/contest/score/feature/train',*feature_list)
test_fdata = model.features_to_fdata('G:/Program/python/contest/score/feature/test',*feature_list)
validation_train_data,validation_test_data = model.divide_data(train_fdata,0.005)

print validation_test_data
RR = RidgeRegression()

# model.train_fdata(train_fdata,RR, alpha=0.5, copy_X=True, fit_intercept=True, max_iter=None,
#                   normalize=True, solver='auto', tol=0.001)
# model.submit_fdata(test_fdata,file_name = 'G:/Program/python/contest/score/submit/submit.txt')


model.train_fdata(validation_train_data, RR, alpha=0.5, copy_X=True, fit_intercept=True, max_iter=None,
                  normalize=True, solver='auto', tol=0.001)
model.evaluate_fdata(validation_test_data)
