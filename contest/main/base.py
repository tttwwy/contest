# coding=utf-8
# created by WangZhe on 2014/12/14

import time
import os
import collections


from contest.util.log import logging,train_log,run_time
from contest.util.conf import setting
import cPickle
import collections

class BaseModel():
    def __init__(self):
        self.model_args = {}
        print setting.label_file_path
        if setting.default_label:
            default_label = setting.default_label
        else:
            default_label = '0'
        self.init_labels(setting.label_file_path,default_label)
        self.default_label = default_label
        self.map = {}


    def init_labels(self,file_name,default_label='0'):
        # def default():
        #     return '0'
        # self.labels = collections.defaultdict(default)
        self.labels = self.read_labels(file_name)

    @run_time
    def read_labels(self,file_name):
        labels = {}
        for line in open(file_name,'r'):
            line_list = line.strip().split("\t")
            uid = line_list[0]
            key,value = line_list[1].split(":")
            labels[key] = value
            return labels


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

    @run_time
    def train_fdata(self, fdata, model, **kwargs):
        train_data = self.transform_fdata(fdata, model.train_data_type)
        model.train_fdata(fdata=train_data, **kwargs)
        self.model = model

    @run_time
    def save_submit_file(self,predicts,save_file_name):
        pass


    @run_time
    def evaluate_fdata(self, fdata, **kwargs):
        uid_label_predict = self.predict_fdata(fdata)
        result = self.handle_predict_result(uid_label_predict, **kwargs)
        return self.get_score(result)


    def handle_predict_result(self, uid_label_predict, **kwargs):
        result = sorted(uid_label_predict, lambda x, y: cmp(x[2], y[2]), reverse=True)
        result_scale = kwargs['result_scale']
        result_num = int(result_scale * len(result))
        print result[:100]
        new_result = []
        for index,(uid,label,predict) in enumerate(result):
            predict = '1' if index < result_num else '0'
            new_result.append((uid,label,predict))
        #
        #
        # print result[-100:]
        return new_result

    @run_time
    def get_score(self, uid_label_predict):
        # print uid_label_predict
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