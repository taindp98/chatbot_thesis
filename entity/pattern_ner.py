from utils import *
import json
from intent.intent_regconize import *
from collections import OrderedDict
"""
    
    label = ['other_intent','type_edu','case','career']
"""
map_order_entity = {}

# intent pattern matching
# tìm ngành
map_order_entity['major_name'] = ['point','subject_group','career','criteria','object','register','case']
map_order_entity['major_code']=['major_name','subject_group']
map_order_entity['point']=['major_name','subject_group','year','type_edu','case']
map_order_entity['subject_group']=['major_name','subject']
map_order_entity['subject']=['major_name','subject_group']
map_order_entity['tuition']=['major_name','type_edu']
map_order_entity['year'] = ['major_name','subject_group','point','subject']
map_order_entity['object'] = ['case','type_edu','major_name','register']
map_order_entity['register'] = ['case','type_edu','major_name','object']
map_order_entity['criteria'] = ['major_name','case','object','register','subject_group','subject','type_edu','year']
# intent deep learning
# label = ['other','type_edu','case','career']
map_order_entity['type_edu']=['major_name','subject_group','subject','case','object','register','criteria']
map_order_entity['case']=['major_name','criteria','subject','subject_group','case','register','criteria']
map_order_entity['career']=['major_name','subject','subject_group']

# map_order_entity['other']=['major_name','type_edu','point','year','career','subject','tuition','subject_group','case','major_code','criteria','object','register']



# bổ sung intent là INFORM cho user_request:
map_order_entity['not_intent']=['major_name','type_edu','point','year','career','subject','tuition','subject_group','case','major_code','criteria','object','register']
map_order_entity['major_name_inform'] = ['major_name']
map_order_entity['major_code_inform'] = ['major_code']
map_order_entity['subject_group_inform'] = ['subject_group']
map_order_entity['point_inform'] = ['point']
map_order_entity['type_edu_inform'] = ['type_edu']
map_order_entity['year_inform'] = ['year']

map_order_entity['case_inform'] = ['case']
map_order_entity['criteria_inform'] = ['criteria']
map_order_entity['object_inform'] = ['object']
map_order_entity['register_inform'] = ['register']
map_order_entity['subject_inform'] = ['subject']
map_order_entity['career_inform'] = ['career']
map_order_entity['tuition_inform'] = ['tuition']


entity_path = './data/check_entity.json'
with open(entity_path,'r') as jsonfile:
    dict_entity = json.load(jsonfile)[0]

# print(dict_entity['type_edu'])
def find_all_entity(intent,input_sentence):
    # with open(entity_path,'r') as jsonfile:
    #     dict_entity = json.load(jsonfile)
    normalized_input_sentence = convert_unicode(input_sentence)
    result_entity_dict={}
    list_order_entity_name=map_order_entity[intent]
    # print(list_order_entity_name)
    map_entity_name_to_threshold={}
    for entity_name in list_order_entity_name:
        # threshold wordnumber
        if entity_name in ['type_edu', 'career', 'subject','tuition', 'subject_group','point','major_code','year']:
            map_entity_name_to_threshold[entity_name]=1
        else:
            map_entity_name_to_threshold[entity_name]=2
        # else:
            # map_entity_name_to_threshold[entity_name]=4

    ordered_real_dict = OrderedDict()
    for entity_name in map_order_entity[intent]:
        # print(entity_name)
        ordered_real_dict[entity_name] = dict_entity[entity_name]
    for entity_name, list_entity in ordered_real_dict.items():
        # phân biệt cho từng order
        if entity_name in ["major_name",'type_edu']:
            matching_threshold = 0.2
        elif entity_name == 'subject':
            matching_threshold = 0.55
        else:
            matching_threshold = 0.3
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
    # if intent == 'point':
    #     result_entity_dict['point'] = catch_point(input_sentence)
    confirm_obj = None
    if intent in result_entity_dict:
        value = result_entity_dict.pop(intent)
        confirm_obj = {intent:value}
    return result_entity_dict,confirm_obj

# mess = 'cho em hỏi ngành kỹ thật điện điện tử thì có cơ hội việc làm ra sao ạ'
# # intent_catched, prob,mess_clean = catch_intent(mess)
# entity_dict,confirm = find_all_entity('review',mess)
# print(entity_dict)
