# coding=utf-8
# created by WangZhe on 2014/12/14

import time
import os
import collections

from contest.util.log import logging, train_logging, run_time
from contest.util.conf import setting
import cPickle
import collections
import os
import re
from itertools import product
class BaseModel(object):
    def __init__(self):

        if setting.default_label:
            default_label = setting.default_label
        else:
            default_label = '0'

        self.model_params = {}
        self.model_params['feature_names'] = set()
        self.model_params['predict_params'] = {}
        self.label_file_path = setting.label_file_path
        self.default_label = default_label
        self.map = {}

    def feature_file_search(self,work_dir,feature_list):
        file_list = os.listdir(work_dir)
        is_chosen = [False] * len(file_list)
        for feature_name in feature_list:
            for index,flag in enumerate(is_chosen):
                if not flag and re.search(r'^{0}.txt$'.format(feature_name),file_list[index]):
                    is_chosen[index] = True
        result = [file_list[index][:-4] for index,flag in enumerate(is_chosen) if flag]
        result = list(set(result))
        return result

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

    def cross_validation(self,ftrain,model,scale=0.7,times=1,show_detail=False,**kwargs):
        results = []
        print times
        for i in range(times):
            validation_train_data,validation_test_data = self.divide_data(ftrain,scale)
            result = self.gird_search(validation_train_data,validation_test_data,show_log=show_detail,model=model,**kwargs)
            results.append(result)

        first_result = results[0]
        for result in results[1:]:
            for index,(param,score) in enumerate(result):
                for key,value in score.iteritems():
                    first_result[index][1][key] += value

        for index, (param, score) in enumerate(result):
            for key, value in score.iteritems():
                first_result[index][1][key] /= times

        # self.model.train_params = param

        print len(first_result)
        for index,(param,score) in enumerate(first_result):
            self.model.train_params = param
            self.model_params['score'] = score
            if index == 0:
                self.log_params_name()
            self.log_params_value()
        return first_result










    def gird_search(self,ftrain,ftest,model,show_log=True,**kwargs):
        keys = []
        values = []
        result = []
        is_first = True
        mtrain = self.transform_fdata(ftrain, model.train_data_type)
        mtest = self.transform_fdata(ftest, model.train_data_type)
        for key,value in kwargs.iteritems():
            if isinstance(value,list):
                keys.append(key)
                values.append(value)

        for item in product(*values):
            param = {}
            for index,key in enumerate(keys):
                kwargs[key] = item[index]
                param[key] = item[index]
            self.train_mdata(mtrain,model,**kwargs)

            score = self.evaluate_mdata(mtest,log=False)
            if show_log:
                if is_first:
                    self.log_params_name()
                    is_first = False
                self.log_params_value()
            result.append([param,score])

        return result


    # 模型训练
    @run_time
    def train_fdata(self, fdata, model, **kwargs):
        train_data = self.transform_fdata(fdata, model.train_data_type)
        self.train_mdata(train_data, model, **kwargs)

    # 模型训练
    @run_time
    def train_mdata(self, mdata, model, **kwargs):
        model.train(data=mdata, **kwargs)
        self.model = model
        self.model.train_params = kwargs


    # 对fdata格式的验证集评分
    @run_time
    def evaluate_fdata(self, fdata,log=True, **kwargs):
        mdata = self.transform_fdata(fdata, self.model.train_data_type, is_train=False)
        return self.evaluate_mdata(mdata,log, **kwargs)

    # 对mdata格式的验证集评分
    @run_time
    def evaluate_mdata(self, mdata,log=True, **kwargs):
        uid_label_predict = self.predict_mdata(mdata)
        result = self.handle_predict_result(uid_label_predict, **kwargs)
        self.model_params['score'] = {}
        self.model_params['predict_params'].update(kwargs)

        result = self.get_score(result)
        self.model_params['score'].update(result)
        if log:
            self.log_params_value()
        return result

    # 对fdata格式的测试数据，产生提交文件
    def submit_fdata(self, fdata, **kwargs):
        mdata = self.transform_fdata(fdata, self.model.train_data_type, is_train=False)
        return self.submit_mdata(mdata, **kwargs)

    # 对mdata格式的测试数据，产生提交文件
    def submit_mdata(self, mdata, **kwargs):
        uid_label_predict = self.predict_mdata(mdata)
        result = self.handle_predict_result(uid_label_predict, **kwargs)
        self.save_submit_file(result, save_file_name=kwargs['file_name'])

    # 输入key，label,predict_label,产生提交文件
    @run_time
    def save_submit_file(self, predicts, save_file_name):
        pass

    # 处理得到预测结果（概率）的数据，以方便下一步评分
    def handle_predict_result(self, uid_label_predict, **kwargs):
        result = sorted(uid_label_predict, lambda x, y: cmp(x[2], y[2]), reverse=True)
        result_scale = kwargs['scale']
        result_num = int(result_scale * len(result))
        new_result = []
        for index, (uid, label, predict) in enumerate(result):
            predict = '1' if index < result_num else '0'
            new_result.append((uid, label, predict))

        return new_result


    # 显示训练参数和评分的表头名称
    @run_time
    def log_params_name(self):
        scores = self.model_params['score'].keys()
        predict_params = self.model_params['predict_params'].keys()
        feature_names = ['feature_names']
        train_params = self.model.train_params.keys()
        result_list = scores + ['model']+predict_params + train_params + feature_names
        result_str = "\t".join(result_list)
        train_logging.info(result_str)


    # 显示训练参数和评分的值
    @run_time
    def log_params_value(self):
        scores = self.model_params['score'].values()
        predict_params = self.model_params['predict_params'].values()
        feature_names = self.model_params['feature_names']
        train_params = self.model.train_params.values()
        result_list = scores + [self.model.model_name] + predict_params + train_params + [",".join(feature_names)]
        result_str = "\t".join([str(x) for x in result_list])
        train_logging.info(result_str)

    # 对数据进行评分
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
            return {'P': P, 'R': R, 'F': F}
        except Exception, e:
            logging.info(e)
            return {'P': 0, 'R': 0, 'F': 0}


if __name__ == "__main__":
    BaseModel.feature_file_search()