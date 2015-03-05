# coding=utf-8
# created by WangZhe on 2014/11/2

import os
import collections
from contest.util.log import logging,train_log,run_time

class Base(object):
    def read_sql(self,sql):
        pass

    # @run_time
    # def extract(self,feature_name,sql):
    #     results = collections.defaultdict(list)
    #     for line in self.read_sql(sql):
    #         uid = line[0]
    #         key = feature_name + line[1] if len(line) == 3 else ''
    #         value = line[-1]
    #         results[uid].append((key,value))
    #
    #     with open(os.path.join(self.work_dir, feature_name + ".txt"), 'w') as f:
    #         for uid,key_value in results.iteritems():
    #             result_list = ["{0}:{1}".format(key,value) for key,value in key_value]
    #             f.write("{0}\t{1}\n".format(uid,"\t".join(result_list)))

    @run_time
    def extract(self,feature_name,sql):
        with open(os.path.join(self.work_dir, feature_name + ".txt"), 'w') as f:
            for line in self.read_sql(sql):
                if feature_name[:2] == 'si':
                    key1 = line[0]
                    key2 = line[1]
                    value = line[2]
                    f.write("{0}_{1}\t{2}:{3}\n".format(key1,key2,feature_name,value))
                else:
                    key = line[0]
                    value = line[1]
                    f.write("{0}\t{1}:{2}\n".format(key,feature_name,value))

class Hive(Base):
    def __init__(self,hive_path,work_dir='',database=''):
        self.hive_path = hive_path
        self.work_dir = work_dir
        self.database = database

    @run_time
    def set_database(self,database):
        self.database = database

    @run_time
    def read_sql(self,sql):
        execute = '''{0} -e "{1}" --database {2}'''.format(self.hive_path, sql, self.database)
        print execute
        for line in os.popen(execute):
            line_list = line.strip().split("\t")
            if len(line_list) + 1 == type:
                yield line_list

class MySql(Base):
    def __init__(self,work_dir='',**kwargs):

        self.work_dir = work_dir
        self.kwargs = kwargs
        self.set_database()
        print self.work_dir



    @run_time
    def set_database(self,db=''):
        import MySQLdb
        if db:
            self.kwargs['db'] = db
        self.cursor  = MySQLdb.connect(**self.kwargs).cursor()

    @run_time
    def read_sql(self,sql):
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

if __name__ == "__main__":
    feature = MySql()






