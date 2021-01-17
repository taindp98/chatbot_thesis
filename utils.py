from datetime import date
import string
import torch
import numpy as np
from pyvi import ViTokenizer
# import regex as re
import os
import re
import json
from fastai.text import *
import pickle
# path = '/home/taindp/Database/intent/'
path = 'data/'
def check_question(mess):
    # input: câu nhập vào người dùng
    # return: nếu là câu hỏi True
    list_quest = []
    with open(os.path.join(path,'check_question.txt'),'r') as infile:
        lines = infile.readlines()
        for line in lines:
            line = str(line).replace('\n','')
            words = line.split(',')
            for word in words:
                list_quest.append(word)
    for ele in list_quest:
        if (mess.lower().find(ele) != -1):
            return True

def create_token(mess):
    # input: câu nhập vào của người dùng
    # return: token(_) loại bỏ những special token
    mess_rmspectoken = re.findall(r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ0-9]+\b', mess)
    mess_norm = ' '.join(mess_rmspectoken)
    mess_token = ViTokenizer.tokenize(mess_norm)
    mess_lower = mess_token.lower()
    tokens = mess_lower.split()
    table = str.maketrans('', '', string.punctuation.replace("_", ""))
    tokens = [w.translate(table) for w in tokens]
    tokens = [word for word in tokens if word]
    return tokens

def remove_stopword(mess):
    # input: đường dẫn tới file chứa stopword
    # input: câu nhập vào của người dùng đã create_token thành token
    # return: câu tự nhiên đã loại bỏ stopword giúp bắt entity dễ dàng hơn
    mess_cleaned=create_token(mess)
    f=open(os.path.join(path,'stopword.txt'),'r')
    stopword=f.read()
    sw_word=stopword.split(',')
    stop_word=set(sw_word)
    mean_mess=[w for w in mess_cleaned if w not in stop_word]
    mess_std = []
    for item in mean_mess:
        item_std = item.replace('_',' ')
        mess_std.append(item_std)
    return ' '.join(mess_std)

uniChars = "àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆĐÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴÂĂĐÔƠƯ"
unsignChars = "aaaaaaaaaaaaaaaaaeeeeeeeeeeediiiiiooooooooooooooooouuuuuuuuuuuyyyyyAAAAAAAAAAAAAAAAAEEEEEEEEEEEDIIIOOOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYYAADOOU"


def loaddicchar():
    dic = {}
    char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
        '|')
    charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
        '|')
    for i in range(len(char1252)):
        dic[char1252[i]] = charutf8[i]
    return dic
dicchar = loaddicchar()
def convert_unicode(txt):
    return re.sub(
        r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
        lambda x: dicchar[x.group()], txt)
def clean_mess(mess):
    # input: câu nhập vào của người dùng
    # return: câu đã loại bỏ special token
    mess_unic = convert_unicode(mess).lower()
    mess_rmspectoken = re.findall(r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ0-9]+\b', mess_unic)
    mess_norm = ' '.join(mess_rmspectoken)
    return mess_norm



def get_current_time():
    time= date.today()
    time_split = str(time).split('-')
    year = time_split[0]
    return year

def find_entity_equation(sentence,list_entity):
    #input câu nhập user nhập vào
    #output tất cả các thực thể trong list_entity có trong câu
    normalized_sentence=convert_unicode(sentence)
    list_token_sentence=normalized_sentence.split(' ')
    list_result_entity=[]
    list_normalized_entity=[convert_unicode(entity) for entity in list_entity]
    for entity in list_normalized_entity:
        list_token_entity=entity.split(' ')
        for i in range(len(list_token_sentence)-len(list_token_entity)+1):
            if list_token_entity==list_token_sentence[i:i+len(list_token_entity)]:
                list_result_entity.append(entity)
    return list_result_entity

def longest_common_sublist(a, b):
    #input list a, list b
    #output số item chung liền kề dài nhất và giá trị item đầu tiên trong list item chung
    table = {}
    l = 0
    i_max = None
    j_max = None
    for i, ca in enumerate(a, 1):
        #enumerate(iter,start)
        for j, cb in enumerate(b, 1):
            if ca == cb:
                table[i, j] = table.get((i - 1, j - 1), 0) + 1
                if table[i, j] > l:
                    l = table[i, j]
                    i_max=i
                    j_max=j
    if i_max != None:
        return l,i_max - 1
    return l,i_max

def lcs_length(a, b):
    #input list a, list b
    #output max length cả liền kề / không liền kề
    table = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i, ca in enumerate(a, 1):
        for j, cb in enumerate(b, 1):
            table[i][j] = (
                table[i - 1][j - 1] + 1 if ca == cb else
                max(table[i][j - 1], table[i - 1][j]))
    return table[-1][-1]

def find_entity_longest_common(sentence,list_entity,entity_name):
    #input câu user nhập vào,list entity, entity được chọn để bắt
    #output index của entity bắt được trong list entity, chiều dài max, index last của token match trong câu nhập vào
    normalized_sentence=convert_unicode(sentence)
    list_token_sentence = normalized_sentence.split(' ')
    list_result_entity = []
    dict_max_len = {}
    list_normalized_entity = [str(entity) for entity in list_entity]
    result = []
    longest_common_length = None
    end_common_index = None
    for index, entity in enumerate(list_normalized_entity):
        list_token_entity = entity.split(' ')
        longest_common_length, end_common_index = longest_common_sublist(list_token_sentence,list_token_entity)
        if longest_common_length!=0:
            dict_max_len[(index)] = {'longest_common_length':longest_common_length,'end_common_index':end_common_index}
        # list_token_sentence = list_token_sentence[: end_common_index - longest_common_length] + list_token_sentence[end_common_index:]
    max_longest_common_length=0
    for k,v in dict_max_len.items():
        if v['longest_common_length']>max_longest_common_length:
            max_longest_common_length=v['longest_common_length']

    for k,v in dict_max_len.items():
        if v['longest_common_length']==max_longest_common_length:
            if entity_name in ['register','reward','works']:
                result.append({"longest_common_entity_index":int(k),"longest_common_length":v['max_length_in_sentence'],"end_common_index":v['end_common_index']})
            else:
                result.append({"longest_common_entity_index":int(k),"longest_common_length":v['longest_common_length'],"end_common_index":v['end_common_index']})
    return result

