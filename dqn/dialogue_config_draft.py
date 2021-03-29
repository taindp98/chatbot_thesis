# Special slot values (for reference)
'PLACEHOLDER'  # For informs
'UNK'  # For requests
'anything'  # means any value works for the slot with this value
'no match available'  # When the intent of the agent is match_found yet no db match fits current constraints

#######################################
# Usersim Config
#######################################
# Used in EMC for intent error (and in user)
usersim_intents = ['inform', 'request', 'thanks', 'reject', 'done']

# The goal of the agent is to inform a match for this key
usersim_default_key = 'activity'
# usersim_default_key = 'ticket'


# Required to be in the first action in inform slots of the usersim if they exist in the goal inform slots
# usersim_required_init_inform_keys = ['moviename']

usersim_required_init_inform_keys = ['name_activity']

#######################################
# Agent Config
#######################################

# Possible inform and request slots for the agent
# agent_inform_slots = ['moviename', 'theater', 'starttime', 'date', 'genre', 'state', 'city', 'zip', 'critic_rating',
#                       'mpaa_rating', 'distanceconstraints', 'video_format', 'theater_chain', 'price', 'actor',
#                       'description', 'other', 'numberofkids', usersim_default_key]
# agent_request_slots = ['moviename', 'theater', 'starttime', 'date', 'numberofpeople', 'genre', 'state', 'city', 'zip',
#                         'critic_rating', 'mpaa_rating', 'distanceconstraints', 'video_format', 'theater_chain', 'price',
#                         'actor', 'description', 'other', 'numberofkids']
agent_inform_slots =  ['name_activity', 'type_activity', 'holder', 'time', 'address', 'name_place',
                       'reward', 'contact', 'register', 'works', 'joiner',usersim_default_key]
agent_request_slots = ['name_activity', 'type_activity', 'holder', 'time', 'address', 'name_place',
                       'works']

# Possible actions for agent
agent_actions = [
    {'intent': 'done', 'inform_slots': {}, 'request_slots': {}},  # Triggers closing of conversation
    {'intent': 'match_found', 'inform_slots': {}, 'request_slots': {}}
]
for slot in agent_inform_slots:
    # Must use intent match found to inform this, but still have to keep in agent inform slots
    if slot == usersim_default_key:
        continue
    agent_actions.append({'intent': 'inform', 'inform_slots': {slot: 'PLACEHOLDER'}, 'request_slots': {}})
for slot in agent_request_slots:
    agent_actions.append({'intent': 'request', 'inform_slots': {}, 'request_slots': {slot: 'UNK'}})
print("agent action total: {}".format(len(agent_actions)))
# Rule-based policy request list
# rule_requests = ['moviename', 'starttime', 'city', 'date', 'theater', 'numberofpeople']
# rule_requests = ['name_activity', 'contact', 'works', 'joiner', 'register']
# rule_requests=['name_activity', 'type_activity', 'holder', 'time', 'city', 'district', 'ward', 'name_place', 'street',
#                        'reward', 'contact', 'register', 'works', 'joiner']
# These are possible inform slot keys that cannot be used to query
rule_requests = ['name_activity', 'type_activity', 'holder', 'time', 'address', 'name_place',
                       'works']
no_query_keys = [usersim_default_key,'_id']
# no_query_keys = ['numberofpeople',usersim_default_key]

#######################################
# Global config
#######################################

# These are used for both constraint check AND success check in usersim
FAIL = -1
NO_OUTCOME = 0
SUCCESS = 1
UNSUITABLE = -2
NO_VALUE = -3
GOOD_INFORM = 2
# All possible intents (for one-hot conversion in ST.get_state())
all_intents = ['inform', 'request', 'done', 'match_found', 'thanks', 'reject']

# All possible slots (for one-hot conversion in ST.get_state())
# all_slots = ['actor', 'actress', 'city', 'critic_rating', 'date', 'description', 'distanceconstraints',
#              'genre', 'greeting', 'implicit_value', 'movie_series', 'moviename', 'mpaa_rating',
#              'numberofpeople', 'numberofkids', 'other', 'price', 'seating', 'starttime', 'state',
#              'theater', 'theater_chain', 'video_format', 'zip', 'result', usersim_default_key, 'mc_list']
all_slots = ['name_activity', 'type_activity', 'holder', 'time', 'name_place', 'address',
                       'reward', 'contact', 'register', 'works', 'joiner',usersim_default_key]