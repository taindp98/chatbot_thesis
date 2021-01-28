from utils import *
from intent.intent_regconize import *
from entity.pattern_ner import *
from response.constants_response import *
"""
LIST INTENT PATTERN MATCHING
'major_code',
'duration',
'location',
'public_transport',
'accommodation',
'address',
'out_come',
'group',
'tuition',
'point',
'greet',
'farewell'

LIST INTENT FASTAI
'general_career',
'general_rate',
'general_company',
'general_major'
"""
def user_request(mess,state_tracker):
    confirm_obj = None
    if isinstance(mess, str):
        user_action = {}
        # clean câu nhập vào
        intent_catched, prob,mess_clean = catch_intent(mess)
        # kiểm tra câu nhập vào có phải câu hỏi
        # check_ques = check_question(mess_clean)
        ignore_intent = ['hello','done','other_intent','anything','thanks','not_intent']

        # request la intent
        if intent_catched not in ignore_intent:
            user_action['intent'] = 'request'
            user_action['inform_slots'],confirm_obj=find_all_entity(intent_catched,mess)
            user_action['request_slots'] = {intent_catched:'UNK'}
            
        elif intent_catched == 'not_intent':
            #get agent request key for user to inform (not intent)
            last_agent_action = state_tracker.history[-1]
            #nếu agent request 1 key thì user trả lời key đó
            if len(list(last_agent_action['request_slots'].keys())) > 0:
                user_inform_key = list(last_agent_action['request_slots'].keys())[0]
            #nếu agent inform 1 key thì user cũng inform lại key đó
            elif len(list(last_agent_action['inform_slots'].keys())) > 0:
                user_inform_key = list(last_agent_action['inform_slots'].keys())[0]

            if len(list(last_agent_action['request_slots'].keys())) > 0 or len(list(last_agent_action['inform_slots'].keys())) > 0:
                final_intent = user_inform_key + '_inform'
                # final_intent = user_inform_key
            else:
                final_intent = 'not_intent'
            intent_catched = 'inform'
            user_action['intent'] = intent_catched
            user_action['inform_slots'],confirm_obj=find_all_entity(final_intent,mess)
            user_action['request_slots'] = {}
            user_action['list_match_obj'] = {}
            # list_map_key = ['major_name', 'type_edu', 'career', 'subject','tuition', 'subject_group','satisfy', 'point','major_code','year']
            if user_inform_key in list_map_key:
                for key in list_map_key:
                    if key ==  user_inform_key:
                        user_action['list_match_obj'][key] = user_action['inform_slots'][user_inform_key]
                        # user_action['list_match_obj'][0][key] = user_action['inform_slots'][user_inform_key]
                    else:
                        user_action['list_match_obj'][key] = ''
                        # user_action['list_match_obj'][0][key] = ''

        elif intent_catched == 'anything':
            # mac dinh de tranh crash server
            anything_key = "major_name"
            user_action['intent'] = 'inform'
            user_action['inform_slots'] = {anything_key:'anything'}
            user_action['request_slots'] = {}
        else:
            user_action['intent'] = intent_catched
            user_action['inform_slots'] = {}
            user_action['request_slots'] = {}
    else:
        user_action = mess
    return user_action,confirm_obj

# if __name__=='__main__':
#     FOLDER_PATH = '/home/taindp/PycharmProjects/thesis/deep_q_learning_chatbot'
#     CONSTANTS_FILE_PATH = f'{FOLDER_PATH}/constants.json'
#     constants_file = CONSTANTS_FILE_PATH
#     with open(constants_file) as f:
#         constants = json.load(f)
#     file_path_dict = constants['db_file_paths']
#     DATABASE_FILE_PATH = file_path_dict['database']
#     database= json.load(open(DATABASE_FILE_PATH,encoding='utf-8'))
#     state_tracker = StateTracker(database, constants)
#     mess1 = 'em dự định thi khối d7 thì nên học ngành nào ạ'
#     dqn_agent = DQNAgent(state_tracker.get_state_size(), constants)
#     print(user_request(mess1,state_tracker))
