# coding=utf-8
# created by WangZhe on 2014/12/25
import os
from contest.util import conf
conf.set_config_path('src/setting.py')
print conf.setting.log_path
# from contest.util.log import *

from src.feature import MyExtract



for work_dir,database in [('G:\\Program\\python\\contest\\score\\feature\\train',"score_train"),("G:\\Program\\python\\contest\\score\\feature\\test","score_test")]:
    feature = MyExtract(work_dir = work_dir,host='ssh.freeshell.ustc.edu.cn',user='root',passwd='root',port=48384,db=database)
    feature.run_sql("drop function if EXISTS daypart;")
    feature.run_sql('''CREATE FUNCTION daypart( time datetime)
                        RETURNS INT
                        BEGIN
                        DECLARE x,hour_time INT;
                        set hour_time = hour(time);
                        set x = 5;
                        if hour_time >=5 and hour_time <=8  then
                        set x = 1;
                        end if;
                        if hour_time >8 and hour_time <=11  then
                        set x = 2;
                        end if;
                        if hour_time >11 and hour_time <=13  then
                        set x = 3;
                        end if;
                        if hour_time >13 and hour_time <=19  then
                        set x = 4;
                        end if;
                        return x;
                        end''')

    def time_feature(feature_name, times, sql):
        sql_replace = {'month': 'month(time)',
                        'week': 'week(time)',
                        'daypart': 'daypart(time)'}
        for time in times:
            if time == 'all_term':
                new_sql = sql.replace('month(time),', '')
                new_feature_name = feature_name.replace('time_', '')
            else:
                new_sql = sql.replace('month(time)', sql_replace[time])
                new_feature_name = feature_name.replace('time', time)

            feature.extract(new_feature_name, new_sql)


    time_feature('uid_term_time_book_1',
                 ['all_term'],
                 '''select uid,term,month(time),book_id,1 from book group by uid,term,month(time),book_id''')

    time_feature('uid_term_time_category_1',
                 ['all_term'],
                 '''select uid,term,month(time),category,count(uid) from book group by uid,term,month(time),category''')

    time_feature('uid_term_time_category_2',
                 ['all_term'],
                 '''select uid,term,month(time),category,1 from book group by uid,term,month(time),category''')

    feature.extract('uid_term_score1', ''' SELECT uid,term,rank FROM score''')
    feature.extract('uid_term_score2', ''' select uid,term,rank*rank from score''')
    feature.extract('uid_term_score3', ''' select a.uid,0,a.rank*b.rank from
                                            (select uid,rank from score where term=1)a
                                            INNER JOIN
                                            (select uid,rank from score where term=2)b on a.uid = b.uid''')

    # uid_term_time
    time_feature('uid_term_time_1',
                 ['all_term','month'],
                 ''' SELECT uid,term,month(time),count(uid) FROM `book`group by uid,term,month(time)''')

    time_feature('uid_term_time_2',
                 ['all_term','month','week','daypart'],
                 ''' select uid,term,month(time),count(uid) from library_door group by uid,term,month(time)''')

    time_feature('uid_term_time_3',
                 ['all_term','month'],
                 ''' select uid,term,month(time),count(distinct day(time)) from library_door group by uid,term,month(time)''')

    time_feature('uid_term_time_4',
                 ['all_term','month'],
                 ''' select uid,term,month(time),count(uid)/count(distinct day(time)) from library_door group by uid,term,month(time)''')



    #uid_term_time_location

    time_feature('uid_term_time_location_1',
                 ['all_term', 'month','week','daypart'],
                 ''' select uid,term,month(time),location,sum(money) FROM `money` group by uid,term,month(time),location;''')

    time_feature('uid_term_time_location_2',
                 ['all_term', 'month','week','daypart'],
                 ''' SELECT uid,term,month(time),location,count(uid) FROM `money` group by uid,term,month(time),location;''')
    time_feature('uid_term_time_location_3',
                 ['all_term', 'month'],
                 ''' SELECT uid,term,month(time),location,count(distinct day(time)) FROM `money` group by uid,term,month(time),location;''')

    time_feature('uid_term_time_location_4',
                 ['all_term', 'month'],
                 ''' SELECT uid,term,month(time),location,sum(money)/count(distinct day(time)) FROM `money` group by uid,term,month(time),location;''')

    time_feature('uid_term_time_location_5',
                 ['all_term', 'month'],
                 ''' SELECT uid,term,month(time),location,count(uid)/count(distinct day(time)) FROM `money` group by uid,term,month(time),location;''')
