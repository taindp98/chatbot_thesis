import requests
from glob import glob
import os
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

# list_case = [0,1,2,3,4]
case_path = './test_case'
list_case = glob(os.path.join(case_path,'*.txt'))
list_num_case = [int(item.split('/')[-1].replace('.txt','').replace('case','')) for item in list_case]
list_num_case_sort = sorted(list_num_case)

for case_num in list_num_case_sort[-1:]:
    print('='*50)
    current_case = os.path.join(case_path,str('case'+str(case_num)+'.txt'))
    # case_num = case.split('/')[-1].replace('.txt','')
    print('case {}'.format(case_num))
    file_input = open(current_case,'r').readlines()
    list_text = []
    for text in file_input:
        text_input = text.replace('\n','')
        print('User: {}'.format(text_input))
        agent = get_bot_response(text_input)
        print('Agent: {}'.format(agent))
        if str(agent).startswith('Thông tin'):
            print('----Pass----')
            break
