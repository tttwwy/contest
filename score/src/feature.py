# coding=utf-8
# created by WangZhe on 2014/12/23


from contest.feature.extract import MySql
import os
from collections import defaultdict
from contest.util.log import logging
class MyExtract(MySql):

    def __init__(self,work_dir='',**kwargs):
        super(MyExtract,self).__init__(work_dir='',**kwargs)

    def extract(self,feature_name,sql):
        logging.info("{0} start".format(feature_name))
        logging.info("sql:{0}".format(sql))

        terms = defaultdict(lambda: defaultdict(lambda: []))
        feature_list = feature_name.strip().split("_")
        feature_size = len(feature_list)
        for line in self.read_sql(sql):
            if len(line) != feature_size:
                continue

            uid,term = line[:2]
            other_key = line[2:-1]
            value = line[-1]
            terms[term][uid].append(("_".join(other_key),value))

        for term,items in terms.iteritems():
            with open(os.path.join(self.work_dir, "uid_term{0}_{1}".format(term,"_".join(feature_list)) + ".txt"), 'w') as f:
                for uid,value_list in items:
                    f.write("{0}\t{1}".format(uid,"\t".join(["{0}:{1}".format(key,value) for key,value in value_list])))
        logging.info("{0} end".format(feature_name))


if __name__ == "__main__":
    pass
