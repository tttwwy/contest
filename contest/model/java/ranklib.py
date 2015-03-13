# coding=utf-8
# created by WangZhe on 2014/12/19

import numpy as np
import itertools
import random
import os
from contest.util.conf import setting
from contest.util.log import logging,run_time
import subprocess
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class Ranklib():
    def __init__(self):
        self.train_data_type = 'sklearn_dense'
        self.model_name = 'ranklib'
        self.ranklib_path = 'G:/Program/python/contest/contest/model/java/ranklib/'
        self.ranklib_run = 'java -jar {0}'.format(os.path.join(self.ranklib_path,'bin/RankLib.jar'))
        self.model_path = None

    def __del__(self):
        os.remove(self.model_path)

    @run_time
    def get_random_file(self):
        while True:
            file_name = str(random.randint(0, 1000)) + ".tmp"
            file_path = os.path.join(setting.temp_path, file_name)
            if not os.path.isfile(file_path):
                return file_path

    @run_time
    def transform_data(self,data):
        file_path = self.get_random_file()
        logging.debug('path'+file_path)
        with open(file_path,'w') as f:
            UID,Y,X = data
            for uid,y,x in zip(UID,Y,X):
                x_str = " ".join(["{0}:{1}".format(key+1,value) for key,value in enumerate(x)])
                f.write('{0} qid:111 {1}\n'.format(int(y),x_str))

        return file_path

    @run_time
    def run_ranklib(self,**kwargs):
        params = [self.ranklib_run]
        for key,value in kwargs.iteritems():
            params.append('-{0}'.format(key))
            params.append(str(value))
        logging.debug(" ".join(params))
        logging.debug(params)
        param_str = " ".join(params)
        popen = subprocess.Popen(param_str,shell=True,stdout=subprocess.PIPE)
        print popen.stdout.read()
        output,errors = popen.communicate()

        return str

    @run_time
    def train(self,data,**kwargs):
        if self.model_path:
            os.remove(self.model_path)
        train_data_path = self.transform_data(data)
        with open(train_data_path,'r') as f:
            logging.debug(f.read())
        logging.info('train_data path:{0}'.format(train_data_path))
        self.model_path = self.get_random_file()
        kwargs['train'] = train_data_path
        kwargs['save'] = self.model_path
        self.run_ranklib(**kwargs)



        with open(self.model_path, 'r') as f:
            logging.debug(f.read())


        with open(self.model_path,'r') as f:
            self.model = f.read()
        os.remove(train_data_path)

        logging.info('model path:{0}'.format(self.model_path))


    def predict_value(self,data):
        value = self.model.predict(data)[0]
        return value

    @run_time
    def predict_values(self,x):
        if not os.path.isfile(self.model_path):
            self.model_path = self.get_random_file()
            with open(self.model_path,'w') as f:
                f.write(self.model)

        y = [1] * len(x)
        uid = [111] * len(x)

        predict_data_path = self.transform_data((uid,y,x))
        with open(predict_data_path,'r') as f:
            logging.debug(f.read())
        logging.info('predict_data path:{0}'.format(predict_data_path))

        score_data_path = self.get_random_file()
        run_log = self.run_ranklib(load=self.model_path,rank=predict_data_path,score=score_data_path)
        logging.debug(run_log)
        with open(score_data_path,'r') as f:
            logging.debug(f.read())
        result = []
        with open(score_data_path,'r') as f:
            for line in f:
                line = line.strip().split()
                result.append(float(line[2]))
        logging.info('score_data path:{0}'.format(score_data_path))

        # os.remove(predict_data_path)
        # os.remove(score_data_path)
        return result



if __name__ == "__main__":
    pass
