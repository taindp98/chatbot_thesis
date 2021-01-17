from utils import *
import os
import pandas as pd
"""
2 class:
+ nên chọn ngành nào
+ review về ngành
"""
path = 'data/'
def catch_intent(mess):
    # input: câu nhập vào của người dùng
    # return: intent,probability,messcleaned
    # quy trình xử lý: chuẩn hóa kiểu gõ,check question ,check intent
    mess_unic = convert_unicode(mess)
    mess_clean = clean_mess(mess_unic)
    # mess_rmsw = remove_stopword(mess_unic)
    dict_require_pattern = {}
    with open(os.path.join(path,'pattern_require_intent.csv'),'r') as infile:
        pattern_synth = pd.read_csv(infile)
        pattern_name_list = pattern_synth['pattern_name'].tolist()
        keyword = pattern_synth['keyword']
        # print(pattern_name_list)
        for index,ele in enumerate(pattern_name_list):
            keyword_list = []
            keywords = str(keyword[index]).split(',')
            for word in keywords:
                keyword_list.append(word)
            dict_require_pattern[ele] = keyword_list

    dict_statement_pattern = {}
    with open(os.path.join(path,'pattern_statement_intent.csv'),'r') as stmfile:
        pattern_stm = pd.read_csv(stmfile)
        pattern_stm_name = pattern_stm['pattern_name'].tolist()
        keyword = pattern_stm['keyword']
        for index,ele in enumerate(pattern_stm_name):
            keyword_list = []
            keywords = str(keyword[index]).split(',')
            for word in keywords:
                keyword_list.append(word)
            dict_statement_pattern[ele] = keyword_list
    # print(dict_statement_pattern)
    if check_question(mess_clean):
        # print("This is question")
        for index1,item in enumerate(list(dict_require_pattern.keys())):
            list_intent = dict_require_pattern[item]
            for index2,notifi in enumerate(list_intent):
                if mess_clean.find(notifi)!=-1:
                    return item,1.0,mess_clean
                elif index1 == (len(list(dict_require_pattern.keys()))-1) and index2 == (len(list_intent)-1):
                    return predict_fastai(mess_clean)
                else:
                    pass
    else:
        for index1,item in enumerate(list(dict_statement_pattern.keys())):
            list_intent_stm = dict_statement_pattern[item]
            for index2,notifi in enumerate(list_intent_stm):
                # print(notifi)
                if mess_clean.find(notifi)!=-1:
                    return item,1.0,mess_clean
                elif index1 == (len(list(dict_statement_pattern.keys()))-1) and index2 == (len(list_intent_stm)-1):
                    return 'not_intent',1.0,mess_clean
                else:
                    pass

