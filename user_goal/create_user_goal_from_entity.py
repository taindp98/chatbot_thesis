import pymongo
import re
import random
import json
import numpy as np
import matplotlib.pyplot as plt
from utils import *
# path_entity = '/home/taindp/Jupyter/deep_q_learning/data/db_entity_31dec.json'
# load database to generate usergoal
# path_entity = '/data/db_hcmut_dqn_31dec.json'
dict_entity = json.load(open(path_entity,'r'))

# major_list =[major for major in list(dict_entity[0].keys())]
# print(major_list)
# print(len(limit_db_100))

def generate_user_goal(num_goal,rule_requests,max_num_inform_slot,major_list,dict_entity):
    user_goal_list = []
    user_inform_list = []
    for ite in range(num_goal):
        for num_request_slot in range(2):
            inform_dict = {}
            request_slot = None
            if num_request_slot > 0:
                request_slot = random.choice(rule_requests)
            num_inform_slot = random.randint(1,max_num_inform_slot)
            
            # print(num_inform_slot)
            for _ in range(num_inform_slot):
                # for i in range(2,num_inform_slot):
                inform_slot = random.choice(major_list)
                while inform_slot == request_slot:
                    inform_slot = random.choice(major_list)
                # print(inform_slot)
                # inform_dict[inform_slot]=[random.choice(dict_entity[0][inform_slot]) for i in range(0,random.randint(1,2))]
                inform_dict[inform_slot]= [random.choice(dict_entity[0][inform_slot])]
            if request_slot != None:
                user_goal_list.append({'request_slots':{request_slot:'UNK'},'diaact':'request','inform_slots':inform_dict})
            else:
                user_goal_list.append({'request_slots':{},'diaact':'request','inform_slots':inform_dict})
                # if inform_dict not in user_inform_list:
            user_inform_list.append(inform_dict)
    return user_goal_list

# rule_requests = ['major_code','major_name','type_edu','point','subject_group','year','major']
# rule_requests = ['major_name', 'type_edu','subject','subject_group','point', 'year']
rule_requests = ['major_name']
agent_request_slots = ['major_name', 'type_edu', 'career', 'subject','tuition_one_credit', 'subject_group', 'satify', 'point', 'major_code','year']
# agent_request_slots = ['major_code','major_name','type_edu','point','subject_group','university_code','university_name','year','career','subject','tuition_one_credit','duration_std','credits','foreign_lang_min']
max_num_request_slot = 1
max_num_inform_slot = len(agent_request_slots)
# list_rule = ['major_code','major_name','type_edu','point']
goal = generate_user_goal(500,rule_requests,max_num_inform_slot,major_list,dict_entity)
print(len(goal))
final_goal= []
for item in goal:
    if item not in final_goal:
        final_goal.append(item)
print(len(final_goal))
len_if = []
for item in final_goal:
    len_if.append(len(item['inform_slots']))
plt.hist(len_if,bins=10)
plt.show()
# print(set(len_if))
print(major_list)
fileout = open('/home/taindp/Jupyter/deep_q_learning/data/goal_hcmut_%s_%s.json'% (max_num_inform_slot,len(final_goal)),'w')
item2str = str(final_goal).replace(r"'",r'"')
fileout.write(item2str)
