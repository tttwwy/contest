__author__ = 'WangZhe'
# coding=utf-8


import os
import random
from contest.util.log import logging,train_log,run_time
import base
import cPickle
from scipy.sparse import lil_matrix,vstack
import numpy
import pandas as pd

class GeneralModel(base.BaseModel):

    def __init__(self):
        super(GeneralModel,self).__init__()


    @run_time
    def read_labels(self, file_name):
        datas = []
        with open(file_name, 'r') as f:
            for line in f:
                data = {}
                line = line.strip().split("\t")
                uid = line[0]
                features = line[1:]
                data['uid'] = uid
                for item in features:
                    feature_name, feature_value = item.split(":")
                    data['label'] = float(feature_value)
                datas.append(data)

        return pd.DataFrame(datas)

    @run_time
    def features_to_fdata(self, work_dir, file_list):
        file_list = self.feature_file_search(work_dir,file_list)
        new_data = self.file_to_data(os.path.join(work_dir, file_list[0] + ".txt"), file_list[0]   )
        for feature_name in file_list[1:]:
            file_name = os.path.join(work_dir, feature_name + ".txt")
            data = self.file_to_data(file_name,feature_name)
            new_data = pd.merge(new_data,data,how='outer',on='uid')

        self.feature_names = file_list
        label_data = self.read_labels(self.label_file_path)
        new_data = pd.merge(new_data, label_data, how='inner', on='uid')
        new_data = new_data.fillna(0.0)
        self.model_params['feature_names'].update(file_list)
        return new_data

    def file_to_data(self, file_name,feature_name):
        datas = []
        with open(file_name,'r') as f:
            for line in f:
                data = {}
                line = line.strip().split("\t")
                uid = line[0]
                features = line[1:]
                data['uid'] = uid
                for item in features:
                    key,value = item.split(":")
                    if key:
                        key = "_" + key
                    data[feature_name + key] = float(value)
                datas.append(data)

        return pd.DataFrame(datas)

    def combine_data(self,fdata1,fdata2):
        return pd.merge(fdata1,fdata2,how='outer',on='uid')


    @run_time
    def divide_data(self,data,scale_list):
        if isinstance(scale_list,float):
            scale_list = [scale_list,1-scale_list]
        result = []
        total_row = data.shape[0]
        remain = data
        for scale in scale_list:
            num = int(total_row * scale)
            rows = random.sample(remain.index,num)
            result.append(remain.ix[rows])
            remain = remain.drop(rows)
        return result



    @run_time
    def sklearn_dense(self, fdata, is_train=True):
        uid_matrix = fdata['uid'].values
        y_matrix = fdata['label'].values
        x_matrix = fdata[fdata.columns.drop(['uid','label'])].values
        # from sklearn.preprocessing import StandardScaler
        # x_matrix = StandardScaler().fit_transform(x_matrix)

        return uid_matrix, y_matrix, x_matrix

    @run_time
    def sklearn_sparse(self, fdata,is_train=True):
        uid_matrix = fdata['uid'].values
        y_matrix = fdata['label'].values
        x_matrix = fdata[fdata.columns.drop(['uid','label'])].values
        # from sklearn.preprocessing import StandardScaler
        # x_matrix = StandardScaler().fit_transform(x_matrix)
        return uid_matrix, y_matrix, x_matrix

    @run_time
    def transform_fdata(self,fdata,func_name,is_train=True):
        transform_func = getattr(self,func_name)
        return transform_func(fdata,is_train)

    @run_time
    def predict_mdata(self,mdata):
        model = self.model
        uid_matrix, y_matrix, x_matrix = mdata
        predict_matrix = model.predict_values(x_matrix)
        return zip(uid_matrix,y_matrix,predict_matrix)


    @run_time
    def predict_fdata(self,fdata):
        data = self.transform_fdata(fdata,self.model.train_data_type,False)
        return self.predict_mdata(data)






