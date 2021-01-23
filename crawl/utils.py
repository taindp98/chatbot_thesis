from pyvi import ViTokenizer
from keras.preprocessing.text import Tokenizer
import nltk
import string
import regex as re
import json
from nltk.tokenize.treebank import TreebankWordDetokenizer
from pyvi import ViTokenizer
import pandas as pd
import csv
import re
import os
def check_question(data_path,mess):
    f1=open(os.path.join(data_path,'list_ques_signal.txt'),'r')
    content1=f1.read()
    content1=content1.replace('\n','')
    list_ques_signal = content1.split(",")
    f1.close()
    f2=open(os.path.join(data_path,'list_ques_signal_last.txt'),'r')
    content2=f2.read()
    content2=content2.replace('\n','')
    list_ques_signal_last = content2.split(",")
    f2.close()
    f3=open(os.path.join(data_path,'list_object.txt'),'r')
    content3=f3.read()
    content3=content3.replace('\n','')
    list_object = content3.split(",")
    f3.close()
    f4=open(os.path.join(data_path,'list_subject.txt'),'r')
    content4=f4.read()
    content4=content4.replace('\n','')
    list_subject = content4.split(",")
    f4.close()
    f5=open(os.path.join(data_path,'list_verb.txt'),'r')
    content5=f5.read()
    content5=content5.replace('\n','')
    list_verb = content5.split(",")
    f5.close()
    list_total=list_ques_signal+list_ques_signal_last+list_verb+list_object+list_subject
    for ele in list_total:
        if (mess.lower().find(ele) != -1):
            return True

