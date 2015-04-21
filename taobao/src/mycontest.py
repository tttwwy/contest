# coding=utf-8
# created by WangZhe on 2014/12/23


from contest.main.general import GeneralModel
from contest.util.conf import setting
from contest.util.log import logging,train_logging,run_time
import pandas as pd
import os
class MyContest(GeneralModel):
    def __init__(self):
        super(GeneralModel,self).__init__()




    @run_time
    def features_to_fdata(self, work_dir, file_list,label_path):
        self.model_params['feature_names'].update(file_list)
        file_list = self.feature_file_search(work_dir, file_list)
        logging.error(file_list)


        # datas = {'uid':None,'bid':None,'uid_bid':None}
        datas = {}
        for feature_name in file_list:
            feature_list = feature_name.split("_")
            file_name = os.path.join(work_dir, feature_name + ".txt")
            data = self.file_to_data(file_name, feature_name)

            # print 'data',data
            if feature_list[0] == 'uid' and feature_list[1] == 'bid':
                data_type = 'uid_bid'
            else:
                data_type = feature_list[0]

            logging.error(data_type)
            if data_type not in datas:
                datas[data_type] = data
            else:
                logging.error('begin to merge')
                datas[data_type] = pd.merge(datas[data_type], data, how='outer')

        if 'uid_bid' not in datas:
            if datas['uid']:
                return datas['uid']
            if datas['bid']:
                return datas['bid']
            return None
        else:
            new_data = datas['uid_bid']
            if 'uid' in datas:
                new_data = pd.merge(new_data, datas['uid'], how='outer',on='uid')
            if 'bid' in datas:
                new_data = pd.merge(new_data, datas['bid'], how='outer', on='bid')

        label_data = self.file_to_data(label_path,'label')
        new_data = pd.merge(new_data, label_data, how='outer')
        new_data = new_data.fillna({'label':0})
        new_data = new_data.fillna(0.0)
        return new_data




    def file_to_data(self, file_name, feature_name):
        datas = []
        if feature_name == 'label':
            head = ['uid', 'bid']
        else:
            head = [x for x in feature_name.split("_") if x in ['uid','bid','category']]
        print file_name
        with open(file_name, 'r') as f:
            for line in f:
                data = {}
                line = line.strip().split("\t")
                for head_name,item in zip(head,line[:-1]):
                    data[head_name] = item

                data[feature_name] = float(line[-1])
                datas.append(data)
        return pd.DataFrame(datas)



    def save_submit_file(self, predicts, save_file_name):
        with open(save_file_name,'w') as f:
            f.write('user_id,item_id\n')
            for item,label,predict in predicts:
                if predict == '1':
                    uid,bid = item.split("_")
                    f.write('{0},{1}\n'.format(uid,bid))
