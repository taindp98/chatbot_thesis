from utils import *
from intent.intent_regconize import catch_intent
from entity.pattern_ner import *
from constant_general import list_map_key
from nlg.constants_response import *
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
def get_user_request(mess,state_tracker):
    confirm_obj = None
    if isinstance(mess, str):
        user_action = {}
        # clean câu nhập vào
        intent_catched, prob,mess_clean = catch_intent(mess)
        # print("intent_catched",intent_catched)
        # kiểm tra câu nhập vào có phải câu hỏi
        # check_ques = check_question(mess_clean)
        ignore_intent = ['hello','done','other','anything','thanks','not_intent']

        ## add intent agree or disagree

        ignore_intent.append('agree')
        ignore_intent.append('disagree')

        # request la intent
        if intent_catched not in ignore_intent:
            user_action['intent'] = 'request'
            user_action['inform_slots'],confirm_obj=find_all_entity(intent_catched,mess)
            user_action['request_slots'] = {intent_catched:'UNK'}

        # elif intent_catched == 'not_intent' or intent_catched == 'other':
        elif intent_catched in ['not_intent','other']:
            if state_tracker.history:
                last_agent_action = state_tracker.history[-1]

                # print(last_agent_action)
                #nếu agent request 1 key thì user trả lời key đó
                user_inform_key = None
                slot_inform = None
                if len(list(last_agent_action['request_slots'].keys())) > 0:
                    user_inform_key = list(last_agent_action['request_slots'].keys())[0]

                #nếu agent inform 1 key thì user cũng inform lại key đó
                elif len(list(last_agent_action['inform_slots'].keys())) > 0:
                    user_inform_key = list(last_agent_action['inform_slots'].keys())[0]
                if len(list(last_agent_action['request_slots'].keys())) > 0 or len(list(last_agent_action['inform_slots'].keys())) > 0:
                    final_intent = user_inform_key + '_inform'
                else:
                    final_intent = 'not_intent'
                user_action['inform_slots'],confirm_obj=find_all_entity(final_intent,mess)
                user_action['intent'] = 'inform'
                user_action['request_slots'] = {}
            else:
                # tránh crash
                other_key_avoid_crash = 'major_name'
                user_action['intent'] = 'inform'
                user_action['inform_slots'] = {other_key_avoid_crash:'anything'}
                user_action['request_slots'] = {}
        elif intent_catched in ['agree','disagree']:
            last_agent_action = state_tracker.history[-1]
            # print(last_agent_action)
            #nếu agent request 1 key thì user trả lời key đó
            user_inform_key = None
            slot_inform = None
            # if len(list(last_agent_action['request_slots'].keys())) > 0:
            #     user_inform_key = list(last_agent_action['request_slots'].keys())[0]

            #nếu agent inform 1 key thì user cũng inform lại key đó
            if len(list(last_agent_action['inform_slots'].keys())) > 0:
                user_inform_key = list(last_agent_action['inform_slots'].keys())[0]
            if len(list(last_agent_action['request_slots'].keys())) > 0 or len(list(last_agent_action['inform_slots'].keys())) > 0:
                final_intent = user_inform_key + '_inform'
            else:
                final_intent = 'not_intent'
            # user_action['inform_slots'],confirm_obj=find_all_entity(final_intent,mess)
            user_action['intent'] = 'inform'
            user_action['request_slots'] = {}

            if intent_catched == 'agree':
                user_action['inform_slots'] = dict(last_agent_action['inform_slots'].items())
            else:
                ## fix entity

                dict_fix_entity,confirm_obj = find_all_entity(final_intent,mess)

                if not dict_fix_entity:
                    user_action['inform_slots'] = {}
                    user_action['inform_slots'][user_inform_key] = 'anything'
                else:
                    user_action['inform_slots'] = dict_fix_entity

            # if user_inform_key in list_map_key:
            #     for key in list_map_key:
            #         if key ==  user_inform_key:
            #             user_action['list_match_obj'][0][key] = result_entity_dict[user_inform_key]
            #         else:
            #             user_action['list_match_obj'][0][key] = ''

        elif intent_catched == 'anything':
            anything_key = None
            last_agent_action = state_tracker.history[-1]
            if len(list(last_agent_action['request_slots'].keys())) > 0:
                anything_key = list(last_agent_action['request_slots'].keys())[0]
            elif len(list(last_agent_action['inform_slots'].keys())) > 0:
                anything_key = list(last_agent_action['inform_slots'].keys())[0]
            # mac dinh de tranh crash server
            if not anything_key:
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
