# coding=utf-8
# created by WangZhe on 2014/12/23


from contest.feature.extract import MySql
import os
from collections import defaultdict
from contest.util.log import logging
class MyExtract(MySql):

    def __init__(self,work_dir='',**kwargs):
        super(MyExtract,self).__init__(work_dir,**kwargs)

    def extract(self,feature_name,sql):
        logging.info("{0} start".format(feature_name))
        logging.info("sql:{0}".format(sql))

        with open(os.path.join(self.work_dir, feature_name +  ".txt"),'w') as f:
            for line in self.read_sql(sql):
                line = [str(x) for x in line]
                f.write("{0}\n".format("\t".join(line)))
        logging.info("{0} end".format(feature_name))


if __name__ == "__main__":
    pass
