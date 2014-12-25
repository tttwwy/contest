# coding=utf-8
# created by WangZhe on 2014/12/14

import time
import os
import collections
from contest.util.log import *
from contest.util.conf import setting
import cPickle

class BaseModel():
    def __init__(self):
        self.model_args = {}
        print setting.label_file_path
        self.read_label(setting.label_file_path)

    @run_time
    def read_label(self,file_name):
        self.labels = {}
        for line in open(file_name,'r'):
            line_list = line.strip().split("\t")
            uid = line_list[0]
            key,value = line_list[1].split(":")
            self.labels[key] = value


    @run_time
    def save_model(self, model_file_name):
        model = self.model
        map = self.map
        with open(model_file_name + ".model", "w") as f:
            cPickle.dump(model, f)
        with open(model_file_name + ".index", "w") as f:
            cPickle.dump(map, f)

    @run_time
    def load_model(self, model_file_name):
        logging.info(model_file_name)
        with open(model_file_name + ".model", "r") as f:
            self.model = cPickle.load(f)
        with open(model_file_name + ".index", "r") as f:
            self.map = cPickle.load(f)


    def train_fdata(self, fdata, model, **kwargs):
        train_data = self.transform_fdata(fdata, model.train_type)
        model.train(train_data=train_data, **kwargs)
        self.model = model

    @run_time
    def save_submit_file(self,predicts,save_file_name):
        pass


    @run_time
    def evaluate_fdata(self, fdata, **kwargs):
        uid_label_predict = self.predict_fdata(fdata)
        result = self.handle_predict_result(uid_label_predict, **kwargs)
        return self.score(result)


    def handle_predict_result(self, uid_label_predict, **kwargs):
        result = sorted(uid_label_predict, lambda x, y: cmp(x[2], y[2]), reverse=True)
        result_scale = kwargs['result_scale']
        result_num = result_scale * len(result)
        return result[:result_num]

    @run_time
    def get_score(self, uid_label_predict):
        A = 0
        B = 0
        C = 0

        try:
            for index, (uid, label, predict) in enumerate(uid_label_predict):
                label = str(label)
                if label == predict == '1':
                    A += 1
                elif label != '1' and predict == '1':
                    B += 1
                elif label == '1' and predict != '1':
                    C += 1

            logging.info("{0} {1} {2}".format(A, B, C))
            P = round(float(A) / (A + B), 4)
            R = round(float(A) / (A + C), 4)
            F = round(2 * P * R / (P + R), 4)
            submit_count = A + B
            logging.info("{0} {1} {2}".format(P, R, F))
            return P, R, F
        except Exception, e:
            logging.info(e)
            return 0, 0, 0

if __name__ == "__main__":
    pass