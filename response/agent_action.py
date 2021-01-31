from dqn.user_simulator import UserSimulator
from dqn.error_model_controller import ErrorModelController
from dqn.dqn_agent import DQNAgent
from dqn.state_tracker import StateTracker
import pickle, argparse, json
from dqn.user import User
from dqn.utils import remove_empty_slots
from response.agent_response import *
import pymongo
def get_agent_action(state_tracker,dqn_agent,user_action,done=False):
    state_tracker.update_state_user(user_action)
    current_state = state_tracker.get_state(done)
    _, agent_action = dqn_agent.get_action(current_state)
    if 'round' not in agent_action.keys():
        state_tracker.update_state_agent(agent_action)
    else:
        if agent_action['round'] < 10:
            state_tracker.update_state_agent(agent_action)
        else:
            state_tracker.reset()
    # assert len(state_tracker.current_request_slots) > 0
#     if agent_action['intent'] == 'match_found':
# #         print("inform slot match found: {}".format(agent_action['inform_slots']))
#         agent_action['intent'] = 'inform'
# # #         try:
# #         user_request_slot = state_tracker.current_request_slots[0]
#         user_request_slot = list(user_action['request_slots'].keys())[0]
# # #         except:
# # #             print('Fail state tracker',state_tracker)
# #         # print("user request slot: {}".format(user_request_slot))
#
#         inform_value = agent_action['inform_slots'][user_request_slot]
#         agent_action['inform_slots'].clear()
#         agent_action['inform_slots'][user_request_slot] = inform_value
#         print("inform slot converted: {}".format(agent_action['inform_slots']))
    return agent_action



# if __name__ == '__main__':
#     user_action = {'intent': 'inform', 'request_slots': {'major_code': 'UNK'}, 'inform_slots': {'major_name': ['hóa học']}}
#     FOLDER_PATH = '/home/taindp/PycharmProjects/thesis/dqn'
#     CONSTANTS_FILE_PATH = f'{FOLDER_PATH}/constants.json'
#     constants_file = CONSTANTS_FILE_PATH
#     with open(constants_file) as f:
#         constants = json.load(f)
# #     file_path_dict = constants['db_file_paths']
# #     DATABASE_FILE_PATH = file_path_dict['database']
# #     database= json.load(open(DATABASE_FILE_PATH,encoding='utf-8'))
#     client = pymongo.MongoClient("mongodb://taindp:chatbot2020@thesis-shard-00-00.bdisf.mongodb.net:27017,thesis-shard-00-01.bdisf.mongodb.net:27017,thesis-shard-00-02.bdisf.mongodb.net:27017/<dbname>?ssl=true&replicaSet=atlas-12fynb-shard-0&authSource=admin&retryWrites=true&w=majority")
#     db = client.hcmut
#     collection = db['general'].find({})
#     # collection = db['general']
#     database = []
#     for item in collection:
#         database.append(item)
#     state_tracker = StateTracker(database, constants)
#     dqn_agent = DQNAgent(state_tracker.get_state_size(), constants)
#     done = False
#     # print(database)
#     agent_action = get_agent_action(state_tracker, dqn_agent, user_action,done)
#     print(agent_action)
    # print(response_craft(agent_action, state_tracker))
