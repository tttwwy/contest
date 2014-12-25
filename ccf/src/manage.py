# coding=utf-8
# created by WangZhe on 2014/12/23
import os
os.environ.setdefault("CONTEST_SETTINGS_MODULE", "setting")
from contest.main import spark

print os.environ['CONTEST_SETTINGS_MODULE']

class Work(spark.SparkModel):
    def get_score(self, uid_label_predict):
        pass

    def save_submit_file(self,predicts,save_file_name):
        pass



if __name__ == "__main__":
    a = Work()

