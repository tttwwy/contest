__author__ = 'WangZhe'
# coding=utf-8

import base
import os
import random
from contest.util.log import *
import cPickle
from scipy.sparse import lil_matrix,vstack
import numpy

class SparkModel(base.BaseModel):

    def __init__(self):
        base.BaseModel.__init__(self)
        try:
            from pyspark import SparkContext
            SparkModel.sc = SparkContext(appName="contest")
        except:
            pass

    @run_time
    def features_to_fdata(self,work_dir,*args):
        new_data = self.file_to_data(os.path.join(work_dir,args[0] + ".txt"))
        for feature_name in args[1:]:
            file_name = os.path.join(work_dir,feature_name + ".txt")
            data = self.file_to_data(file_name)
            new_data = new_data + data
        self.feature_names = args

        fdata = self.data_to_fdata(new_data)

        return fdata

    def get_sc(self):
        return SparkModel.sc


    @run_time
    def data_to_fdata(self,data):
        lables = self.labels
        default_lable = self.default_label
        print lables
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

    def divide_data(self,data,scale):
        seed = random.randint(0,10000)
        data = data.map(lambda x:(x[0],x))
        rdd1 = data.sample(False,scale,seed)
        rdd2 = data.subtractByKey(rdd1)
        rdd1 = rdd1.map(lambda x:x[1])
        rdd2 = rdd2.map(lambda x:x[1])
        return rdd1,rdd2

    def file_to_data(self,file_name):
        data = SparkModel.sc.textFile(file_name)
        return data


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


    def sklearn(self, fdata,is_reduce=True):
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
        if not is_reduce:
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
    def transform_fdata(self,fdata,type,is_reduce=True):
        if type == 'sklearn':
            return self.sklearn(fdata,is_reduce)



    @run_time
    def predict_fdata(self,fdata):
        model = self.model
        data = self.transform_fdata(fdata,model.train_data_type,False)
        uid_label_predict = data.map(lambda p:(p[0],p[1],model.predict_value(p[2]))).collect()
        return uid_label_predict





