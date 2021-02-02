import requests
from flask import Flask, render_template, request
import json
import telegram
import telebot
# from telebot.credentials import bot_token, bot_user_name,URL
# from telebot.mastermind import get_response
import requests

api_key='1607480015:AAFRjjzwhq5FLcwTFgde1gBzjc5v-g5Imck'
def get_bot_response():
    url = "https://api.telegram.org/bot{}/getUpdates".format(api_key)
    response = requests.get(url)
    data=response.json()
    # userText = request.args.get('msg')
    userText = data['result'][-1]['message']['text']
    # print(data['result'][-1]['message'])
    userID = data['result'][-1]['message']['chat']['id']
    api_url = 'http://0.0.0.0:6969/api/convers-manager'
    input_data = {}
    input_data['message'] = str(userText)
    input_data['state_tracker_id'] = str(userID)
    r = requests.post(url=api_url, json=input_data)
    chatbot_respose = r.json()
    mess_response = chatbot_respose['message'].replace('\n', r'').replace(r'"',r'')
    url_response='https://api.telegram.org/bot'+str(api_key)+'/sendmessage?chat_id='+str(userID)+'&text='+str(mess_response)
    response = requests.get(url_response)
    return response
#
get_bot_response()
#
# if __name__ == '__main__':
#     app.run(threaded=True)
