import requests

def get_bot_response(userText):
    # userText = request.args.get('msg')
    api_url = 'http://0.0.0.0:6969/api/convers-manager'
    # api_url = 'https://chatbot-hcmut.herokuapp.com/api/convers-manager'
    input_data = {}
    input_data['message'] = str(userText)
    input_data['state_tracker_id'] = '1011'
    r = requests.post(url=api_url, json=input_data)
    chatbot_respose = r.json()
    mess_response = chatbot_respose['message'].replace('\n', r'').replace(r'"',r'')
    return mess_response

file_input = open('/home/taindp/PycharmProjects/thesis/test_case/case2.txt','r').readlines()
list_text = []
for text in file_input:
    text_input = text.replace('\n','')
    print('User: {}'.format(text_input))
    agent = get_bot_response(text_input)
    print('Agent: {}'.format(agent))
