__author__ = 'WangZhe'
# coding=utf-8

import base
import os
import random
from contest.util.log import logging,train_log,run_time

import cPickle
from scipy.sparse import lil_matrix,vstack
import numpy
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.linalg import SparseVector

class SparkModel(base.BaseModel):

    def __init__(self):
        # base.BaseModel.__init__(self)
        super(SparkModel,self).__init__()
        try:
            from pyspark import SparkContext
            SparkModel.sc = SparkContext(appName="contest")
        except:
            pass


        # 读取label，方便为训练数据和测试集打标签

    @run_time
    def read_labels(self, file_name):
        labels = {}
        for line in open(file_name, 'r'):
            line_list = line.strip().split("\t")
            uid = line_list[0]
            key, value = line_list[1].split(":")
            labels[key] = value
            return labels

    def get_sc(self):
        return SparkModel.sc


# 读取特征文件，转化成框架的标准特征文件fdata

    @run_time
    def features_to_fdata(self, work_dir, file_list):
        file_list = self.feature_file_search(work_dir,file_list)
        new_data = SparkModel.sc.textFile(os.path.join(work_dir, file_list[0] + ".txt"))
        for feature_name in file_list[1:]:
            file_name = os.path.join(work_dir, feature_name + ".txt")
            data = SparkModel.sc.textFile(file_name)
            new_data = new_data + data

        self.feature_names = file_list

        fdata = self.data_to_fdata(new_data)
        self.model_params['feature_names'].update(file_list)
        return fdata

    @run_time
    def data_to_fdata(self,data):
        lables = self.read_labels(self.label_file_path)
        default_lable = self.default_label
        labels_broadcast = SparkModel.sc.broadcast((lables,default_lable))

        def handle(x):
            line = x.split("\t")
            return line[0],line[1:]

        def handle2(x):
            uid,values = x
            labels,default_label = labels_broadcast.value
            label = labels.get(uid,default_label)
            value_map = {}
            for item in values:
                key,value = item.split(":")
                value_map[key] = float(value)
            return (uid,label,value_map)

        result = data.map(handle).reduceByKey(lambda x,y:list(x)+list(y))
        fdata = result.map(handle2)
        return fdata

    @run_time
    def divide_data(self,data,scale_list):
        if isinstance(scale_list,float):
            scale_list = [scale_list,1-scale_list]
        # seed = random.randint(0,10000)
        # data = data.map(lambda x:(x[0],x))
        # rdd1 = data.sample(False,scale,seed)
        # rdd2 = data.subtractByKey(rdd1)
        # rdd1 = rdd1.map(lambda x:x[1])
        # rdd2 = rdd2.map(lambda x:x[1])
        return data.randomSplit(scale_list)


    @run_time
    def fdata_filter(self,fdata,f):
        filter_data = fdata.filter(f)
        return filter_data

    @run_time
    def get_fdata_map(self,fdata):
        if self.map:
            return self.map
        feature_data = fdata.flatMap(lambda x:x[2].keys())
        index = 0
        new_map = {}
        for feature_name in feature_data.distinct().collect():
            new_map[feature_name] = index
            index += 1
        self.map = new_map
        return new_map

    @run_time
    def map_fdata(self,fdata):
        map = self.get_fdata_map(fdata)
        broadcast_map = SparkModel.sc.broadcast(map)
        broadcast_size = SparkModel.sc.broadcast(len(map))
        def handle(line):
            uid,label,values = line
            new_values = {}
            for key,value in values.iteritems():
                if key in broadcast_map.value:
                    new_values[broadcast_map.value[key]] = value
            return (uid,label,new_values)
        mdata = fdata.map(handle)
        return mdata


    @run_time
    def balance_data(self,data1,data2,balance_scale=1.0):
        data1_count = data1.count()
        data2_count = data2.count()
        logging.info(balance_scale)
        max_data,min_data = (data1,data2) if data1_count > data2_count else (data2,data1)
        if balance_scale <= 1:
            scale = int(max(data1_count,data2_count)/min(data1_count,data2_count)) - 1
            new_min_data = min_data.flatMap(lambda x:[x] * int(scale*balance_scale))
            return max_data + new_min_data

        else:
            scale = min(data1_count,data2_count)*balance_scale*1.0/(max(data1_count,data2_count))
            seed = random.randint(0,10000)
            new_max_data = max_data.sample(False,scale,seed)
            return min_data + new_max_data

    @run_time
    def mllib(self,fdata,is_train=True):
        map = self.get_fdata_map(fdata)
        broadcast_map = self.get_sc().broadcast(map)
        broadcast_size = self.get_sc().broadcast(len(map))
        def train_data(line):
            uid,label,values = line
            new_values = {}
            for key,value in values.iteritems():
                if key in broadcast_map.value:
                    new_values[broadcast_map.value[key]] = value
            return LabeledPoint(label,SparseVector(broadcast_size.value,new_values))

        def test_data(line):
            uid,label,values = line
            new_values = {}
            for key,value in values.iteritems():
                if key in broadcast_map.value:
                    new_values[broadcast_map.value[key]] = value
            return (uid,label,SparseVector(broadcast_size.value,new_values))

        if is_train:
            data = fdata.map(train_data)
        else:
            data = fdata.map(test_data)
        return data

    @run_time
    def sklearn_dense(self, fdata, is_train=True):
        map = self.get_fdata_map(fdata)

        broadcast_map = self.get_sc().broadcast(map)
        broadcast_size = self.get_sc().broadcast(len(map))

        def map(line):
            uid, y, values = line
            x = lil_matrix((1, broadcast_size.value), dtype=float)
            for key, value in values.iteritems():
                if key in broadcast_map.value:
                    x[0, broadcast_map.value[key]] = value
            x = x.tocsr()
            return (uid, y, x)

        sparse_data = fdata.map(map)
        if not is_train:
            return sparse_data

        logging.info("reduce start")
        uid_list = []
        y_list = []
        x_list = []
        for uid, y, x in sparse_data.collect():
            uid_list.append(uid)
            y_list.append(y)
            x_list.append(x)

        logging.info("reduce end")

        x_matrix = vstack(x_list)
        uid_matrix = numpy.array(uid_list)
        y_matrix = numpy.array(y_list)

        return uid_matrix, y_matrix, x_matrix

    @run_time
    def sklearn_sparse(self, fdata,is_train=True):
        map = self.get_fdata_map(fdata)

        broadcast_map = self.get_sc().broadcast(map)
        broadcast_size = self.get_sc().broadcast(len(map))

        def map(line):
            uid, y, values = line
            x = lil_matrix((1, broadcast_size.value), dtype=float)
            for key, value in values.iteritems():
                if key in broadcast_map.value:
                    x[0, broadcast_map.value[key]] = value
            x = x.tocsr()
            return (uid, y, x)

        sparse_data = fdata.map(map)
        if not is_train:
            return sparse_data

        logging.info("reduce start")
        uid_list = []
        y_list = []
        x_list = []
        for uid, y, x in sparse_data.collect():
            uid_list.append(uid)
            y_list.append(y)
            x_list.append(x)

        logging.info("reduce end")

        x_matrix = vstack(x_list)
        uid_matrix = numpy.array(uid_list)
        y_matrix = numpy.array(y_list)

        return uid_matrix, y_matrix, x_matrix

    @run_time
    def transform_fdata(self,fdata,func_name,is_train=True):
        func = None
        # exec 'func = self.{0}'.format(func_name)
        transform_func = getattr(self,func_name)
        return transform_func(fdata,is_train)
        # if func_name == 'sklearn':
        #     return self.sklearn_sparse(fdata,is_train)
        # elif func_name == 'mllib':
        #     return self.mllib(fdata,is_train=is_train)

    @run_time
    def predict_mdata(self,mdata):
        model = self.model
        uid_label_predict = mdata.map(lambda p:(p[0],p[1],model.predict_value(p[2]))).collect()
        return uid_label_predict


    @run_time
    def predict_fdata(self,fdata):
        data = self.transform_fdata(fdata,self.model.train_data_type,False)
        return self.predict_mdata(data)






