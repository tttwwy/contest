# coding=utf-8
# created by WangZhe on 2014/12/25
import os
import sys
os.environ.setdefault("CONTEST_SETTINGS_MODULE", "src.setting")

from contest.util.conf import *
from src.manage import Work
# from contest.model.sklearn.LogisticRegression import LR as SklearnLR
from contest.model.mllib.LogisticRegression import LR
from contest.model.sklearn.RandomForestClassifier import RF

if __name__ == "__main__":
    work = Work()
    feature_lists = [
        ['us00']
    ]
    for feature_list in feature_lists:
        ftrain_data = work.features_to_fdata("ccf/data/train/", *feature_list)
        # ftrain_data = ftrain_data.sample(False,0.01,3)
        ftest_data = work.features_to_fdata("ccf/data/validation/", *feature_list)

        LR = LR()
        RF = RF()
        # work.train_fdata(fdata=ftrain_data,
        #                  model=model,
        #                   C=0.2, intercept_scaling=1,
        #                   duallsFalse,
        #                   fit_intercept=False,
        #                   penalty='l1',
        #                   tol=0.1)

        # work.train_fdata(fdata=ftrain_data,
        #                  model=model,
        #                  iterations=1000009,
        #                  regParam=0.0001,
        #                  regType="l1",
        #                  intercept=False,
        #                  corrections=10,
        #                  tolerance=0.001)
        work.train_fdata(fdata=ftrain_data,
                         model=RF,
                         n_estimators=10,
                         criterion='gini',
                         max_depth=None,
                         min_samples_split=2,
                         min_samples_leaf=1,
                         max_features='auto',
                         max_leaf_nodes=None,
                         bootstrap=True,
                         oob_score=False,
                         n_jobs=12,
                         random_state=None,
                         verbose=0,
                         min_density=None,
                         compute_importances=None)


        for result_scale in [0, 0.0005, 0.0006, 0.006, 0.007, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01]:
            print work.evaluate_fdata(fdata=ftest_data, result_scale=result_scale)


