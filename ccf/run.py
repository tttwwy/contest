# coding=utf-8
# created by WangZhe on 2014/12/25
import os
import sys
sys.path.append('src')
# os.environ.setdefault("CONTEST_SETTINGS_MODULE", "src.setting")

from contest.util.conf import *
from src.manage import Work
from contest.model.sklearn.LogisticRegression import LR
if __name__ == "__main__":
    work = Work()
    feature_lists = [
        ['us00']
    ]
    for feature_list in feature_lists:
        ftrain_data = work.features_to_fdata("/home/wangzhe/ccf/data/feature/train/", *feature_list)
        # ftrain_data = ftrain_data.sample(False,0.01,3)
        ftest_data = work.features_to_fdata("/home/wangzhe/ccf/data/feature/validation/", *feature_list)

        model = LR()
        work.train_fdata(fdata=ftrain_data,
                         model=model,
                          C=0.2, intercept_scaling=1,
                          dual=False,
                          fit_intercept=False,
                          penalty='l1',
                          tol=0.1)
        for result_scale in [0, 0.0005, 0.0006, 0.006, 0.007, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01]:
            print work.evaluate_fdata(fdata=ftest_data, result_scale=result_scale)


