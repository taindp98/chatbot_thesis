import pymongo
import re
import random
import json
import numpy as np
from utils import *
# path_entity = '/home/taindp/PycharmProjects/thesis/data/db_entity_official.json'
# load database to generate usergoal
path_db = '/data/db_hcmut_dqn_31dec.json'
db = json.load(open(path_db,'r'))

# print(len(db))
rule_requests = ['major_name', 'type_edu','subject','subject_group','point', 'year']
# print(len(limit_db_100))
# list_rule = ['major_code','major_name','type_edu','point']
def generate_user_goal(db,num_goal,max_num_inform_slot,rule_requests):
    my_user_goal = []
    for ite in range(num_goal):
        for item in db:

    return my_user_goal


