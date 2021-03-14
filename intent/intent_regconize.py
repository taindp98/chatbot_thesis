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
# def check_question(mess):
#     # input: câu nhập vào người dùng
#     # return: nếu là câu hỏi True
#     for ele in list_check_question:
#         if (mess.lower().find(ele) != -1):
#             print(ele)
#             return True
def check_question(message):
#     ... subject muốn hỏi/biết/xin… *
# ... subject muốn được hỏi/tư vấn .... *
# ... cho subject hỏi/biết/xin *
# ... subject cần hỏi/biết/xin... *
# .... subject cần ... thông tin … *
# .... gửi subject ... *
# ... cho hỏi/xin/biết… *
# ... có/được (...)? không (...) *
    #bắt WH question
    for signal in list_question_signal:
        if signal in message.lower():
            # #print(signal)
            return True

    for verb in list_verb_have:
        if (message.lower().find(verb)!=-1 and message.lower().find("không")!=-1 and message.lower().find(verb)<message.lower().find("không")):
            #print("1")
            return True

    #....sao (liên hệ/đăng ký sao)
    if "sao"==message.split(' ')[len(message.split(' '))-1]:
        return True


    #.... sao bạn
    for object in list_object:
        if message.lower().find("sao")!=-1 and message.lower().find(object)!=-1 and message.lower().find("sao")<message.lower().find(object):
            return True

    if (message.lower().find("còn")!=-1 and message.lower().find("không")!=-1 and message.lower().find("còn")<message.lower().find("không")):
        #print("1")
        return True

    if message.lower().find("xin")!=-1 and (message.lower().find("chào")< message.lower().find("xin")):
        #print("1")
        return True

    #cách liên hệ/đăng ký
    if message.lower().find("cách")==0:
        #print("1")
        return True

    #ai .... (ai được tham gia)
    if message.lower().find("ai")==0:
        #print("1")
        return True


    # #thông tin về xxx/thông tin xxx
    # if message.lower().find("thông tin")!=-1:
    #     #print("1")
    #     return True

    for subject in list_subject:
        for verb in list_verb_want:
            if (message.lower().find(subject+" muốn "+verb)!=-1 or message.lower().find("cho "+subject+" "+verb)!=-1 or message.lower().find(subject+" cần "+verb)!=-1):
                #print("2")
                return True

    for subject in list_subject:
        #chứ bạn
        if message.lower().find("chứ "+subject)!=-1:
            #print("3")
            return True
        if (message.lower().find(subject+" muốn được hỏi")!=-1 or message.lower().find(subject+" muốn được tư vấn")!=-1):
            #print("3")
            return True
        if (message.lower().find(subject+" cần")!=-1 and message.lower().find("thông tin")!=-1 and message.lower().find(subject+" cần")<message.lower().find("thông tin")):
            #print("4")
            return True
        if (message.lower().find(subject+" muốn")!=-1 and message.lower().find("thông tin")!=-1 and message.lower().find(subject+" muốn")<message.lower().find("thông tin")):
            #print("4")
            return True
        if (message.lower().find("gửi "+subject)!=-1):
            #print("5")
            return True
        if (message.lower().find("chỉ "+subject)!=-1):
            #print("5")
            return True
        if (message.lower().find("chỉ giúp "+subject)!=-1):
            #print("5")
            return True

    #cho xin
    for verb in list_verb_want:
        if (message.lower().find("cho "+verb)!=-1):
            #print("6")
            return True

    # nào ... nhỉ
    for signal in list_question_signal_last:
        if (message.lower().find("nào")!=-1) and (message.lower().find(signal)!=-1) and (message.lower().find("nào")<message.lower().find(signal)):
            #print("6")
            return True

    #...... hả
    if message.lower().split(' ')[len(message.lower().split(' '))-1]=="hả":
        return True



    #gửi cho mình/cho mình/gửi mình/mình cần/mình muốn
    for subject in list_subject:
        if (message.lower().find("cho "+subject)!=-1) or (message.lower().find("gửi "+subject)!=-1) or (message.lower().find(subject+" cần")!=-1) or (message.lower().find(subject+" muốn")!=-1):
            return True


    #mình (có việc) muốn/cần
    #mình định....
    for subject in list_subject:
        if ((message.lower().find(subject)!=-1) and (message.lower().find("định")!=-1) and (message.lower().find(subject)<message.lower().find("định"))) or ((message.lower().find(subject)!=-1) and (message.lower().find("cần")!=-1) and (message.lower().find(subject)<message.lower().find("cần"))) or ((message.lower().find(subject)!=-1) and (message.lower().find("muốn")!=-1) and (message.lower().find(subject)<message.lower().find("muốn"))):
            return True

    #bắt YES-NO/WH question mà signal cuối câu
    if len(message.split(" "))>3 and (message.split(" ")[-1].lower()=="chưa" or message.split(" ")[-1].lower()=="không" or message.split(" ")[-1].lower()=="ta" or message.split(" ")[-1].lower()=="sao" or message.split(" ")[-1].lower()=="nhỉ" or message.split(" ")[-1].lower()=="nào"):
        #print("7")
        return True

    #bắt YES-NO question cuối câu có chủ ngữ

    for subject in list_object:
        for question_signal_last in list_question_signal_last:
            if message.split(" ")[-1].lower()==subject and message.split(" ")[-2].lower()==question_signal_last:
                #print("8")
                return True


    return False
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
