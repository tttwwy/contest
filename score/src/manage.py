# coding=utf-8
# created by WangZhe on 2014/12/23


from contest.feature.extract import Base,MySql
from contest.main.general import GeneralModel
import os
from collections import defaultdict
class MyExtract(MySql):
    def extract(self,feature_name,sql):
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

class MyContest(GeneralModel):
    def __init__(self):
        super(self,GeneralModel).__init__()

    def handle_predict_result(self, uid_label_predict, **kwargs):
        return uid_label_predict
    # def get_score(self, uid_label_predict):

#
# class Work(spark.SparkModel):
#     def get_score(self, uid_label_predict):
#         pass
#
#     def save_submit_file(self,predicts,save_file_name):
#         pass



if __name__ == "__main__":
    pass
