# coding=utf-8
# created by WangZhe on 2014/12/25
import os
from contest.util import conf
conf.set_config_path('src/setting.py')
print conf.setting.log_path
# from contest.util.log import *
# logging.info("d")
from src.feature import MyExtract
#
feature = MyExtract(work_dir = '',host='ssh.freeshell.ustc.edu.cn',user='root',passwd='root',port=48384,db='score_train')

