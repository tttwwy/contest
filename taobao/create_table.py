# coding=utf-8
# created by WangZhe on 2014/12/25


import sys
from contest.util import conf

import platform
if platform.system() == 'Windows':
    conf.set_config_path('G:/Program/python/contest/taobao/src/setting.py')
else:
    conf.set_config_path('/media/172.16.46.8/wangzhe/contest/taobao/src/linux_setting.py')

print conf.setting.log_path
from contest.util.log import logging
print sys.path
from src.myfeature import MyExtract



def create_table(table_name,start_time,end_time):
    sql = '''
 CREATE TABLE {table_name} (
  `user_id` int(10) unsigned DEFAULT NULL,
  `item_id` int(11) DEFAULT NULL,
  `behavior_type` int(11) DEFAULT NULL,
  `user_geohash` varchar(30) DEFAULT NULL,
  `item_category` int(11) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `day` int(10) unsigned DEFAULT NULL,
  KEY `user_id` (`user_id`),
  KEY `item_id` (`item_id`),
  KEY `behavior_type` (`behavior_type`),
  KEY `day_1` (`day`)
)as
SELECT
  *,
 datediff('{end_time}',time) as day
FROM
 train_user
WHERE 
 time>='{start_time} 00:00:00' and time<='{end_time} 23:59:59'
    '''.format(start_time=start_time,end_time=end_time,table_name=table_name)
    return sql
feature = MyExtract(work_dir = conf.setting.feature_path,host='114.214.166.162',user='tianchi',passwd='tianchi',port=3435,db='mobile')
times = [
    ('test_1205_1218','2014-12-5','2014-12-18'),
         ('target_1212','2014-12-12','2014-12-12'),
         ('train_1128_1211','2014-11-28','2014-12-11'),
         ('target_1205','2014-12-5','2014-12-5'),
         ('train_1121_1204','2014-11-21','2014-12-4'),
         ('target_1128','2014-11-28','2014-11-28'),
         ('train_1118_1127','2014-11-18','2014-11-27')
         ]
for table_name,start_time,end_time in times:
    logging.info("{0} {1} {2} start".format(table_name,start_time,end_time))
    sql = create_table(table_name,start_time,end_time)
    feature.run_sql(sql)
    logging.info("{0} {1} {2} end".format(table_name, start_time, end_time))
