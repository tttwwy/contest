# coding=utf-8
# created by WangZhe on 2014/12/23


from contest.main.general import GeneralModel

class MyContest(GeneralModel):
    def __init__(self):
        super(GeneralModel,self).__init__()

    def handle_predict_result(self, uid_label_predict, **kwargs):
        label_replace = {label:index+1 for index,label in enumerate(sorted([int(label) for uid,label,predict in uid_label_predict]))}
        predict_replace = {predict:index+1 for index,predict in enumerate(sorted([int(predict) for uid,label,predict in uid_label_predict]))}
        new_result = [ (uid, label_replace[int(label)] , predict_replace[int(predict)]) for uid,label,predict in uid_label_predict ]
        return new_result

    def get_score(self, uid_label_predict):
        print uid_label_predict
        n = len(uid_label_predict)

        score = 1 - 6.0 * sum([(label - predict)**2 for uid,label,predict in uid_label_predict])/(n*(n**2-1))
        return {'score':score}

    def save_submit_file(self, predicts, save_file_name):
        with open(save_file_name,'w') as f:
            f.write('id,rank\n')
            for uid,label,predict in predicts:
                f.write('{0},{1}\n'.format(uid,predict))
def save_submit_file(self, predicts, save_file_name):
    pass
