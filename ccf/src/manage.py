# coding=utf-8
# created by WangZhe on 2014/12/23

from contest.main import spark


class Work(spark.SparkModel):
    def __init__(self):
        spark.SparkModel.__init__(self)

    def read_labels(self,file_name):
        labels = {}
        for line in open(file_name,'r'):
            uid = line.strip()
            labels[uid] = '1'
        return labels




if __name__ == "__main__":
    a = Work()

