# coding=utf-8
# created by WangZhe on 2014/12/28
from contest.feature.extract import *
class Feature(MySql):
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
                        f.write("{0}\t{2}:{3}\n".format(key,feature_name,value))



if __name__ == "__main__":
    pass
