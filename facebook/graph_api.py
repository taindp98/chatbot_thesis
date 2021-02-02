import random
from flask import Flask, request
from pymessenger.bot import Bot
import requests
app = Flask(__name__)
ACCESS_TOKEN = 'EAACXSOaUdSYBAE1ZA0KRXbz8JYhaZBNeZBUAda9JXNLZBrkZAaUI3Pl2sIcfc2P2Efyf4hBlGqz3zmZB9PuMla1BlRjgBgxnMc5FfjDXNTERcmTnZCD4Jq4iUn0IXE2CQaegZBjLf66lZBUY6XalDyio6tAEwSzZAQcKlqiWp3WZBULypIfwb0sQLtZA'
VERIFY_TOKEN = '1011'
bot = Bot(ACCESS_TOKEN)
#id con bot 106253084559943
#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       # print(output)
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            # print(message)
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                # print(message)
                if 'message' in message.keys():
                    userID = message['sender']['id']
                    userText = message['message'].get('text')
                    api_url = 'http://0.0.0.0:6969/api/convers-manager'
                    input_data = {}
                    input_data['message'] = str(userText)
                    input_data['state_tracker_id'] = str(userID)
                    if userID != '106253084559943':
                        r = requests.post(url=api_url, json=input_data)
                        chatbot_respose = r.json()
                        mess_response = chatbot_respose['message'].replace('\n', r'').replace(r'"',r'')
                    #     response_sent_text = get_message()
                        # send_message(userID, response_sent_text)
                        send_message(userID, mess_response)
                #if user sends us a GIF, photo,video, or any other non-text item
                # if message['message'].get('attachments'):
                #     response_sent_nontext = get_message()
                #     send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ['Chào nha']
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
