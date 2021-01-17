#!/usr/bin/env python
# coding: utf-8

# from sklearn.externals import joblib
import numpy as np
from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from fastai.text import *
import torch
import numpy as np
# from sklearn.externals import joblib
from sklearn import preprocessing
import joblib
import os.path
from collections import OrderedDict

current_path = os.path.abspath(os.path.dirname(__file__))
TAGS = OrderedDict()
TAGS.update([('normal', 'O'),
             ('addr_street', 'STREET'),
             ('addr_district', 'DISTRICT'),
             ('addr_city', 'CITY'),
             ('addr_ward', 'WARD'),
             ('position', 'POSITION'),
             ('area', 'AREA'),
             ('price', 'PRICE'),
             ('transaction_type', 'TRANSACTION_TYPE'),
             ('realestate_type', 'REAL_ESTATE_TYPE'),
             ('legal', 'LEGAL'),
             ('potential', 'POTENTIAL'),
             ('surrounding', 'SURROUNDING_PLACE'),
             ('surrounding_characteristics', 'SURROUNDING_CHARACTERISTIC'),
             ('surrounding_name', 'SURROUNDING_NAME'),
             ('interior_floor', 'FLOOR'),
             ('interior_room', 'ROOM'),
             ('orientation', 'ORIENTATION'),
             ('project', 'PROJECT')])
SPLIT_TOKEN = ' '
B_TOKEN = 'B-{}'
I_TOKEN = 'I-{}'
WORD_TAG_SEPARATOR = '\t'
CHARACTER_SEPARATOR = '|'
ALL_TEXTS = 'all_text.txt'
WORD_VEC_PATH = './output/word_vec.bin'
REVERSE_TAGS = {v: k for k, v in TAGS.items()}

def tags2classes(tags):
    i = 0
    result = {}
    for value in tags:
        if value == TAGS['normal']:
            result[value] = str(i)
            i += 1
        else:
            result[B_TOKEN.format(value)] = str(i)
            result[I_TOKEN.format(value)] = str(i+1)
            i += 2
    return result


CLASSES = tags2classes(TAGS.values())
NUM_CLASSES = len(CLASSES)

#MODEL LANGUAGE, CLASSIFIER
CONST_THRESHOLD=0.4
list_label=['contact','register','activity','work','joiner']
le = preprocessing.LabelEncoder()
y = le.fit_transform(list_label)
vocab = torch.load(os.path.join(current_path,'saved_model/new_vocab.h5'))
lm = get_language_model(AWD_LSTM, 27498)
lm.eval()
lm.load_state_dict(torch.load(os.path.join(current_path,"saved_model/model_cpu_add_new_vocab.pth")))
clf = joblib.load(os.path.join(current_path,'saved_model/lm_kernel_linear_svm_classifier_final.pkl'))
emb_sz=lm[0].emb_sz

#INTENT PATTERN MATCHING SIGNAL
list_name_place_notification=["nơi","tại đâu","địa điểm diễn ra","tại chỗ nào","ở đâu","chỗ nào","tại đâu","khu nào","địa điểm của","địa điểm nào","chỗ diễn ra","chỗ đâu","khu tổ chức","là ở","là tại","là nơi","là tập trung tại","là diễn ra tại","là diễn ra ở"]
list_address_notification=["ấp nào","phường nào","xã nào","quận nào","huyện nào","thành phố nào","tỉnh nào","đường nào","đường gì","số mấy","địa chỉ nào","địa chỉ","tên đường","số nhà","phường mấy","quận mấy","số mấy"]
list_type_activity_notification=["loại hoạt động","loại nào","loại gì","kiểu hoạt động","kiểu gì","kiểu nào"]
list_name_activity_notification=["tên gì","tên là gì","tên hoạt động là gì","tên hoạt động"] #check lai
list_time_notification=["là tháng","là ngày","là vào","tháng mấy","thứ mấy","là diễn ra vào","là diễn ra lúc","ngày mấy","khi nào","lúc nào","thời gian nào","ngày nào","ngày bao nhiêu","giờ nào","giờ bao nhiêu","mấy giờ","mấy h ","thời gian"]
list_holder_notification=["ban tổ chức","btc","ai tổ chức","đơn vị nào tổ chức","đơn vị tổ chức","trường nào tổ chức","clb nào tổ chức","câu lạc bộ nào tổ chức","người tổ chức","tổ chức hả","tổ chức phải không","tổ chức đúng không"]
list_reward_notification=["có được drl",'có được đrl','có được điểm rèn luyện',"được thứ gì","bao nhiêu tiền","thưởng cái gì","được lợi gì","mấy ngày ctxh","mấy điểm rèn luyện","mấy drl","mấy đrl","mấy ngày công tác xã hội","bao nhiêu ngày ctxh","bao nhiêu ctxh","bao nhiêu điểm rèn luyện","bao nhiêu drl","bao nhiêu đrl","bao nhiêu ngày công tác xã hội","có ích gì","điểm rèn luyện","được công tác xã hội","được ctxh","được thưởng gì","được gì","được cái gì","có lợi gì","lợi ích","phần thưởng","được quà gì","tặng gì","được bao nhiêu","số tiền","có được ctxh","có được ngày công tác xã hội","có được ngày ctxh","có được tặng","có được thưởng","có được cho","là được ctxh","là được ngày công tác xã hội","là được ngày ctxh","là được tặng","là được thưởng","là được cho"]



