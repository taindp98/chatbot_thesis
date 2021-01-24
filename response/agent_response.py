import re
import random
import warnings

from utils import check_match_sublist_and_substring
warnings.filterwarnings('ignore')
# from response.constants_response import list_map_key
list_map_key = ["major_name", "point", "subject_group","year"]
GREETING = [
    'Xin chào! Mình là BK Assistant. Mình có thể giúp gì được bạn?',
    'Hi! BK Assistant có thể giúp gì được bạn đây?'
]
DONE = [
    'Cảm ơn bạn, hy vọng bạn hài lòng với trải nghiệm vừa rồi! Bye ',
    'Rất vui được tư vấn cho bạn! Chào bạn nhé!',
    'Hy vọng bạn hài lòng với những gì mình tư vấn. Chào bạn!'
]
DONT_UNDERSTAND = [
    'Xin lỗi, mình không hiểu. Bạn nói cách khác dễ hiểu hơn được không?',
    'Mình không hiểu ý bạn lắm'
]

NOT_FOUND = [
    'Mình không tìm thấy ngành nào thỏa mãn các thông tin bạn đã cung cấp, vui lòng điều chỉnh lại giúp mình nhé!'
]
EMPTY_SLOT = [
    'Thông tin về ngành thỏa mãn điều kiện của bạn nhưng nó không đề cập đến thông tin *request_slot*'
]
def get_greeting_statement():
    return random.choice(GREETING)

MATCH_FOUND = {
    'found': [
        "Thông tin *found_slot* chung bạn cần: *found_slot_instance*, bên dưới là ngành cụ thể chứa thông tin đó và một số ngành khác cũng thỏa điều kiện bạn đưa ra"
    ],
    'not_found': [
        "Mình không tìm thấy ngành nào chứa thông tin *found_slot* mà bạn cần, bạn xem lại các thông tin đã cung cấp dưới đây và điều chỉnh lại giúp mình nhé!"
    ],
    'found_activity' :[
        "Dưới đây là thông tin bạn cần tìm."
    ]
}
REQUEST = {}
"""
user_known = ['major_name', 'type_edu','subject','subject_group','point', 'year']
# sửa lại dialogue train
'major_code',
'major_name',
'type_edu',
'point',
'subject_group',
'university_code',
'university_name',
'year',



'career',
'company',
'subject',
'tuition_one_credit',
'duration_std',
'credits',
'foreign_lang_min'
"""
###############################################################################################################
REQUEST['major_name'] = [
    'Bạn định hỏi về *major_name* nào? (khoa học máy tính, điện điện tử, cơ khí, ...)',
    '*major_name* là gì vậy bạn?',
    'Bạn cần thông tin về *major_name* nào?'
]
REQUEST['type_edu'] = [
    '*type_edu* bạn cần tìm là gì vậy ạ?',
    'Bạn muốn tìm thông tin về *type_edu* nào?'
]
REQUEST['point'] = [
    'Bạn muốn tra cứu mức *point* thế nào ạ?',
    'Bạn muốn tìm ngành với *point* tầm bao nhiêu ạ?',
    'Cho mình xin thêm thông tin về *point* mong muốn của bạn được không?'
]
REQUEST['subject_group'] = [
    'Bạn muốn tra cứu *subject_group* nào bạn?',
    'Cụ thể là *subject_group* nào vậy bạn?',
    'Mời bạn cung cấp thông tin *subject_group* '
]

REQUEST['subject'] = [
    'Bạn muốn tra cứu *subject* nào bạn?',
    'Cụ thể là *subject* nào vậy bạn?',
    'Mời bạn cung cấp thông tin *subject* '
]

REQUEST['year'] = [
    'Bạn cho mình xin *year* cụ thể bạn muốn tìm nha!',
    '*year* là bao nhiêu vậy bạn?'
]

