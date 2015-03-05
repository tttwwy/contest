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

    feature.extract('uid_term_month_1', ''' SELECT uid,term,month(time),count(uid) FROM `book`group by uid,term,month(time)''')
    feature.extract('uid_term_month_2', '''select uid,term,month(time),count(uid) from library_door group by uid,term,month(time) ''')
    feature.extract('uid_term_month_3', ''' select uid,term,month(time),count(distinct day(time)) from library_door group by uid,term,month(time)''')
    feature.extract('uid_term_month_4', ''' select uid,term,month(time),count(uid)/count(distinct day(time)) from library_door group by uid,term,month(time)''')


    feature.extract('uid_term_book_month_1', '''select uid,term,book_id,1 from book group by term,book_id ''')
    feature.extract('uid_term_category_month_1', ''' select uid,term,category,1 from book group by term,category''')



    feature.extract('uid_term_week_1', ''' select uid,term,week(time),count(uid) from library_door group by uid,term,week(time)''')
    
    feature.extract('uid_term_1', ''' ''')
    feature.extract('uid_term_1', ''' ''')
    feature.extract('uid_term_1', ''' ''')
    feature.extract('uid_term_1', ''' ''')
    feature.extract('uid_term_1', ''' ''')
    feature.extract('uid_term_1', ''' ''')
    feature.extract('uid_term_1', ''' ''')


    feature.extract('uid_term_1','select uid,term,rank from score')
    feature.extract('uid_term_2','select uid,term,rank*rank from score')
    feature.extract('uid_term_3','''select a.uid,0,a.rank*b.rank from
    (select uid,rank from score where term=1)a
    INNER JOIN
    (select uid,rank from score where term=2)b on a.uid = b.uid''')

