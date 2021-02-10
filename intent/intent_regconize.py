from utils import *
import os
import pandas as pd
import requests
from intent.pattern_intent import *
#
# def predict_fastai(mess):
#     mess_clean = mess
#     mess_rm_sw = remove_stopword(mess_clean)
#     print(mess_rm_sw)
#     np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
#     # model_path = 'intent/'
#     model_path = './intent/'
#     data_classify = load_data(model_path,'data_classify')
#     model = text_classifier_learner(data_classify, AWD_LSTM, drop_mult=0.65, metrics=[accuracy])
#     model.load('vi_classify', purge=False)
#     # model.load('intent_model.pkl', purge=False)
#     predict = model.predict(mess_rm_sw)
#
#     list_pred = predict[2].tolist()
#     probability = max(list_pred)
#     # print(list_pred)
#     index_pred = list_pred.index(probability)
#     # list_label = ['satisfy','career']
#     list_label = ['other_intent','career']
#     label_pred = list_label[index_pred]
#     if probability > 0.66:
#         return label_pred,probability,mess
#     else:
#         return 'other_intent',1.0,mess
#
def predict_lstm(mess):
    url = 'https://api-intent.herokuapp.com/predict'
    pred = requests.post(url,json={'message':mess})
    dict_pred = pred.json()
    return dict_pred['intent'],dict_pred['probability'],dict_pred['message']


def catch_intent(mess):
    # input: câu nhập vào của người dùng
    # return: intent,probability,messcleaned
    # quy trình xử lý: chuẩn hóa kiểu gõ,check question ,check intent
    mess_unic = convert_unicode(mess)
    mess_clean = clean_mess(mess_unic)

    if check_question(mess_clean):
        for index1,item in enumerate(list(dict_business_intent.keys())):
            list_intent = dict_business_intent[item]
            for index2,notifi in enumerate(list_intent):
                if mess_clean.find(notifi)!=-1:
                    return item,1.0,mess_clean
                elif index1 == (len(list(dict_business_intent.keys()))-1) and index2 == (len(list_intent)-1):
                    return predict_lstm(mess_clean)
                else:
                    pass
    else:
        for index1,item in enumerate(list(dict_random_intent.keys())):
            list_intent_stm = dict_random_intent[item]
            for index2,notifi in enumerate(list_intent_stm):
                if mess_clean.find(notifi)!=-1:
                    return item,1.0,mess_clean
                elif index1 == (len(list(dict_random_intent.keys()))-1) and index2 == (len(list_intent_stm)-1):
                    return 'not_intent',1.0,mess_clean
                else:
                    pass