REQUEST_REPEAT = [
    'Thông tin *request_key* bạn nhập vào chưa rõ ràng, bạn cung cấp lại giúp mình thông tin này nhé! ',
    'Rất tiếc, thông tin *request_key* bạn nhập vào mình vẫn chưa rõ, bạn vui lòng cung cấp lại thông tin này giúp mình nhé!',
    'Bạn cung cấp lại thông tin *request_key* giúp mình với nhé!'
]
################################################################################
"""
# sửa lại dialogue train
'major_code',
'major_name',
'type_edu',
'point',
'subject_group',
'university_code',
'university_name',
'year',
'typical_group',


'rate',
'career',
'company',
'subject',
'tuition_one_credit',
'tuition_avg_one_sem',
'duration_std',
'credits',
'foreign_lang_min'
"""
INFORM = {}
INFORM['major_code'] = [
    '*major_code_instance* là mã của ngành bạn cần tìm',
    '*major_code_instance* có phải là *major_code* bạn muốn tìm không?'
]
INFORM['major_name'] = [
    'ngành *major_name_instance* đó bạn',
    '*major_name_instance* có phải là *major_name* bạn muốn tìm không?'
]
INFORM['type_edu'] = [
    'có phải bạn muốn hỏi về chương trình *type_edu_instance* không?',
    '*type_edu_instance* có phải là *type_edu* bạn muốn tìm không?'
]
INFORM['point'] = [
    '*point_instance* điểm đó bạn'
]
INFORM['subject_group'] = [
    'có phải bạn muốn hỏi về *subject_group_instance* không?',
    '*subject_group_instance* có phải là *subject_group* bạn muốn tìm không?'
]

INFORM['year'] = [
    'năm *year_instance* đó bạn'
]

INFORM['career'] = [
    '*career_instance* là cơ hội nghề nghiệp của ngành bạn cần tìm'
]
INFORM['subject'] = [
    '*subject_instance* thuộc tổ hợp khối thi cho ngành bạn cần tìm'
]
INFORM['tuition'] = [
    '*tuition_instance* là mức học phí trên một tín chỉ của ngành bạn cần tìm'
]
INFORM['satisfy'] = [
    '*satisfy_instance* là mức độ hài lòng của sinh viên đang theo học ngành bạn cần tìm'
]
INFORM['major'] = [
    'Đây là ngành mình tìm được với yêu cầu hiện tại của bạn: *major_instance*'
]
"""
# sửa lại dialogue train
'major_code',
'major_name',
'type_edu',
'point',
'subject_group',
'university_code',
'university_name',
'year',
'typical_group'
"""
user_known = ['major_name', 'type_edu','subject','subject_group','point', 'year']
AGENT_REQUEST_OBJECT = {
    "major_name": "tên ngành",
    "type_edu": "chương trình đào tạo",
    "point": "điểm chuẩn",
    "subject_group": "tổ hợp khối",
    "subject": "môn thi",
    "year":"năm",
}
"""
# sửa lại dialogue train
'major_code',
'major_name',
'type_edu',
'point',
'subject_group',
'university_code',
'university_name',
'year',
'typical_group',


'rate',
'career',
'company',
'subject',
'tuition_one_credit',
'tuition_avg_one_sem',
'duration_std',
'credits',
'foreign_lang_min'
"""
AGENT_INFORM_OBJECT = {
    "major_code": "mã ngành",
    "major_name": "tên ngành",
    "type_edu": "chương trình đào tạo",
    "point": "điểm chuẩn",
    "subject_group": "khối thi",
    "year":"năm",
    "career": "cơ hội nghề nghiệp",
    "subject": "môn thi",
    "tuition": "giá học phí một tín chỉ",
    "satisfy": "sự hài lòng"
}


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
        assert len(state_tracker.current_request_slots) > 0
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
                sentence = random.choice(MATCH_FOUND['found_activity'])
            response_obj = ''
            list_obj_map_match = []
            if list_obj_map_match != []:
                response_obj += "Cụ thể các thông tin về ngành này là:\n"
                for obj_map_match in list_obj_map_match:
                    response_obj += "************************************************* \n"
                    for key in list_map_key:
                        response_obj += "+ {0} : {1} \n".format(AGENT_INFORM_OBJECT[key], ', '.join(obj_map_match[key]))


            # print(sentence)
            sentence += "\n" + response_obj + response_match
            print("-----------------------------match sentence")
            # print(sentence)
    return sentence

# print(response_craft({'intent': 'inform', 'inform_slots': {'major_name': ['điện tử']}, 'request_slots': {}, 'round': 1, 'speaker': 'Agent'}))
