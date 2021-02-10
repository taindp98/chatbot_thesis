import requests
from flask import Flask, render_template, request
import json
import telegram
import telebot
# from telebot.credentials import bot_token, bot_user_name,URL
# from telebot.mastermind import get_response
import requests

api_key='1607480015:AAFRjjzwhq5FLcwTFgde1gBzjc5v-g5Imck'
# def get_bot_response():
#     url = "https://api.telegram.org/bot{}/getUpdates".format(api_key)
#     response = requests.get(url)
#     data=response.json()
#     # userText = request.args.get('msg')
#     userText = data['result'][-1]['message']['text']
#     # print(data['result'][-1]['message'])
#     userID = data['result'][-1]['message']['chat']['id']
#     api_url = 'http://0.0.0.0:6969/api/convers-manager'
#     input_data = {}
#     input_data['message'] = str(userText)
#     input_data['state_tracker_id'] = str(userID)
#     r = requests.post(url=api_url, json=input_data)
#     chatbot_respose = r.json()
#     mess_response = chatbot_respose['message'].replace('\n', r'').replace(r'"',r'')
#     url_response='https://api.telegram.org/bot'+str(api_key)+'/sendmessage?chat_id='+str(userID)+'&text='+str(mess_response)
#     response = requests.get(url_response)
#     return response
#
import re
from flask import Flask, request
import telegram
# from telebot.credentials import bot_token, bot_user_name,URL


global bot
global TOKEN
TOKEN = api_key
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
   # retrieve the message in JSON and then transform it to Telegram object
   update = telegram.Update.de_json(request.get_json(force=True), bot)

   chat_id = update.message.chat.id
   msg_id = update.message.message_id

   # Telegram understands UTF-8, so encode text for unicode compatibility
   text = update.message.text.encode('utf-8').decode()
   # for debugging purposes only
   print("got text message :", text)
   # the first time you chat with the bot AKA the welcoming message
   if text == "/start":
       # print the welcoming message
       bot_welcome = """
       Welcome to coolAvatar bot, the bot is using the service from http://avatars.adorable.io/ to generate cool looking avatars based on the name you enter so please enter a name and the bot will reply with an avatar for your name.
       """
       # send the welcoming message
       bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)


   else:
       try:
           # clear the message we got from any non alphabets
           text = re.sub(r"W", "_", text)
           # create the api link for the avatar based on http://avatars.adorable.io/
           url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
           # reply with a photo to the name the user sent,
           # note that you can send photos by url and telegram will fetch it for you
           bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
       except Exception:
           # if things went wrong
           bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)

   return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
   s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
   if s:
       return "webhook setup ok"
   else:
       return "webhook setup failed"

@app.route('/')
def index():
   return '.'


if __name__ == '__main__':
   app.run(threaded=True)
# get_bot_response()
#
# if __name__ == '__main__':
#     app.run(threaded=True)
