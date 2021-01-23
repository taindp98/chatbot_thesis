from utils import *
import json
from intent.intent_regconize import *
from collections import OrderedDict
"""
    0 là review ngành có nên học không --> satify
    1 là review ngành ra trường làm gì --> career
    all_slot = ['major_name', 'type_edu', 'career', 'subject','tuition_one_credit', 'subject_group', 'satisfy', 'point','major_code','year']
    user_known = ['major_name', 'type_edu','subject','subject_group','point', 'year']
"""
map_order_entity = {}

# intent pattern matching
# tìm ngành
map_order_entity['major_name'] = ['point','subject_group','career']

# xin mã ngành = tên ngành/program/khối
map_order_entity['major_code']=['major_name','subject_group']
# xin điểm = tên ngành/khối/program
map_order_entity['point']=['major_name','subject_group','year']
# xin khối = subject/tên ngành
map_order_entity['subject_group']=['major_name','subject']

map_order_entity['type_edu']=['major_name','subject_group','subject']

map_order_entity['subject']=['major_name','subject_group']
map_order_entity['tuition']=['major_name','type_edu']

map_order_entity['year'] = ['major_name','subject_group','point','subject']
# intent fastai

map_order_entity['satisfy']=['major_name','subject_group','subject','point','career']
map_order_entity['career']=['major_name','subject','subject_group']

# bổ sung intent là INFORM cho user_request:
map_order_entity['not_intent']=['major_code', 'major_name', 'subject_group', 'point', 'type_edu', 'year', 'satisfy', 'subject', 'career', 'tuition']
entity_path = '/home/taindp/PycharmProjects/thesis/data/db_entity_jan23.json'
with open(entity_path,'r') as jsonfile:
    dict_entity = json.load(jsonfile)[0]

# print(dict_entity['type_edu'])
def find_all_entity(intent,input_sentence):
    # with open(entity_path,'r') as jsonfile:
    #     dict_entity = json.load(jsonfile)
    normalized_input_sentence = convert_unicode(input_sentence)
    result_entity_dict={}
    list_order_entity_name=map_order_entity[intent]
    map_entity_name_to_threshold={}
    for entity_name in list_order_entity_name:
        # tìm chiều dài ngắn nhất cho từng entity
        # chung cho tất cả order
        # {'major_code': 1,
        # 'major_name': 2,
        # 'subject_group': 1,
        # 'point': 1,
        # 'type_edu': 4,
        # 'year': 1,
        # 'rate': 1,
        # 'university_name': 13,
        # 'sub1': 1,
        # 'sub2': 1,
        # 'sub3': 1,
        # 'career': 1,
        # 'typical_group': 1,
        # 'company': 0,
        # 'tuition_one_credit': 4,
        # 'tuition_avg_one_sem': 4,
        # 'duration_std': 1,
        # 'credits': 1,
        # 'foreign_lang_min': 2}
        all_slot = ['major_name', 'type_edu', 'career', 'subject','tuition', 'subject_group', 'satisfy', 'point','major_code','year']

        # if entity_name in ['major_code','subject_group','point','year','rate','subject','typical_group','company','duration_std','credits','foreign_lang_min']:
        # threshold wordnumber
        if entity_name in ['type_edu', 'career', 'subject','tuition', 'subject_group','point','major_code','year']:
            map_entity_name_to_threshold[entity_name]=1
        elif entity_name in ['major_name']:
            map_entity_name_to_threshold[entity_name]=2
        else:
            map_entity_name_to_threshold[entity_name]=4

    ordered_real_dict = OrderedDict()
    for entity_name in map_order_entity[intent]:
        # print(entity_name)
        ordered_real_dict[entity_name] = dict_entity[entity_name]
    for entity_name, list_entity in ordered_real_dict.items():
        # phân biệt cho từng order
        if entity_name == "major_name":
            matching_threshold = 0.2
        elif entity_name == 'type_edu':
            matching_threshold = 0.2
        else:
            matching_threshold = 0.5
        catch_entity_threshold_loop = 0
        while True:
            if catch_entity_threshold_loop > 3:
                break
            list_dict_longest_common_entity = find_entity_longest_common(normalized_input_sentence,list_entity,entity_name)
            if list_dict_longest_common_entity == []:
                break
            if list_dict_longest_common_entity[0]['longest_common_length'] < map_entity_name_to_threshold[entity_name] :
                break

            list_sentence_token = normalized_input_sentence.split(' ')
            greatest_entity_index=None
            greatest_common_length = None
            greatest_end_common_index = None
            max_match_entity = 0.0
            for dict_longest_common_entity in list_dict_longest_common_entity:
                longest_common_entity_index = dict_longest_common_entity['longest_common_entity_index']
                longest_common_length = dict_longest_common_entity['longest_common_length']
                end_common_index = dict_longest_common_entity['end_common_index']
                list_sentence_token_match = list_sentence_token[end_common_index - longest_common_length+1:end_common_index+1]

                list_temp_longest_entity_token = str(list_entity[longest_common_entity_index]).split(' ')
                score = len(list_sentence_token_match)/float(len(list_temp_longest_entity_token))
                # print(score)
                if score > max_match_entity:
                    max_match_entity = score
                    greatest_entity_index = longest_common_entity_index
                    greatest_common_length = longest_common_length
                    greatest_end_common_index = end_common_index
            if greatest_common_length >= map_entity_name_to_threshold[entity_name] and max_match_entity > matching_threshold:
                result = ' '.join(list_sentence_token[greatest_end_common_index - greatest_common_length +1 :greatest_end_common_index +1])

                if entity_name in result_entity_dict:
                    result_entity_dict[entity_name].append(result)
                else:
                    result_entity_dict[entity_name] = [result]
                list_sentence_token[greatest_end_common_index - greatest_common_length +1 :greatest_end_common_index +1] = ["✪"]*greatest_common_length
                normalized_input_sentence = ' '.join(list_sentence_token)
            catch_entity_threshold_loop = catch_entity_threshold_loop + 1
    if intent == 'point':
        result_entity_dict['point'] = catch_point(input_sentence)
    confirm_obj = None
    if intent in result_entity_dict:
        value = result_entity_dict.pop(intent)
        confirm_obj = {intent:value}
    return result_entity_dict,confirm_obj

# mess = 'cho em hỏi điểm ngành hóa học năm nay có tầm 25 điểm không ạ'
# intent_catched, prob,mess_clean = catch_intent(mess)
# entity_dict,confirm = find_all_entity(intent_catched,mess)
# print(confirm)