def create_vocab(mess):
    token=Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\]^`{|}~ ')
    token.fit_on_texts(mess)
    return token.word_index

def create_token(mess):
    mess = re.findall(r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ0-9]+\b', mess)
    mess = ' '.join(mess)
    mess = ViTokenizer.tokenize(mess) #Pyvi Vitokenizer library
    mess = mess.lower() #Lower
    tokens = mess.split() #Split in_to words
    table = str.maketrans('', '', string.punctuation.replace("_", ""))
    tokens = [w.translate(table) for w in tokens]
    tokens = [word for word in tokens if word]
    return tokens

def clean_document_note(mess):
    #mess = re.findall(r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ0-9]+\b', mess)
    #mess = ' '.join(mess)
    mess = ViTokenizer.tokenize(mess) #Pyvi Vitokenizer library
    mess = mess.lower() #Lower
    tokens = mess.split(' ') #Split in_to words
    table = str.maketrans('', '', string.punctuation.replace("_", ""))
    tokens = [w.translate(table) for w in tokens]
    tokens = [word for word in tokens if word]
    return tokens

def remove_stopword(data_path,mess):
    #mess cleaned
    mess=create_token(mess)
    f=open(os.path.join(data_path,'stopword.txt'),'r')
    content=f.read()
    list=content.split(',')
    stop_word=set(list)
    mean_mess=[w for w in mess if not w in stop_word]
    return ' '.join(mean_mess) #tra ve string


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

def replace_short_word(data_path,mess):
    with open(os.path.join(data_path,'viettat.json')) as file1:
        d1 = json.load(file1)
    with open(os.path.join(data_path,'teencode.json')) as file2:
        d2 = json.load(file2)
    with open(os.path.join(data_path,'name_univ.json')) as file3:
        d3 = json.load(file3)
    with open(os.path.join(data_path,'complete.json')) as file4:
        d4 = json.load(file4)
    data={}
    data.update(d1)
    data.update(d2)
    data.update(d3)
    data.update(d4)
    list_key=list(data.keys())
    for t in range(len(list_key)):
        list_key[t]=list_key[t].lower()
    dict_ref=dict(zip(list_key,data.values()))
    #mess1=ViTokenizer.tokenize(mess).lower()
    mess=mess.lower()
    mess=nltk.word_tokenize(mess)
    for i,v in enumerate(mess):
        if v in dict_ref.keys():
            new_v=v.replace(v,dict_ref[v].lower())
            mess[i]=new_v
            #sent_new=(TreebankWordDetokenizer().detokenize(sent))
    sent_new=' '.join(mess)
    sent_new=sent_new.replace('_',' ')
    return sent_new

def intent_catch_pattern(data_path,mess):
    f1=open(os.path.join(data_path,'short-major.txt'),'r')
    content1=f1.read()
    content1 = content1.split(",")
    list_short_major=[]
    for item in content1:
        if ((item not in list_short_major) and (item != '')):
            list_short_major.append(item.rstrip())

    f2=open(os.path.join(data_path,'major.txt'),'r')
    content2=f2.read()
    content2 = content2.split(",")
    list_major=[]
    for item in content2:
        if ((item not in list_major) and (item != '')):
            list_major.append(item.rstrip())

    f3=open(os.path.join(data_path,'group.txt'),'r')
    content3=f3.read()
    content3 = content3.split(",")
    list_group=[]
    for item in content3:
        if ((item not in list_group) and (item != '')):
            list_group.append(item.rstrip())

    f4=open(os.path.join(data_path,'point.txt'),'r')
    content4=f4.read()
    content4 = content4.split(",")
    list_point=[]
    for item in content4:
        if ((item not in list_point) and (item != '')):
            list_point.append(item.rstrip())

    f5=open(os.path.join(data_path,'sub-require.txt'),'r')
    content5=f5.read()
    content5 = content5.split(",")
    list_sub_require=[]
    for item in content5:
        if ((item not in list_sub_require) and (item != '')):
            list_sub_require.append(item.rstrip())

    f6=open(os.path.join(data_path,'short-uni.txt'),'r')
    content6=f6.read()
    content6 = content6.split(",")
    list_short_uni=[]
    for item in content6:
        if ((item not in list_short_uni) and (item != '')):
            list_short_uni.append(item.rstrip())

    f7=open(os.path.join(data_path,'full-uni.txt'),'r')
    content7=f7.read()
    content7 = content7.split(",")
    list_full_uni=[]
    for item in content7:
        if ((item not in list_full_uni) and (item != '')):
            list_full_uni.append(item.rstrip())

    f8=open(os.path.join(data_path,'respect.txt'),'r')
    content8=f8.read()
    content8 = content8.split(",")
    list_respect=[]
    for item in content8:
        if ((item not in list_respect) and (item != '')):
            list_respect.append(item.rstrip())

    f9=open(os.path.join(data_path,'good-bye.txt'),'r')
    content9=f9.read()
    content9 = content9.split(",")
    list_good_bye=[]
    for item in content9:
        if ((item not in list_good_bye) and (item != '')):
            list_good_bye.append(item.rstrip())

    for notification in list_major:
        if mess.lower().find(notification)!=-1:
            return 'major',1.0

    for notification in list_short_major:
        if mess.lower().find(notification)!=-1:
            return 'code_major',1.0

    for notification in list_full_uni:
        if mess.lower().find(notification)!=-1:
            return 'full_name_uni',1.0

    for notification in list_group:
        if mess.lower().find(notification)!=-1:
            return 'group',1.0

    for notification in list_point:
        if mess.lower().find(notification)!=-1:
            return 'point',1.0

    for notification in list_sub_require:
        if mess.lower().find(notification)!=-1:
            return 'sub_require',1.0

    for notification in list_short_uni:
        if mess.lower().find(notification)!=-1:
            return 'code_name_uni',1.0

    return 'forward_fastai'
def clean_mess(mess):
    mess = re.findall(r'(?i)\b[a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ0-9]+\b', mess)
    messRepSpecToken = ' '.join(mess)
    return messRepSpecToken

def process_mess(data_path,mess):
    messRepSpecToken = clean_mess(mess)
    messNormUnicode=convert_unicode(messRepSpecToken)
    if check_question(data_path,messNormUnicode):
        info = intent_catch_pattern(data_path,messNormUnicode)
    return info
    # if info == 'forward_fastai' :


