import re
import random
import warnings

from utils import check_match_sublist_and_substring
warnings.filterwarnings('ignore')

from response.constants_response import *

def get_greeting_statement():
    return random.choice(GREETING)
def response_craft(agent_action, state_tracker, confirm_obj,isGreeting=False):
    sentence_pattern = None
    if isGreeting:
        return random.choice(GREETING)
    agent_intent = agent_action['intent']
    if agent_intent == "inform":
        ############ TO DO : lấy list_match_obj ra inform cho user (dạng câu) (ok)
        # list_match_obj = agent_action['list_match_obj']
        inform_slot = list(agent_action['inform_slots'].keys())[0]
        if agent_action['inform_slots'][inform_slot] == 'no match available':
            return random.choice(NOT_FOUND)

        #check lai
        sentence_pattern = random.choice(INFORM[inform_slot])

        sentence = sentence_pattern.replace("*{}*".format(inform_slot), AGENT_INFORM_OBJECT[inform_slot])

        if len(agent_action['inform_slots'][inform_slot]) > 1:
            inform_value = ",\n".join(agent_action['inform_slots'][inform_slot])
            sentence = sentence.replace("*{}_instance*".format(inform_slot), "\n\"{}\"".format(inform_value))

        elif len(agent_action['inform_slots'][inform_slot]) == 1:

            inform_value = agent_action['inform_slots'][inform_slot][0]
            sentence = sentence.replace("*{}_instance*".format(inform_slot), "\"{}\"".format(inform_value))
        else:
            sentence_pattern = random.choice(EMPTY_SLOT)
            sentence = sentence_pattern.replace("*request_slot*", inform_slot)
        response_obj = ''
        # if list_match_obj != []:
        #     # response_obj += "Cụ thể các công việc sẽ là (kèm theo thời gian, địa điểm, địa chỉ):\n"
        #     response_obj += "Cụ thể các thông tin về ngành này là:\n"
        #     for obj_map_match in list_match_obj:
        #         response_obj += "************************************************* \n"
        #         for key in list_map_key:
        #             response_obj += "+ {0} : {1} \n".format(AGENT_INFORM_OBJECT[key], ', '.join(obj_map_match[key]))
        # sentence += response_obj
        # print(sentence_pattern)
    elif agent_intent == "request":
        request_slot = list(agent_action['request_slots'].keys())[0]
        # sentence_pattern = random.choice(REQUEST[request_slot])
        # sentence = sentence_pattern.replace("*{}*".format(request_slot), AGENT_REQUEST_OBJECT[request_slot])
        # print(sentence_pattern)
        check_request_repeat = False
        list_agent_request = state_tracker.list_agent_request
        for i in range(len(list_agent_request) - 1):
            history_request_slot = list(list_agent_request[i]['request_slots'].keys())[0]
            if history_request_slot == request_slot:
                check_request_repeat = True
        if check_request_repeat:
            sentence_pattern = random.choice(REQUEST_REPEAT)
            sentence = sentence_pattern.replace('*request_key*', AGENT_REQUEST_OBJECT[request_slot])
        else:
            sentence_pattern = random.choice(REQUEST[request_slot])
            sentence = sentence_pattern.replace("*{}*".format(request_slot), AGENT_REQUEST_OBJECT[request_slot])
            # print(sentence_pattern)
    elif agent_intent == "done":
        return random.choice(DONE)
    elif agent_intent == "match_found":
        ########### TO DO : lấy list_match_obj ra inform cho user (dạng câu)
        # list_match_obj = agent_action['list_match_obj']
        # assert len(state_tracker.current_request_slots) > 0
        inform_slot = state_tracker.current_request_slots[0]
        if agent_action['inform_slots']['activity'] == "no match available":
            sentence_pattern = random.choice(MATCH_FOUND['not_found'])
            sentence = sentence_pattern.replace("*found_slot*", AGENT_INFORM_OBJECT[inform_slot])
        else:
            key = agent_action['inform_slots']['activity']
            first_result_data = agent_action['inform_slots'][key][0]

            # #nếu là câu hỏi intent confirm thì cần response lại mà match hay không
            # print("-------------------------------inform slot :{}".format(inform_slot))
            # print("---------------------------------confirm obj: {}".format(confirm_obj))
            response_match = ''
            if confirm_obj != None:
                if inform_slot not in list_map_key:
                    check_match = check_match_sublist_and_substring(confirm_obj[inform_slot],first_result_data[inform_slot])
                # else: #nếu là 4 key map
                #     check_match = check_match_sublist_and_substring(confirm_obj[inform_slot],first_result_data[inform_slot])
                #     # neu chưa match với key chung thì tìm trong map
                #     if not check_match:
                #         if "time_works_place_address_mapping" in first_result_data and first_result_data["time_works_place_address_mapping"] not in [None,[]]:
                #             list_obj_map = first_result_data["time_works_place_address_mapping"]
                #             for obj_map in list_obj_map:
                #                 if inform_slot in obj_map:
                #                     if check_match_sublist_and_substring(confirm_obj[inform_slot],obj_map[inform_slot]):
                #                         check_match = True
                #                         break

                value_match = ''
                if len(confirm_obj[inform_slot]) > 1:
                    value_match = ',\n'.join(confirm_obj[inform_slot])
                else:
                    value_match = confirm_obj[inform_slot][0]
                if check_match:
                    response_match = "\n \n Đúng rồi! {0} là {1}".format(AGENT_INFORM_OBJECT[inform_slot],value_match)
                else:
                    response_match = "\n \n Sai rồi! {0} không là {1}".format(AGENT_INFORM_OBJECT[inform_slot],value_match)
            if inform_slot != "major":
                sentence_pattern = random.choice(MATCH_FOUND['found'])
                sentence = sentence_pattern.replace("*found_slot*", AGENT_INFORM_OBJECT[inform_slot])
                if len(first_result_data[inform_slot]) > 1:
                    inform_value = ",\n".join(first_result_data[inform_slot])
                    sentence = sentence.replace("*found_slot_instance*", "\n\"{}\"".format(inform_value))
                elif len(first_result_data[inform_slot]) == 1:
                    inform_value = first_result_data[inform_slot][0]
                    sentence = sentence.replace("*found_slot_instance*", "\"{}\"".format(inform_value))
                else: #slot mà user request của kết quả trả về là list rỗng
                    # inform_value = "không có thông tin này"
                    sentence = EMPTY_SLOT[0].replace("*request_slot*",AGENT_INFORM_OBJECT[inform_slot])
            else:
                sentence = random.choice(MATCH_FOUND['found_major'])
            response_obj = ''
            # list_obj_map_match = []
            # if list_match_obj != []:
            #     response_obj += "Cụ thể các thông tin về ngành này là:\n"
            #     for obj_map_match in list_match_obj:
            #         response_obj += "************************************************* \n"
            #         for key in list_map_key:
            #             response_obj += "+ {0} : {1} \n".format(AGENT_INFORM_OBJECT[key], ', '.join(obj_map_match[key]))
            # # print(sentence)
            sentence += "\n" + response_obj + response_match
            print("-----------------------------match sentence")
            # print(sentence)
    return sentence

# print(response_craft({'intent': 'inform', 'inform_slots': {'major_name': ['điện tử']}, 'request_slots': {}, 'round': 1, 'speaker': 'Agent'}))
