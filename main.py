from utils import *
from collections import defaultdict
import random
import pymongo
import warnings
from response.user_request import *
from intent.intent_regconize import *
from pyvi import ViTokenizer, ViPosTagger
from tqdm import tqdm
from response.agent_response import *
from response.agent_action import *
from entity.pattern_ner import *
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
if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    # user_action = {'intent': 'inform', 'request_slots': {'major_code': 'UNK'}, 'inform_slots': {'major_name': ['hóa học']}}
    FOLDER_PATH = '/home/taindp/PycharmProjects/thesis/dqn'
    CONSTANTS_FILE_PATH = f'{FOLDER_PATH}/constants.json'
    constants_file = CONSTANTS_FILE_PATH
    with open(constants_file) as f:
        constants = json.load(f)
#     file_path_dict = constants['db_file_paths']
#     DATABASE_FILE_PATH = file_path_dict['database']
#     database= json.load(open(DATABASE_FILE_PATH,encoding='utf-8'))
    client = pymongo.MongoClient("mongodb://taindp:chatbot2020@thesis-shard-00-00.bdisf.mongodb.net:27017,thesis-shard-00-01.bdisf.mongodb.net:27017,thesis-shard-00-02.bdisf.mongodb.net:27017/<dbname>?ssl=true&replicaSet=atlas-12fynb-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.hcmut
    collection = db['general'].find({})
    # collection = db['general']
    database = []
    for item in collection:
        database.append(item)
    state_tracker = StateTracker(database, constants)
    dqn_agent = DQNAgent(state_tracker.get_state_size(), constants)
    done = False
    mess = 'cho em hỏi em muốn  thi ngành bảo dưỡng công nghiệp thì nên tập trung học môn nào ạ'
    # mess = 'cho em hỏi học điện tử sau này ra trường làm gì ạ'
    user_action,confirm_obj = (user_request(mess,state_tracker))
    print(user_action)
    agent_action = get_agent_action(state_tracker, dqn_agent, user_action)
    print(agent_action)
    print(response_craft(agent_action, state_tracker,confirm_obj))

