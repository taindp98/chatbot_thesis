# from utils import *
# # from collections import defaultdict
# # import random
# # import pymongo
# # import warnings
# # from nlg.user_request import *
# # from intent.intent_regconize import *
# # from pyvi import ViTokenizer, ViPosTagger
# # from tqdm import tqdm
# # from nlg.agent_response import *
# # from nlg.agent_action import *
# # from entity.pattern_ner import *
# # from datetime import datetime
# import re
# import flask
# import io
# import sys
# import pymongo
# from flask_pymongo import PyMongo
# from flask import Flask, request,render_template,jsonify
# from flask_cors import CORS
# from nlg.user_request import *
# from dqn.state_tracker import StateTracker
# from dqn.dqn_agent import DQNAgent
#
# from keras import backend as K
# from intent.intent_regconize import *
# from nlg.user_request import user_request
# from nlg.agent_action import get_agent_action
# from nlg.agent_response import response_craft
# from nlg.default_response import response_to_user_free_style
# import random
# from datetime import datetime
#
# import os
# from bs4 import BeautifulSoup
# # from mongoengine import connect
#
# app = Flask(__name__)
# # app.config["MONGO_URI"] = "mongodb://localhost:27017"
# os.environ["MONGOLAB_URI"] = 'mongodb://taindp:chatbot2020@thesis-shard-00-00.bdisf.mongodb.net:27017,thesis-shard-00-01.bdisf.mongodb.net:27017,thesis-shard-00-02.bdisf.mongodb.net:27017/hcmut?ssl=true&replicaSet=atlas-12fynb-shard-0&authSource=admin&retryWrites=true&w=majority'
# app.config['MONGO_URI'] = os.environ.get('MONGOLAB_URI')
# mongo = PyMongo(app)
# FOLDER_PATH = './dqn'
# CONSTANTS_FILE_PATH = f'{FOLDER_PATH}/constants.json'
# # CONSTANT_FILE_PATH = 'constants.json'
# with open(CONSTANTS_FILE_PATH) as f:
#     constants = json.load(f)
# client = pymongo.MongoClient(os.environ.get('MONGOLAB_URI'))
# db = client.hcmut
# collection = db['general'].find({})
# # collection = db['general']
# database = []
# re_pattern = r"\'.*?\'"
# for item in collection:
#     bad_id = item['_id']
#     good_id = str(bad_id)
#     item['_id'] = good_id
#     database.append(item)
# print(database)
# if __name__=='__main__':
#     # input_sentence='ngành điện tử đấy ạ'
#     mess='cho em hỏi ngành điện tử với ngành kỹ thuật hóa có năm 2019 hoặc 2020 tầm 24.25 điểm không ạ'
#     mess = 'anh chị cho em hỏi học phí tiên tiến ngành kỹ thuật hóa với ạ'
    # mess = 'tks'
    # print(check_shorted_entity('/home/taindp/Database/hcmut/db_entity_official.json'))
    # catch_point(input_sentence)
    # print((load_csvfile(os.path.join(path,'compare_point.csv'))))
    # CONSTANT_FILE_PATH = 'constants.json'
    # with open(CONSTANT_FILE_PATH) as f:
    #     constants = json.load(f)
    # file_path_dict = constants['db_file_paths']
    # DATABASE_FILE_PATH = file_path_dict['database']
    #
    # database= json.load(open(DATABASE_FILE_PATH,encoding='utf-8'))
    # print(database)
    # state_tracker = StateTracker(database, constants)
    # intent_catched,_,mess = catch_intent(mess)
    # print(find_all_entity(intent_catched,mess))
    # print(state_tracker.history)

    # print((ViPosTagger.postagging('Chelsea cần chiến thắng trước Stoke City ở Stamford Bridge để cân bằng kỷ lục 13 chiến thắng của Arsenal ở cuối mùa 2001/02. Cuối cùng, đoàn quân của HLV Conte đã hoàn thành nhiệm vụ này khi vượt qua đối thủ với tỷ số 4-2')))
    # print(catch_intent(mess))
