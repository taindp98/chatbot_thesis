from utils import *
import os
import pandas as pd
from intent.pattern_intent import *

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
                    return predict_fastai(mess_clean)
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