def check_shorted_entity(path_db_entity):
    # input: path tới json chứa db toàn bộ entity
    # return: chiều dài ngắn nhất cho từng entity
    with open(path_db_entity,'r') as dict_file:
        dict = json.load(dict_file)
    len_dict={}
    for item in dict.keys():
        shorted=100
        for ele in dict[item]:
            ele_ap=[]
            ele_split=str(ele).split()
            for i in ele_split:
                if i != ' ':
                    ele_ap.append(i)
            ele_len=len(ele_ap)
            if ele_len < shorted :
                shorted = ele_len
        len_dict[item]=shorted
    return len_dict

def predict_fastai(mess):
    np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
    model_path = 'intent/'
    data_classify = load_data(model_path,'data_classify')
    # model = text_classifier_learner(data_classify, AWD_LSTM, drop_mult=0.6, metrics=[accuracy])
    model = text_classifier_learner(data_classify, AWD_LSTM, drop_mult=0.65, metrics=[accuracy])
    # model.load(os.path.join(model_path,'vi_classify'), purge=False)
    model.load('vi_classify', purge=False)
    predict = model.predict(mess)

    list_pred = predict[2].tolist()
    probability = max(list_pred)
    # print(list_pred)
    index_pred = list_pred.index(probability)
    list_label = ['satisfy','career']
    label_pred = list_label[index_pred]
    if probability > 0.6:
        return label_pred,probability,mess
    else:
        return 'other_intent',1.0,mess

def load_jsonfile(path):
    list_data = []
    for line in open(path, 'r'):
        list_data.append(json.loads(line))
    df = pd.DataFrame.from_dict(list_data)
    return df

def clean_mess_point(mess):
    # input: câu nhập vào của người dùng
    # return: câu đã loại bỏ special token
    mess_unic = convert_unicode(mess).lower()
    mess_rmspectoken = re.findall(r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ0-9\.]+\b', mess_unic)
    # mess_rmspectoken = ' '.join(re.findall('[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđA-ZÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÉÈẺẼẸÊẾỀỂỄỆÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÍÌỈĨỊÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴĐ0-9\,\.]+', mess_unic))
    mess_norm = ' '.join(mess_rmspectoken)
    return mess_norm
def load_csvfile(path):
    df = pd.read_csv(open(path, 'r'))
    dict_data = {}
    keys = df['compare'].tolist()
    values = df['keywords'].tolist()
    # list_value = []
    for index in range(len(values)):
        value = values[index].split(',')
        dict_data[keys[index]] = value
        # list_value.append(value)
    return dict_data
def catch_point(mess):
    # bắt thực thể là điểm
    # return list điểm
    mess_clean = clean_mess_point(mess)
    dict_compare = load_csvfile(os.path.join(path,'compare_point.csv'))

    # mặc định luôn tìm điểm nhỏ hơn
    compare = 'lte'
    for key in list(dict_compare.keys()):
        for value in dict_compare[key]:
            if (mess_clean.find(value) != -1):
                compare = key
            else:
                continue
    # print(dict_compare)
    years = re.findall('\d+[k0]\d+',mess_clean)
    times = re.findall('\d+[/-]\d+[/-]*\d*',mess_clean)
    if years:
        for year in years:
            mess_clean = mess_clean.replace(year,'')
    if times:
        for time in times:
            mess_clean = mess_clean.replace(time,'')
    points = re.findall('\d+[., ]\d*[điểm đ d diem]+',mess_clean)
    # print(points)
    list_point = []
    ignore_list = [' ','điểm','đ','d','diem']
    for point in points:
        point_str = str(point).replace(',','.')
        point_clean = point_str
        for item in ignore_list:
            point_clean = point_clean.replace(item,'')
            # print(point_clean)
        # print(point_clean)
        if float(point_clean) > 1000:
            point_float = float(point_clean)/100
        elif float(point_clean) > 100:
            point_float = float(point_clean)/10
        else:
            point_float = float(point_clean)
        list_point.append(point_float)
    res = []
    if len(list_point) == 1:
        if compare == 'lte':
            res.append(float(0))
            res.append(list_point[0])
        else:
            res.append(list_point[0])
            res.append(float(30))
    elif len(list_point) == 2:
        res = list_point.sort()
    """
    return có dạng [cận dưới,cận trên]
    * nếu chỉ có 1 point bắt được: xét compare
        -compare lte: [0,point]
        -compare gte: [point,30]
    * nếu có 2 point bắt được: sort asc
    """
    return res
def export_pickle_file(data_dict,path):
    with open(path, 'wb') as handle:
        pickle.dump(data_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(path, 'rb') as handle:
        valid = pickle.load(handle)
    if data_dict == valid:
        print('export pickle file done')
def check_match_sublist_and_substring(list_children,list_parent):
        # print("match sublist")
        count_match=0
        list_children = [convert_unicode(x) for x in list_children]
        list_parent = [convert_unicode(x) for x in list_parent]
        for children_value in list_children:
            for parent_value in list_parent:
                if children_value in parent_value:
                    count_match+=1
                    break
        if count_match==len(list_children):
            # print("match sublist")
            return True
        return False
