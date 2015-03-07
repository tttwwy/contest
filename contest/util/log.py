# coding=utf-8
# created by WangZhe on 2014/11/2
import time
import sys
from contest.util import conf
import os

from timeit import timeit as timeit

colors = {
"black": 0,
"red": 1,
"green": 2,
"yellow": 3,
"blue": 4,
"purple": 5,
"cyan": 6,
"gray": 7
}


def set_log(log_path):
    import logging
    import logging.config
    import logging.handlers
    gLogger = logging.getLogger('log')

    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] file:%(filename)s line:%(lineno)d func:%(message)s','%Y-%m-%d %H:%M:%S')
    myhandler = logging.StreamHandler(sys.stdout)
    myhandler.setFormatter(formatter)
    gLogger.addHandler(myhandler)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] file:%(filename)s line:%(lineno)d func:%(message)s','%Y-%m-%d %H:%M:%S')
    myhandler = logging.handlers.RotatingFileHandler(log_path)
    myhandler.setFormatter(formatter)
    gLogger.addHandler(myhandler)
    gLogger.setLevel(logging.INFO)
    return gLogger

def set_train_log(log_path):
    import logging
    import logging.config
    import logging.handlers

    gLogger = logging.getLogger('train')

    formatter = logging.Formatter('%(message)s')
    myhandler = logging.StreamHandler(sys.stdout)
    myhandler.setFormatter(formatter)
    gLogger.addHandler(myhandler)
    formatter = logging.Formatter('%(message)s')
    myhandler = logging.handlers.RotatingFileHandler(log_path)
    myhandler.setFormatter(formatter)
    gLogger.addHandler(myhandler)
    gLogger.setLevel(logging.INFO)
    return gLogger

# def train_log(str):
#     log_file = conf.setting.train_log_path
#     with open(log_file,'a') as f:
#         f.write("{0}\n".format(str))
#         f.flush()
#     logging.info(str)
#     print str

logging = set_log(conf.setting.log_path)
train_logging = set_train_log(conf.setting.train_log_path)



#     logging.basicConfig(level=mylog.DEBUG,
#                     format=' %(asctime)s %(filename)s line:%(lineno)d %(funcName)s :%(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     filename='/home/wangzhe/ccf/contest/log',
#                     filemode='a')
#
# # file = open("/home/wangzhe/ccf/contest/log",'a')
# def info(str,color="red"):
#     # cur_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#     # file.write("\033[0;3{0}m{1} {2}\033[0m".format(colors[color],cur_time,str))
#     mylog.info(str)



def run_time(func):

    def new_func(*args, **args2):
        start = time.time()
        logging.info("{0}:start".format(func.__name__))
        back = func(*args, **args2)
        end = time.time()
        logging.info("{0}:end".format(func.__name__))
        logging.info("{0}: {1} s".format(func.__name__,end - start))
        return back

    return new_func

if __name__ == "__main__":
    pass
