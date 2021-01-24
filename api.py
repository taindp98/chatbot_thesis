import flask
import io
import sys
import pymongo
from flask_pymongo import PyMongo
from flask import Flask, request,render_template,jsonify
from flask_cors import CORS
from fastai import *
from fastai.text import *
from response.user_request import *
from dqn.state_tracker import StateTracker
from dqn.dqn_agent import DQNAgent

from keras import backend as K
from intent.intent_regconize import *
from response.user_request import user_request
from response.agent_action import get_agent_action
from response.agent_response import response_craft
from response.default_response import response_to_user_free_style

from bs4 import BeautifulSoup
# from mongoengine import connect

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017"
mongo = PyMongo(app)
FOLDER_PATH = '/home/taindp/PycharmProjects/thesis/dqn'
CONSTANTS_FILE_PATH = f'{FOLDER_PATH}/constants.json'
# CONSTANT_FILE_PATH = 'constants.json'
with open(CONSTANTS_FILE_PATH) as f:
    constants = json.load(f)

client = pymongo.MongoClient("mongodb://taindp:chatbot2020@thesis-shard-00-00.bdisf.mongodb.net:27017,thesis-shard-00-01.bdisf.mongodb.net:27017,thesis-shard-00-02.bdisf.mongodb.net:27017/hcmut?ssl=true&replicaSet=atlas-12fynb-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.hcmut
collection = db['general'].find({})
# collection = db['general']
database = []
for item in collection:
    database.append(item)

# khoi tao app
app = Flask(__name__)
CORS(app)
StateTracker_Container = dict()
app.config["MONGO_URI"] = "mongodb://taindp:chatbot2020@thesis-shard-00-00.bdisf.mongodb.net:27017,thesis-shard-00-01.bdisf.mongodb.net:27017,thesis-shard-00-02.bdisf.mongodb.net:27017/hcmut?ssl=true&replicaSet=atlas-12fynb-shard-0&authSource=admin&retryWrites=true&w=majority"
mongo = PyMongo(app)

def msg(code, mess=None):
    if code == 200 and mess is None:
        return jsonify({"code": 200, "value": True})
    else:
        return jsonify({"code": code, "message": mess}), code

def get_new_id():
    while (True):
        _id = str(random.randint(100000, 999999))
        if _id not in StateTracker_Container.keys():
            return _id

def process_conversation_POST(state_tracker_id, message):
    state_tracker = None
    print('tracker_id',state_tracker_id)
    if state_tracker_id in StateTracker_Container.keys():
        state_tracker = StateTracker_Container[state_tracker_id][0]
        confirm_obj = StateTracker_Container[state_tracker_id][1]
    else:
        # print("---------------------------------in model")
        state_tracker = StateTracker(database, constants)
        confirm_obj = None
        StateTracker_Container[state_tracker_id] = (state_tracker, confirm_obj)

#
    user_action, new_confirm_obj = user_request(message,state_tracker)
    print("-----------------------------------user action")
    print(user_action)
    #nếu là câu request mới của user thì reset state tracker và cho confirm về lại None
    if user_action['request_slots'] != {}:
        state_tracker.reset()
        confirm_obj = None
    #nếu có câu confirm request mới thì ghi đè
    if new_confirm_obj != None:
        confirm_obj = new_confirm_obj
    if user_action['intent'] not in ["hello","other","done"] :
        dqn_agent = DQNAgent(state_tracker.get_state_size(), constants)
        agent_act = get_agent_action(state_tracker, dqn_agent, user_action)
        print('========================')
        print('agent action',agent_act)
        print('========================')
        StateTracker_Container[state_tracker_id] = (state_tracker,confirm_obj)
        agent_message = response_craft(agent_act, state_tracker,confirm_obj)
    else:
        # to prevent key error
        agent_act = {'intent':user_action['intent'],'request_slots':[],'inform_slots':[]}
        print('========================')
        print('agent action',agent_act)
        print('========================')
        agent_message = random.choice(response_to_user_free_style[user_action['intent']])
        #nếu là done thì reset và cho confirm về None
        if user_action['intent'] == "done":
            state_tracker.reset()
            StateTracker_Container[state_tracker_id] = (state_tracker,None)
    return agent_message,agent_act

# @app.route('/')
# def index():
#     return """<h1>HCMUT Assitant</h1>"""

@app.errorhandler(404)
def url_error(e):
    print("---------------------")
    return msg(404,'URL ERROR')

@app.errorhandler(500)
def server_error(e):
    return msg(500, "SERVER ERROR")

@app.route('/api/', methods=['POST'])
def post_api():
    input_data = request.get_json(force=True)
    print(input_data)
    if "message" not in input_data.keys():
        return msg(400, "Message cannot be None")
    else:
        message = input_data["message"]
        result,probability,mess_clean = catch_intent(message)
        # probability = probability.tolist()
    return jsonify({"code": 200, "message": result, "probability": probability})

@app.route('/api/convers-manager', methods=['POST'])
def post_api_cse_assistant():
    input_data = request.json

    if "message" not in input_data.keys():
        return msg(400, "Message cannot be None")
    else:
        message = input_data["message"]
    print("-------------------------message")
    print(message)
    if "state_tracker_id" not in input_data.keys():
        state_tracker_id = get_new_id()
    else:
        state_tracker_id = input_data["state_tracker_id"]
    print('StateTracker_Container',StateTracker_Container)
    K.clear_session()
    current_informs = 'null'
    agent_message , agent_action = process_conversation_POST(state_tracker_id, message)
    if agent_action['intent'] in ["match_found","inform"]:
        current_informs = StateTracker_Container[state_tracker_id][0].current_informs
    K.clear_session()
    return jsonify({"code": 200, "message": agent_message,"state_tracker_id":state_tracker_id,"agent_action":agent_action,"current_informs":current_informs})

@app.route('/api/cse-assistant-conversation-manager/reset-state-tracker', methods=['POST'])
def post_api_cse_assistant_reset_state_tracker():
    input_data = request.json

    if "state_tracker_id" not in input_data.keys():
        return msg(400, "Message cannot be None")
    else:
        state_tracker_id = input_data["state_tracker_id"]
    # print("-------------------------state_tracker_id")
    # print(state_tracker_id)
    # # if "state_tracker_id" not in input_data.keys():
    # #     state_tracker_id = get_new_id()
    # # else:
    # #     state_tracker_id = input_data["state_tracker_id"]
    # print(StateTracker_Container)
    K.clear_session()

    if state_tracker_id in StateTracker_Container:
        state_tracker = StateTracker_Container[state_tracker_id][0]
        state_tracker.reset()
        StateTracker_Container[state_tracker_id] = (state_tracker,None)
        message = "success"
        code = 200
    else:
        message = "fail"
        code = 404
    K.clear_session()
    return jsonify({"code": code, "message": message,"state_tracker_id":state_tracker_id})


# @app.route('/api/LT-conversation-manager/extract-information', methods=['POST'])
# def post_api_extract_information():
#     input_data = request.json
#     print(input_data)
#     if "message" not in input_data.keys():
#         return msg(400, "Message cannot be None")
#     else:
#         message = input_data["message"]
#         print(message)
#         emails, phones, names = extract_information(message)
#         print(emails)
#         print(phones)
#     return jsonify({"code": 200, "emails": emails, "phones": phones, "names": names})


@app.route("/api/LT-conversation-manager/messages", methods=['POST'])
def user_profile():
    input_data = request.json
    print(input_data)
    if "message" not in input_data.keys():
        return msg(400, "Message cannot be None")
    if "intent" not in input_data.keys():
        return msg(400, "Intent cannot be None")
    user_id = input_data["user_id"]
    message = input_data["message"]
    intent = input_data["intent"]
    is_correct = input_data["is_correct"]

    # check mongo insert cloud
    mongo.db.messages.insert_one(
        {"user_id": user_id, "message": message, "intent": intent, "is_correct": is_correct})

    return jsonify({"code": 200, "message": "insert successed!"})

@app.route('/api/LT-conversation-manager/classify-message', methods=['POST'])
def post_api_classify_message():
    input_data = request.get_json(force=True)
    print(input_data)
    if "message" not in input_data.keys():
        return msg(400, "Message cannot be None")
    else:
        message = input_data["message"]
        result,probability,mess_clean = catch_intent(message)
    return jsonify({"is_question": check_question(message), "intent": result})


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0',port=6969,debug=True)

