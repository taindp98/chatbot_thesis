from utils import *
# import json
# from intent.intent_regconize import *
from entity.confirm_object import catch_point
from collections import OrderedDict

from entity.constants_ner import map_order_entity,list_entity
"""
    
    label = ['other_intent','type_edu','case','career']
"""
dict_entity = list_entity[0]

def find_all_entity(intent,mess_clean):
    normalized_input_sentence = mess_clean
    result_entity_dict={}
    list_order_entity_name=map_order_entity[intent]
    map_entity_name_to_threshold={}
    for entity_name in list_order_entity_name:
        # threshold wordnumber
        if entity_name in ['type_edu', 'subject','tuition', 'subject_group','major_code','year']:
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
        elif entity_name == 'case':
            matching_threshold = 0.15
        elif entity_name == 'subject':
            matching_threshold = 0.55
        else:
            matching_threshold = 0.1
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
    point_entity = catch_point(mess_clean)
    if point_entity:
        result_entity_dict['point'] = point_entity
    confirm_obj = None
    if intent in result_entity_dict:
        value = result_entity_dict.pop(intent)
        confirm_obj = {intent:value}
    return result_entity_dict,confirm_obj

# mess = 'có ngành nào điểm chuẩn tầm 25 điểm không ạ'
# intent_catched, prob,mess_clean = catch_intent(mess)
# entity_dict,confirm = find_all_entity('major_name',mess)
# print(entity_dict)
# print(confirm)
# print(list_entity[0]['object'])
