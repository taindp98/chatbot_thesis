# from chatbot import chatbot
from flask import Flask, render_template, request
import json
import requests

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    api_url = 'http://0.0.0.0:6969/api/convers-manager'
    # api_url = 'https://chatbot-hcmut.herokuapp.com/api/convers-manager'
    input_data = {}
    input_data['message'] = str(userText)
    input_data['state_tracker_id'] = '1011'
    r = requests.post(url=api_url, json=input_data)
    chatbot_respose = r.json()
    mess_response = [item.replace('\n', r'').replace(r'"',r'') for item in chatbot_respose['message']]
    # mess_response = chatbot_respose['message'].replace('\n', r'').replace(r'"',r'')
    # print('mess_response',mess_response)
    return {"message_list":mess_response}

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
