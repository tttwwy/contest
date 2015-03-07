# coding=utf-8
# created by WangZhe on 2014/12/23


from contest.main.general import GeneralModel

class MyContest(GeneralModel):
    def __init__(self):
        super(GeneralModel,self).__init__()

    def handle_predict_result(self, uid_label_predict, **kwargs):
        # uid_label_predict = [(uid,float(label),float(predict))for uid,label,predict in uid_label_predict]
        # label_replace = {label:index+1 for index,label in enumerate(sorted([label for uid,label,predict in uid_label_predict]))}
        # predict_replace = {predict:index+1 for index,predict in enumerate(sorted([predict for uid,label,predict in uid_label_predict]))}
        # new_result = [ (uid, label_replace[label] , predict_replace[predict]) for uid,label,predict in uid_label_predict ]

        result = [[uid,label,predict] for uid,label,predict in uid_label_predict]
        result = sorted(result,cmp=lambda x,y:cmp(x[1],y[1]))
        for  index,item in enumerate(result):
            result[index][1] = index + 1

        result = sorted(result,cmp=lambda x,y:cmp(x[2],y[2]))
        for  index,item in enumerate(result):
            result[index][2] = index + 1
        return result



    def get_score(self, uid_label_predict):
        n = len(uid_label_predict)

        score = 1 - 6.0 * sum([(label - predict)**2 for uid,label,predict in uid_label_predict])/(n*(n**2-1))
        score = round(score,3)
        return {'score':score}

    def save_submit_file(self, predicts, save_file_name):
        with open(save_file_name,'w') as f:
            f.write('id,rank\n')
            for uid,label,predict in predicts:
                f.write('{0},{1}\n'.format(uid,predict))
def save_submit_file(self, predicts, save_file_name):
    pass