#INTENT MESSAGE SIGNALS
list_question_signal = [" hả ","chứ","có biết","phải không","đâu","là sao","nào","khi nào","nơi nào","không ạ","k ạ","là sao","nữa vậy","chưa á","ko ạ","sao ạ","chưa ạ","sao vậy","không vậy","k vậy","ko vậy","chưa vậy","thế"," nhỉ "," ai"," ai ","ở đâu","ở mô","đi đâu","bao giờ","bao lâu","khi nào","lúc nào","hồi nào","vì sao","tại sao","thì sao","làm sao","như nào","thế nào","cái chi","gì","bao nhiêu","mấy","?"," hả ","được không","được k","được ko","vậy ạ","nào vậy","nào thế","nữa không","đúng không","đúng k","đúng ko","nữa k","nữa ko","nào ấy","nào ạ"]
list_question_signal_last = ["vậy","chưa","không","sao","à","hả","nhỉ","thế"]
list_object = ["bạn","cậu","ad","anh","chị","admin","em","mày","bot"]
list_subject = ["mình","tôi","tớ","tao","tui","anh","em"]
list_verb_want = ["hỏi","biết","xin"]
list_verb_have = ["có","được"]


#intent not want information
list_hello_notification = [" hi ","hello","chào","helo"]
list_done_notification = ["bye","tạm biệt","bai","gặp lại"]
list_thanks_notification = ["cảm ơn","tks","thanks",'thank']
list_anything_notification = ["sao cũng được","gì cũng được","anything","s cũng được",\
    'j cũng được',"không biết","k biết","ko biết","không nhớ","ko nhớ","k nhớ","không rõ",\
        "k rõ","ko rõ","cũng được","cũng ok","cũng không sao","cũng dc","cũng k sao","cũng ko sao"]


#map
list_map_key = ["works", "name_place", "address", "time"]



#indicator
list_joiner_indicator = ["có được tham gia","có được tham dự","có được đi",\
                        "được tham gia","được tham dự","được đi","tham gia","tham dự"]

map_entity_name_to_list_noti_anything = {
    'time':['thời gian',"lúc"],
    'name_activity':['tên hoạt động',"tên"],
    'type_activity':["loại hoạt động","loại"],
    'holder':["tổ chức","đơn vị"],
    'name_place':["địa điểm","chỗ","nơi"],
    'address':["địa chỉ","đường","quận","phường"],
    'contact':["liên hệ","liên lạc"],
    'works':["việc","làm"],
    'register':["đăng ký","đăng kí"],
    'reward':["thưởng","lợi ích"],
    'joiner':["đối tượng","ai tham gia","người nào tham gia"]
}


#dictionary
with open('real_dict_2000_new_only_delete_question_noti_new_and_space_newest.json','r') as real_dict_file:
    real_dict = json.load(real_dict_file)
    real_dict_file.close()

with open('list_constants.json','r') as list_file:
    list_file_obj = json.load(list_file)
    list_extra_word = list_file_obj['list_extra_word']

    list_pattern_time = list_file_obj['list_pattern_time']
    list_pattern_reward = list_file_obj['list_pattern_reward']


#works -> []
map_intent_to_list_order_entity_name = {
    'time':['name_activity','type_activity', 'time','name_place', \
                            'holder', 'address'],
    'name_activity':['name_activity','type_activity', 'time', 'name_place', \
                            'holder', 'address','reward','works'],
    'type_activity':['name_activity','type_activity','time', 'name_place',  \
                            'holder', 'address', 'works'\
                            , 'reward'],
    'holder':['name_activity', 'type_activity','time', 'name_place', \
                            'holder', 'address'],
    'name_place':['name_activity','type_activity','time',  'name_place','holder', \
                             'address'],
    'address':['address', 'name_activity','type_activity','time', 'name_place', \
                            'holder'],
    'contact':['contact','name_activity', 'type_activity','time', 'name_place',  \
                            'holder', 'address'],
    'works':['name_activity','type_activity','time', 'name_place', 'works', \
                            'holder', 'address'],
    'register':['name_activity','type_activity','time', 'name_place',  \
                            'holder', 'address','register'],
    'reward':[ 'name_activity','type_activity','name_place','reward','time', \
                            'holder', 'address'],
    'joiner':['name_activity', 'type_activity','time','name_place','joiner', \
                            'holder', 'address'\
                            ],\
    'activity':['name_activity', 'type_activity','time','name_place', \
                            'reward','holder', 'address'\
                            ],\
    'not intent':['name_activity','type_activity','time', 'name_place', \
                            'holder', 'address','contact','register','reward','joiner','works'\
                            ],
    'time_inform':['time'],
    'name_activity_inform':['name_activity'],
    'type_activity_inform':['type_activity'],
    'holder_inform':['holder'],
    'name_place_inform':['name_place'],
    'address_inform':['address'],
    'contact_inform':['contact'],
    'works_inform':['works'],
    'register_inform':['register'],
    'reward_inform':['reward'],
    'joiner_inform':['joiner']
}

response_to_user_free_style = {
    'hello':["Chào bạn ^^ ! Chúc bạn một ngày tốt lành nè .",\
            "OK chào bạn nè ^^. Cần mình hỗ trợ gì nè ? :3"
        ],
    'other':["Huhu xin lỗi mình không hiểu ý bạn lắm :'( :'( ",\
            "Xin lỗi bạn, mình không hiểu ý bạn lắm nè ^^"
        ],
    'done':[
        "OK chào tạm biệt nha ^^ ! Rất vui được giúp bạn nè ",
        "Okie bái bai bạn nè ^^ ! Rất vui được giúp bạn nè ",
        "Bye bye nha ! :D Rất vui được giúp bạn nè "
    ]
}
if __name__ == '__main__':
    print(CLASSES)
