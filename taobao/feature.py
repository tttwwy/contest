# coding=utf-8
# created by WangZhe on 2014/12/25
import os
from contest.util import conf
import platform
if platform.system() == 'Windows':
    conf.set_config_path('G:/Program/python/contest/taobao/src/setting.py')
else:
    conf.set_config_path('/media/172.16.46.8/wangzhe/contest/taobao/src/linux_setting.py')

from contest.util.log import logging

from src.myfeature import MyExtract
import os

train_table_names = ['train_1128_1211',
               'train_1121_1204',
               'train_1118_1127',
               'test_1205_1218']

label_table_names = [
    ('target_1128','train_1118_1127'),
    ( 'target_1205','train_1121_1204'),
    ('target_1212','train_1128_1211')
]
feature = MyExtract(work_dir=os.path.join(conf.setting.feature_path, 'train_item'), host='114.214.166.162', user='tianchi', passwd='tianchi', port=3435, db='mobile')
feature.extract('bid',
                '''
                select distinct(item_id),1 from train_item
                ''')

for table_name,train_table_name in label_table_names:
    work_dir = os.path.join(conf.setting.feature_path, train_table_name)
    # if not os.path.exists(work_dir):
    #     os.makedirs(work_dir)
    feature = MyExtract(work_dir=work_dir, host='114.214.166.162', user='tianchi', passwd='tianchi', port=3435, db='mobile')
    feature.extract('label',
                    '''SELECT user_id,item_id,1 FROM {0} where behavior_type = 4 group by user_id,item_id;'''.format(table_name))


for table_name in train_table_names:
    work_dir = os.path.join(conf.setting.feature_path,table_name)
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)

    feature = MyExtract(work_dir=work_dir, host='114.214.166.162', user='tianchi', passwd='tianchi', port=3435, db='mobile')
    def time_action_feature(feature_name,time_list,action_list,sql):
        logging.info('{0} start'.format(feature_name))
        sql = sql.lower().split()
        sql = " ".join(sql)
        sql = sql.replace('train_user',table_name)
        time_replace = ('1', '2', '3', '5', '7', '10')
        action_replace = {'visit':'1', 'keep':'2', 'car':'3', 'buy':'4'}
        if 'action' in action_list:
            action_list.remove('action')
            action_list.extend(action_replace.keys())
        if 'time' in time_list:
            time_list.remove('time')
            time_list.extend(time_replace)
        for time in time_list:
            for action in action_list:
                new_feature_name = feature_name
                new_sql = sql

                if action == 'all_action':
                    new_feature_name = feature_name.replace('action', 'all')
                    new_sql = sql.replace('behavior_type = 4', 'behavior_type != -1')

                elif action in ('visit','keep','car','buy'):
                    new_feature_name = feature_name.replace('action', action)
                    new_sql = sql.replace('behavior_type = 4', 'behavior_type = {0}'.format(action_replace[action]))


                if time == 'all_time':
                    new_feature_name = new_feature_name.replace('time','all')
                    time = '1000'
                else:
                    new_feature_name = new_feature_name.replace('time',time)
                new_sql = new_sql.replace('day < 1','day < {0}'.format(time))
                feature.extract(new_feature_name,new_sql)

        logging.info('{0} end'.format(feature_name))

    #uid特征
    time_action_feature(
        'uid_action_time_1',
        ['time'],
        ['action'],
        '''SELECT user_id, COUNT(DISTINCT DAY) FROM train_user WHERE behavior_type = 4 AND DAY < 1 GROUP BY user_id''')

    time_action_feature(
        'uid_action_time_2',
        ['time'],
        ['action'],
        '''SELECT user_id, COUNT(*) FROM train_user WHERE behavior_type = 4 AND DAY < 1 GROUP BY user_id''')

    #bid特征
    time_action_feature(
        'bid_action_time_1',
        ['time'],
        ['action'],
        '''SELECT item_id,COUNT(*) AS bid_action_time_1 FROM train_user WHERE behavior_type = 4 AND DAY < 1  GROUP BY item_id; ''')

    time_action_feature(
        'bid_action_time_2',
        ['time'],
        ['action'],
        '''SELECT item_id,COUNT(DISTINCT day) FROM train_user WHERE behavior_type = 4 AND DAY < 1 GROUP BY item_id ;''')

    #uid_bid特征
    time_action_feature(
        'uid_bid_action_time_1',
        ['time'],
        ['action'],
        '''select user_id,item_id,count(item_id) as feature1 from train_user where behavior_type = 4 and day < 1 group by user_id,item_id;''')

    # try:
    #     os.remove(os.path.join(work_dir,'uid_term3_score1.txt'))
    #     os.remove(os.path.join(work_dir, 'uid_term3_score2.txt'))
    # except Exception,e:
    # 