# if __name__ == '__main__':
#     text = "ObjectId('60484802f66da7ba0324ce31')"
#     re_pattern = r"\'.*?\'"
#     print(re.findall(re_pattern,text)[0])
    # now = datetime.now()
    # date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
    # print(date_time)
#     warnings.filterwarnings('ignore')
#     # user_action = {'intent': 'inform', 'request_slots': {'major_code': 'UNK'}, 'inform_slots': {'major_name': ['hóa học']}}
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
#     # mess = 'cho em hỏi em muốn  thi ngành bảo dưỡng công nghiệp thì nên tập trung học môn nào ạ'
#     mess = 'đúng rồi ạ'
#     user_action,confirm_obj = (user_request(mess,state_tracker))
#     # print(database)
#
#     print(user_action)
    # agent_action = get_agent_action(state_tracker, dqn_agent, user_action)
    # print(agent_action)
    # print(response_craft(agent_action, state_tracker,confirm_obj))

# from dqn.dialogue_config import all_intents
# print(all_intents)
# agent_action = {'intent': 'match_found', 'inform_slots': {'60588c802c992394968d36d5': [{'_id': '60588c802c992394968d36d5', 'major_code': ['266'], 'major_name': ['khoa học máy tính'], 'type_edu': ['chất lượng cao', 'tiên tiến'], 'point': [24.0], 'year': ['2020'], 'career': ['thiết kế xây dựng các phần mềm máy tính', 'thiết kế xây dựng các ứng dụng cho thiết bị di động', 'ứng dụng thương mại điện tử trên nền web', 'quản trị và xây dựng các giải pháp đảm bảo an toàn cho các hệ thống máy tính và hệ thống mạng máy tính', 'tư vấn thẩm định và phát triển các dự án giải pháp công nghệ thông tin'], 'subject': ['toán', 'vật lý', 'tiếng anh'], 'tuition': ['30.000.000'], 'subject_group': ['a01', 'a1'], 'case': ['thi tốt nghiệp trung học phổ thông'], 'criteria': [40], 'object': ['thi tốt nghiệp thpt năm 2021'], 'register': ['đăng ký dự thi kỳ thi tốt nghiệp thpt 2021', 'đăng ký xét tuyển']}, {'_id': '60588c802c992394968d36c2', 'major_code': ['266'], 'major_name': ['khoa học máy tính'], 'type_edu': ['chất lượng cao', 'tiên tiến'], 'point': [24.0], 'year': ['2020'], 'career': ['thiết kế xây dựng các phần mềm máy tính', 'thiết kế xây dựng các ứng dụng cho thiết bị di động', 'ứng dụng thương mại điện tử trên nền web', 'quản trị và xây dựng các giải pháp đảm bảo an toàn cho các hệ thống máy tính và hệ thống mạng máy tính', 'tư vấn thẩm định và phát triển các dự án giải pháp công nghệ thông tin'], 'subject': ['toán', 'vật lý', 'hóa học'], 'tuition': ['30.000.000'], 'subject_group': ['a00', 'a'], 'case': ['thi tốt nghiệp trung học phổ thông'], 'criteria': [40], 'object': ['thi tốt nghiệp thpt năm 2021'], 'register': ['đăng ký dự thi kỳ thi tốt nghiệp thpt 2021', 'đăng ký xét tuyển']}, {'_id': '60588c802c992394968d36cd', 'major_code': ['106'], 'major_name': ['khoa học máy tính'], 'type_edu': ['chính quy', 'đại trà'], 'point': [28.0], 'year': ['2020'], 'career': ['thiết kế xây dựng các phần mềm máy tính', 'thiết kế xây dựng các ứng dụng cho thiết bị di động', 'ứng dụng thương mại điện tử trên nền web', 'quản trị và xây dựng các giải pháp đảm bảo an toàn cho các hệ thống máy tính và hệ thống mạng máy tính', 'tư vấn thẩm định và phát triển các dự án giải pháp công nghệ thông tin'], 'subject': ['toán', 'vật lý', 'hóa học'], 'tuition': ['5.850.000'], 'subject_group': ['a00', 'a'], 'case': ['thi tốt nghiệp trung học phổ thông'], 'criteria': [240], 'object': ['thi tốt nghiệp thpt năm 2021'], 'register': ['đăng ký dự thi kỳ thi tốt nghiệp thpt 2021', 'đăng ký xét tuyển']}, {'_id': '60588c802c992394968d36ca', 'major_code': ['106'], 'major_name': ['khoa học máy tính'], 'type_edu': ['chính quy', 'đại trà'], 'point': [28.0], 'year': ['2020'], 'career': ['thiết kế xây dựng các phần mềm máy tính', 'thiết kế xây dựng các ứng dụng cho thiết bị di động', 'ứng dụng thương mại điện tử trên nền web', 'quản trị và xây dựng các giải pháp đảm bảo an toàn cho các hệ thống máy tính và hệ thống mạng máy tính', 'tư vấn thẩm định và phát triển các dự án giải pháp công nghệ thông tin'], 'subject': ['toán', 'vật lý', 'tiếng anh'], 'tuition': ['5.850.000'], 'subject_group': ['a01', 'a1'], 'case': ['thi tốt nghiệp trung học phổ thông'], 'criteria': [240], 'object': ['thi tốt nghiệp thpt năm 2021'], 'register': ['đăng ký dự thi kỳ thi tốt nghiệp thpt 2021', 'đăng ký xét tuyển']}, {'_id': '60588c802c992394968d368d', 'major_code': ['206'], 'major_name': ['khoa học máy tính'], 'type_edu': ['chất lượng cao', 'tiên tiến'], 'point': [27.25], 'year': ['2020'], 'career': ['thiết kế xây dựng các phần mềm máy tính', 'thiết kế xây dựng các ứng dụng cho thiết bị di động', 'ứng dụng thương mại điện tử trên nền web', 'quản trị và xây dựng các giải pháp đảm bảo an toàn cho các hệ thống máy tính và hệ thống mạng máy tính', 'tư vấn thẩm định và phát triển các dự án giải pháp công nghệ thông tin'], 'subject': ['toán', 'vật lý', 'tiếng anh'], 'tuition': ['30.000.000'], 'subject_group': ['a01', 'a1'], 'case': ['thi tốt nghiệp trung học phổ thông'], 'criteria': [100], 'object': ['thi tốt nghiệp thpt năm 2021'], 'register': ['đăng ký dự thi kỳ thi tốt nghiệp thpt 2021', 'đăng ký xét tuyển']}, {'_id': '60588c802c992394968d36f8', 'major_code': ['206'], 'major_name': ['khoa học máy tính'], 'type_edu': ['chất lượng cao', 'tiên tiến'], 'point': [27.25], 'year': ['2020'], 'career': ['thiết kế xây dựng các phần mềm máy tính', 'thiết kế xây dựng các ứng dụng cho thiết bị di động', 'ứng dụng thương mại điện tử trên nền web', 'quản trị và xây dựng các giải pháp đảm bảo an toàn cho các hệ thống máy tính và hệ thống mạng máy tính', 'tư vấn thẩm định và phát triển các dự án giải pháp công nghệ thông tin'], 'subject': ['toán', 'vật lý', 'hóa học'], 'tuition': ['30.000.000'], 'subject_group': ['a00', 'a'], 'case': ['thi tốt nghiệp trung học phổ thông'], 'criteria': [100], 'object': ['thi tốt nghiệp thpt năm 2021'], 'register': ['đăng ký dự thi kỳ thi tốt nghiệp thpt 2021', 'đăng ký xét tuyển']}], 'major': '60588c802c992394968d36d5'}, 'request_slots': {}, 'round': 2, 'speaker': 'Agent'}
# # print(len(agent_action['inform_slots']))
# agent_inform_slots = agent_action['inform_slots']
# list_id_record = list(agent_inform_slots.keys())
# print(list_id_record)
# for id_record in list_id_record:
    # print(agent_inform_slots[id_record])

# a = {'key':'value'}
# a = {}
# if a:
#     print('True')
# else:
#     print('False')
# print(dict(a.items()))
# import os
# print(os.environ.get("MONGOLAB_URI"))
# potential_extensions = ['.mp3', '.mp4']
# file_name = 'music.mp3'

# print(file_name.endswith(tuple(potential_extensions)))